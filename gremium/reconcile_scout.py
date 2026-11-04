#!/usr/bin/env python3
"""Recheck one existing Scout charge with GET requests only.

The original evidence and schedule remain unchanged. A resolved charge is not
a valid dossier and does not automatically authorize resuming an aborted run.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

import openrouter_scout as scout
from openrouter import decode, http

ROOT = Path(__file__).resolve().parents[1]


def hashes(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob('*')) if p.is_file()}


def reconcile(raw_dir, output_dir, config):
    raw_dir, output_dir = Path(raw_dir).resolve(), Path(output_dir).resolve()
    if output_dir == raw_dir or raw_dir in output_dir.parents:
        raise ValueError('Reconciliation evidence must be outside the original raw directory')
    originals = hashes(raw_dir)
    response = decode((raw_dir / 'openrouter-response.json').read_bytes())
    request = decode((raw_dir / 'openrouter-request.json').read_bytes())
    model = decode((raw_dir / 'openrouter-model.json').read_bytes())
    matches = [s for s in config['scouts'] if s['model'] == request.get('model')]
    if len(matches) != 1:
        raise ValueError('Original Scout configuration missing or ambiguous')
    spec = matches[0]
    scout.contract(spec)
    gid = response.get('id')
    if not isinstance(gid, str) or not gid.startswith('gen-'):
        raise ValueError('Original response has no usable generation ID')
    output_dir.mkdir(parents=True, exist_ok=False)

    def save(name, payload):
        data = payload if isinstance(payload, bytes) else (
            json.dumps(payload, ensure_ascii=False, indent=2, default=str) + '\n').encode()
        with (output_dir / name).open('xb') as stream:
            stream.write(data)

    report = {'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'generation_id': gid, 'model': spec['model'],
              'status': 'unresolved', 'inference_calls': 0,
              'schedule_changed': False, 'original_sha256': originals}
    try:
        receipt = http('GET', '/generation?id=' + quote(gid, safe=''))
        save('generation-recheck.json', receipt)
        receipt_data = decode(receipt)
        report['receipt_error_code'] = (receipt_data.get('error') or {}).get('code')
        key = decode(http('GET', '/key')).get('data') or {}
        # Never store arbitrary key/account fields or credential-bearing errors.
        safe_key = {k: key.get(k) for k in ('limit', 'limit_reset', 'limit_remaining', 'usage')}
        save('key-after.json', safe_key)
        report['key_after'] = safe_key
        text, usage, raw, _ = scout.assess(
            spec, response, decode(receipt), model.get('canonical_slug') or model['id'])
        report.update(status='charge_verified', billed_usd=usage['billed_usd'],
                      stop_reason=raw['stop_reason'], dossier_valid=False)
        from run_wart import parse_scout_answer
        try:
            parsed = parse_scout_answer(text)
            report['dossier_valid'] = (raw['stop_reason'] == 'end_turn'
                                       and len(parsed['findings']) <= spec['max_findings'])
        except SystemExit:
            pass
    except Exception as exc:
        report['error_type'] = type(exc).__name__
    finally:
        report['originals_unchanged'] = hashes(raw_dir) == originals
        if not report['originals_unchanged']:
            report['status'] = 'unresolved'
            report['error_type'] = 'OriginalEvidenceChanged'
        save('reconciliation.json', report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-dir', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--config', type=Path, default=ROOT / 'gremium/config.json')
    parser.add_argument('--env-root', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    from envtools import load_env, require_keys
    load_env(args.env_root / 'gremium', args.env_root)
    require_keys('OPENROUTER_API_KEY')
    report = reconcile(args.raw_dir, args.output_dir, json.loads(args.config.read_text()))
    print(json.dumps(report, ensure_ascii=False, default=str))
    return 0 if report['status'] == 'charge_verified' else 2


if __name__ == '__main__':
    raise SystemExit(main())
