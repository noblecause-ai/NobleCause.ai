"""Evidence-backed input envelopes. No guessed tokenizer or context fallback.

Policies are trusted, reviewed configuration, not model output. No production
policy is shipped. The separately authorized observe mode logs billed costs
without an input envelope or a closure reserve; it never invents a bound.
"""
import json
from pathlib import Path

from council_state import digest, encoded
from openrouter import OpenRouterError, amount, integer, worst_case_usd


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
                or rule.get('basis') != 'reviewed_provider_envelope'
                or not rule.get('review_reference')):
            raise MissingBound('B4: Input-Bound nicht an Anbieter/Präzision/Review gebunden')
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
        if not integer(rule['max_request_bytes']) or not integer(rule['input_tokens']):
            raise MissingBound('B4: positive endliche Grenzen erforderlich')
        return rule

    def tokens(self, spec, request):
        rule = self.policy(spec)
        if len(json.dumps(request, ensure_ascii=False).encode()) > rule['max_request_bytes']:
            raise MissingBound('B4: konkreter Request überschreitet belegte Eingabehülle')
        return rule['input_tokens']

    def ceiling(self, spec, max_tokens):
        return worst_case_usd(spec, max_tokens, self.policy(spec)['input_tokens'])


class Budget:
    def __init__(self, cap_usd, bounds=None, *, observe=False):
        self.cap = amount(cap_usd)
        if not self.cap:
            raise ValueError('Positives Sitzungsbudget erforderlich')
        self.bounds, self.spent, self.observe = bounds, amount(0), observe

    def check(self, spec, request, limit, remaining):
        """Reserve the current call AND every required remaining closure call."""
        if self.observe:
            if self.spent >= self.cap:
                raise InsufficientBudget('Abgerechnetes Testbudget erreicht; kein Folgeaufruf')
            return None, amount(0)
        tokens = self.bounds.tokens(spec, request)
        required = worst_case_usd(spec, limit, tokens)
        reserve = sum((self.bounds.ceiling(s, n) for s, n in remaining), amount(0))
        if self.spent + required + reserve > self.cap:
            raise InsufficientBudget('Budget reicht nicht für nächsten Aufruf und Abschlussreserve')
        return tokens, reserve

    def record(self, usage):
        self.spent += amount(usage['billed_usd'])
        if self.spent > self.cap:
            raise OpenRouterError('Abgerechnetes Budget überschritten; kein Folgeaufruf')
