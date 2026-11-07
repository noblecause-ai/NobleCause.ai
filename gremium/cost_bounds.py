"""Reviewed provider envelopes and Steward-approved operational budgets.

Operational limits are empirical allowances with accepted provider billing risk.
Every request is checked locally and every confirmed bill is checked afterward.
"""
import json
from pathlib import Path

from council_state import digest, encoded
from openrouter import MODELS, OpenRouterError, amount, integer, worst_case_usd


class MissingBound(OpenRouterError):
    pass


class InsufficientBudget(OpenRouterError):
    pass


class InputBounds:
    def __init__(self, policies, evidence_root):
        self.policies, self.root = policies, Path(evidence_root).resolve()

    def policy(self, spec):
        rule = self.policies.get(spec['model'])
        if not rule:
            raise MissingBound('B4: kein belegter Input-Bound für ' + spec['model'])
        if (rule.get('endpoint') != spec['openrouter']['endpoint']
                or rule.get('quantization') != spec['openrouter']['quantization']
                or not rule.get('review_reference')):
            raise MissingBound('B4: Input-Bound nicht an Anbieter/Präzision/Review gebunden')
        if rule.get('basis') == 'operational_limits':
            if (rule.get('risk_accepted') is not True
                    or not integer(rule.get('max_request_bytes'))
                    or not integer(rule.get('input_tokens'))):
                raise MissingBound('B4: freigegebene Betriebsgrenzen mit Sicherheitsaufschlag erforderlich')
            integer(rule.get('output_margin_percent'))
            return rule
        if rule.get('basis') != 'reviewed_provider_envelope':
            raise MissingBound('B4: unbekannte Budgetgrundlage')
        evidence = (self.root / rule['evidence_path']).resolve()
        if not evidence.is_relative_to(self.root) or not evidence.is_file() or digest(evidence.read_bytes()) != rule['evidence_sha256']:
            raise MissingBound('B4: Input-Bound-Beleg fehlt oder wurde geändert')
        # The reviewed document must justify this exact finite envelope, including
        # gateway/upstream message framing. Empirical average counts do not qualify.
        contract = json.loads(evidence.read_text())
        fields = ('model', 'endpoint', 'quantization', 'max_request_bytes', 'input_tokens', 'review_reference')
        expected = {**rule, 'model': spec['model']}
        if any(contract.get(k) != expected[k] for k in fields) or contract.get('covers_message_framing') is not True:
            raise MissingBound('B4: Beleg deckt Request-Hülle nicht ab')
        if spec['model'] == MODELS['spacexai']:
            output_limits = rule.get('verified_billed_output_limits', [])
            if contract.get('verified_billed_output_limits', []) != output_limits:
                raise MissingBound('B4: Groks Abrechnungsgrenzen passen nicht zum Beleg')
        if not integer(rule['max_request_bytes']) or not integer(rule['input_tokens']):
            raise MissingBound('B4: positive endliche Grenzen erforderlich')
        return rule

    def tokens(self, spec, request):
        rule = self.policy(spec)
        if len(json.dumps(request, ensure_ascii=False).encode()) > rule['max_request_bytes']:
            raise MissingBound('B4: konkreter Request überschreitet konfigurierte Eingabehülle')
        return rule['input_tokens']

    def ceiling(self, spec, max_tokens):
        rule = self.policy(spec)
        # Grok previously billed past max_tokens on this route, including reasoning.
        if spec['model'] == MODELS['spacexai'] and rule['basis'] == 'reviewed_provider_envelope':
            limit = min(max_tokens, spec['openrouter']['max_output_tokens'])
            if limit not in rule.get('verified_billed_output_limits', []):
                raise MissingBound('B4: Groks Ausgabegrenze einschließlich Reasoning nicht belegt')
        return worst_case_usd(spec, max_tokens, rule['input_tokens'],
                              billed_output_limit=self.output_tokens(spec, max_tokens))

    def output_tokens(self, spec, max_tokens):
        rule = self.policy(spec)
        requested = min(integer(max_tokens), spec['openrouter']['max_output_tokens'])
        margin = rule['output_margin_percent'] if rule['basis'] == 'operational_limits' else 0
        return requested + (requested * margin + 99) // 100


class Budget:
    def __init__(self, cap_usd, bounds=None, *, observe=False):
        self.cap = amount(cap_usd)
        if not self.cap:
            raise ValueError('Positives Sitzungsbudget erforderlich')
        self.bounds, self.spent, self.observe = bounds, amount(0), observe
        self.mode = 'observe' if observe else 'bounded'
        if not observe and any(p.get('basis') == 'operational_limits' for p in bounds.policies.values()):
            self.mode = 'operational'

    def check(self, spec, request, limit, remaining):
        """Reserve the current call AND every required remaining closure call."""
        if self.observe:
            if self.spent >= self.cap:
                raise InsufficientBudget('Abgerechnetes Testbudget erreicht; kein Folgeaufruf')
            return None, amount(0)
        tokens = self.bounds.tokens(spec, request)
        required = self.bounds.ceiling(spec, limit)
        reserve = sum((self.bounds.ceiling(s, n) for s, n in remaining), amount(0))
        if self.spent + required + reserve > self.cap:
            raise InsufficientBudget('Budget reicht nicht für nächsten Aufruf und Abschlussreserve')
        return tokens, reserve

    def record(self, usage):
        self.spent += amount(usage['billed_usd'])
        if self.spent > self.cap:
            raise OpenRouterError('Abgerechnetes Budget überschritten; kein Folgeaufruf')
