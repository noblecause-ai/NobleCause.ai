"""Gemeinsame Prozessschalter und Rollen-Invarianten.

Beide neuen Verfahren bleiben bis zur ausdrücklichen Steward-Freigabe aus.
Die Funktionen liegen absichtlich gemeinsam, damit Wochen- und Sitzungslauf
dieselben Grenzen prüfen und kein zweites Auswahlverfahren entsteht.
"""


def feature_enabled(config, name):
    feature = (config.get("features") or {}).get(name) or {}
    return feature.get("enabled") is True


def configured_scouts(config):
    """Liefert die aktive Scout-Besetzung und prüft ihre Governance-Grenzen.

    Im bestehenden Verfahren ist ``scout`` die einzige Quelle. Erst wenn der
    Schalter ``two_scouts`` ausdrücklich aktiviert ist, wird ``scouts`` mit
    genau zwei Einträgen verlangt. So ändert die bloße Konfiguration neuer
    Kandidaten keinen produktiven Lauf.
    """
    wart = config.get("wart")
    council = config.get("models") or []
    if not wart:
        raise ValueError("wart fehlt in config.json")

    if feature_enabled(config, "two_scouts"):
        scouts = config.get("scouts")
        if not isinstance(scouts, list) or len(scouts) != 2:
            raise ValueError("two_scouts verlangt genau zwei Einträge in config.scouts")
        families = [s.get("family") for s in scouts]
        models = [s.get("model") for s in scouts]
        if len(set(families)) != 2:
            raise ValueError("die beiden Scouts müssen aus verschiedenen Familien stammen")
        if len(set(models)) != 2:
            raise ValueError("die beiden Scouts müssen verschiedene Modelle sein")
        council_families = {m.get("family") for m in council}
        if not any(family not in council_families for family in families):
            raise ValueError("mindestens ein Scout muss aus einer Familie außerhalb des Rats stammen")
    else:
        scout = config.get("scout")
        if not scout:
            raise ValueError("scout fehlt in config.json")
        scouts = [scout]

    if any(not isinstance(s, dict) or not s.get("family") or not s.get("model") for s in scouts):
        raise ValueError("jeder Scout braucht family und model")
    if any(s["model"] == wart.get("model") for s in scouts):
        raise ValueError("Scout und Wart dürfen nicht dasselbe Modell sein")
    return scouts


def _finding_key(finding):
    """Exakter, datenbasierter Vergleich; kein semantisches/Fuzzy-Raten."""
    return (
        str(finding.get("pillar") or "").strip().upper(),
        str(finding.get("topic") or "").strip().casefold(),
        str(finding.get("source") or "").strip().casefold(),
    )


def scout_divergence(parsed_reports):
    """Maschineller Ausweis für genau zwei gültige Scout-Berichte.

    Die Prozentzahl beschreibt nur die exakte Überschneidung strukturierter
    Finding-Schlüssel. Sie behauptet keine semantische Gleichheit.
    """
    if len(parsed_reports) != 2:
        raise ValueError("Divergenz-Ausweis verlangt genau zwei gültige Scout-Berichte")
    keyed = []
    for report in parsed_reports:
        keyed.append({_finding_key(f) for f in report.get("findings") or []})
    both = keyed[0] & keyed[1]
    union = keyed[0] | keyed[1]
    overlap = 100.0 if not union else round(len(both) / len(union) * 100, 1)
    return {
        "method": "exact_structured_finding_keys",
        "overlap_percent": overlap,
        "shared": [list(item) for item in sorted(both)],
        "only_a": [list(item) for item in sorted(keyed[0] - keyed[1])],
        "only_b": [list(item) for item in sorted(keyed[1] - keyed[0])],
    }
