"""Explicit per-pillar decisions for new live ballots; never inferred from prose."""

CONTRACT = 'explicit_abstention_v1'


def check_contract(contract):
    if contract not in (None, CONTRACT):
        raise ValueError('Unbekannter Votumsvertrag')


def read_decision(rec):
    """Return recommend/abstain, or None for an incomplete/conflicting ballot."""
    if not isinstance(rec, dict) or not {
        'decision', 'organization', 'donation_url', 'conditional',
        'reservation', 'abstention_reason'
    } <= rec.keys():
        return None
    decision = rec['decision']
    if decision == 'abstain':
        if (any(rec[k] is not None for k in ('organization', 'donation_url', 'conditional', 'reservation'))
                or not isinstance(rec['abstention_reason'], str) or not rec['abstention_reason'].strip()):
            return None
    elif decision == 'recommend':
        if (not isinstance(rec['organization'], str) or not rec['organization'].strip()
                or type(rec['conditional']) is not bool or rec['abstention_reason'] is not None
                or (rec['conditional'] and (not isinstance(rec['reservation'], str) or not rec['reservation'].strip()))
                or (not rec['conditional'] and rec['reservation'] is not None)):
            return None
    else:
        return None
    return decision
