#!/usr/bin/env python3
"""One explicitly authorized Scout test; no council, retries or activation.

The existing key must have at most one credit left under a temporarily lowered
server limit. The recorded starting usage also prevents a second paid attempt
after the first charge. Native search parameters alone are not a spend cap.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlparse

import openrouter_scout as scout
import prompts
from openrouter import amount
from run_wart import parse_scout_answer

ROOT = Path(__file__).resolve().parents[1]
BASE_USAGE = '32.870685307'
TEST_BUDGET = '1'


def budget_guard(key):
    if (key.get('limit_reset') is not None or amount(key['usage']) != amount(BASE_USAGE)
            or not 0 < amount(key['limit_remaining']) <= amount(TEST_BUDGET)
            or not 0 < amount(key['limit']) - amount(BASE_USAGE) <= amount(TEST_BUDGET)):
        raise ValueError('Test needs unchanged starting usage and at most one credit of server-side key room')


def check_dossier(text, stop_reason, spec, as_of):
    if stop_reason != 'end_turn':
        raise ValueError('Scout did not complete successfully')
    try:
        parsed = parse_scout_answer(text)
    except SystemExit:
        raise ValueError('Scout did not return a structured dossier') from None
    findings = parsed['findings']
    if (not 1 <= len(findings) <= spec['max_findings']
            or len(parsed['rejected_findings']) > 2
            or len(parsed['delta_assessment'].split()) > 60
            or not parsed['search_queries']
            or any(not isinstance(q, str) or not q.strip() for q in parsed['search_queries'])):
        raise ValueError('Incomplete dossier or requested limits exceeded')
    for finding in findings:
        if finding.get('pillar') not in 'ABCD' or len(str(finding.get('pillar'))) != 1:
            raise ValueError('Invalid pillar')
        for field in ('topic', 'summary', 'source', 'source_language', 'evidence_type', 'uncertainty', 'counterevidence'):
            if not isinstance(finding.get(field), str) or not finding[field].strip():
                raise ValueError('Missing finding evidence field: ' + field)
        url = urlparse(finding['source'])
        if url.scheme not in ('http', 'https') or not url.hostname or url.username or url.password:
            raise ValueError('Invalid source URL')
        for field in ('source_date', 'event_date'):
            if field not in finding:
                raise ValueError('Missing source/event date field')
            if finding[field] is not None and dt.date.fromisoformat(finding[field]) > as_of:
                raise ValueError('Future source/event date')
        words = sum(len(v.split()) for v in finding.values() if isinstance(v, str))
        if words > spec['max_words_per_finding']:
            raise ValueError('Finding exceeds requested word limit')
    return parsed


def run(root=ROOT, *, paid=False):
    root = Path(root)
    spec = json.loads((root / 'gremium/gemini-scout-candidate.json').read_text())
    if not paid:
        return {'status': 'not_started', 'inference_calls': 0}
    if (os.environ.get('GITHUB_EVENT_NAME') != 'workflow_dispatch'
            or os.environ.get('GITHUB_REF') != 'refs/heads/codex/gemini-scout-canary-20261104'
            or os.environ.get('GITHUB_REPOSITORY') != 'noblecause-ai/NobleCause.ai'
            or os.environ.get('GITHUB_RUN_ATTEMPT') != '1'):
        raise ValueError('Paid canary requires the single approved manual Actions attempt')
    key = scout.key_state()
    budget_guard(key)
    output = root / 'gremium/.probe-raw/gemini-canary'
    output.mkdir(parents=True, exist_ok=False)
    as_of = dt.date(2026, 11, 4)
    system = prompts.scout_system_for(spec, prompts.SCOUT_SYSTEM)
    user = prompts.SCOUT_BLIND_USER.format(question=prompts.SCOUT_BLIND_QUESTION, as_of=as_of.isoformat())
    (output / 'prompt-system.txt').write_text(system)
    (output / 'prompt-user.txt').write_text(user)
    report = {'status': 'not_started', 'inference_calls': 0, 'model': spec['model'],
              'test_budget_credits': TEST_BUDGET, 'key_before': key,
              'production_changed': False, 'dossier_requires_source_review': True}
    try:
        # call_scout itself records the request before exactly one POST and never
        # retries inference. A missing receipt stops all further paid work.
        text, usage, raw, _ = scout.call_scout(spec, system, user, output)
        report.update(inference_calls=1, billed_usd=usage['billed_usd'])
        if amount(usage['billed_usd']) > amount(TEST_BUDGET):
            raise ValueError('Billed amount exceeds authorized test budget')
        parsed = check_dossier(text, raw['stop_reason'], spec, as_of)
        (output / 'dossier.json').write_text(json.dumps(parsed, ensure_ascii=False, indent=2))
        report.update(status='technical_pass', findings=len(parsed['findings']),
                      pillars=sorted({f['pillar'] for f in parsed['findings']}),
                      search_provenance=usage['research_provenance'])
    except Exception as exc:
        report.update(status='failed', error_type=type(exc).__name__)
    finally:
        if (output / 'openrouter-request.json').exists():
            report['inference_calls'] = 1  # Sent or uncertain; never report it as free.
        try:
            report['key_after'] = scout.key_state()
        except Exception as exc:
            report['key_after_error_type'] = type(exc).__name__
        (output / 'canary-status.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str))
        # Existing status workflow archives run.log. Export only this controlled
        # evidence directory; no environment, headers, credentials or other files.
        for path in sorted(output.iterdir()):
            if path.is_file():
                data = path.read_bytes()
                print('NC_CANARY_FILE ' + json.dumps({'name': path.name,
                    'sha256': hashlib.sha256(data).hexdigest(),
                    'base64': base64.b64encode(data).decode()}), flush=True)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-paid', action='store_true')
    args = parser.parse_args(argv)
    result = run(paid=args.run_paid)
    print(json.dumps(result, ensure_ascii=False, default=str))
    return 0 if result['status'] in ('not_started', 'technical_pass') else 2


if __name__ == '__main__':
    raise SystemExit(main())
