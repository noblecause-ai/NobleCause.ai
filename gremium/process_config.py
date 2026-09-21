"""Gemeinsame Prozessschalter und Rollen-Invarianten.

Beide neuen Verfahren bleiben bis zur ausdrücklichen Steward-Freigabe aus.
Die Funktionen liegen absichtlich gemeinsam, damit Wochen- und Sitzungslauf
dieselben Grenzen prüfen und kein zweites Auswahlverfahren entsteht.
"""

SUPPORTED_SCOUT_FAMILIES = {"anthropic", "google"}
SCOUT_RESEARCH_ROLES = {"discovery", "regional", "counterevidence"}


def feature_enabled(config, name):
    feature = (config.get("features") or {}).get(name) or {}
    return feature.get("enabled") is True


def configured_scouts(config):
    """Liefert die aktive Scout-Besetzung und prüft ihre Governance-Grenzen.

    Im bestehenden Verfahren ist ``scout`` die einzige Quelle.
    Die Schalter ``two_scouts`` und ``three_scouts`` sind exklusiv. Die
    genehmigte Besetzung in ``scouts`` ist von der technischen Aktivierung
    getrennt; eine fehlende Transportfreigabe wird nicht still übergangen.
    """
    wart = config.get("wart")
    live = feature_enabled(config, 'live_council')
    council = config['live_council']['models'] if live else (config.get("models") or [])
    if not live and not wart:
        raise ValueError("wart fehlt in config.json")

    two = feature_enabled(config, "two_scouts")
    three = feature_enabled(config, "three_scouts")
    if live and not three:
        raise ValueError('Live-Rat benötigt die drei genehmigten blinden Scouts')
    if two and three:
        raise ValueError("two_scouts und three_scouts dürfen nicht gleichzeitig aktiv sein")
    if two or three:
        count = 3 if three else 2
        feature = "three_scouts" if three else "two_scouts"
        count_label = "drei" if three else "zwei"
        scouts = config.get("scouts")
        if not isinstance(scouts, list) or len(scouts) != count:
            raise ValueError(f"{feature} verlangt genau {count_label} Einträge in config.scouts")
        if any(not isinstance(s, dict) or not s.get("family") or not s.get("model") for s in scouts):
            raise ValueError("jeder Scout braucht family und model")
        families = [s.get("family") for s in scouts]
        models = [s.get("model") for s in scouts]
        if len(set(families)) != count:
            raise ValueError("die Scouts müssen aus verschiedenen Familien stammen")
        if len(set(models)) != count:
            raise ValueError("die Scouts müssen verschiedene Modelle sein")
        if three and {s.get("research_role") for s in scouts} != SCOUT_RESEARCH_ROLES:
            raise ValueError("drei Scouts brauchen discovery, regional und counterevidence je genau einmal")
        if three and any(s.get("research_context") != "blind" for s in scouts):
            raise ValueError("drei Scouts brauchen research_context=blind ohne frühere Ergebnisse")
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
    if not live and any(s["model"] == wart.get("model") for s in scouts):
        raise ValueError("Scout und Wart dürfen nicht dasselbe Modell sein")
    return scouts


def configured_wart(config, schedule=None):
    if feature_enabled(config, 'live_council'):
        from council_state import chair_for
        if schedule is None:
            raise ValueError('Vorsitz braucht einen expliziten Schedule-Snapshot')
        chair, index = chair_for(config, schedule)
        return {**chair, 'role':'weekly_chair', 'rotation_index':index}
    if feature_enabled(config, "three_scouts"):
        from openrouter_scout import contract
        wart = config["wart_openrouter"]
        contract(wart)
        if wart["model"].removeprefix("anthropic/") != config["wart"]["model"]:
            raise ValueError("Wart-Transport darf das genehmigte Modell nicht ändern")
        return wart
    return config["wart"]


def validate_scout_transport(scout):
    """Validate before SDK/network; never send gateway slugs to direct SDKs."""
    if scout.get("transport") == "openrouter_api":
        from openrouter_scout import contract
        contract(scout)
        return
    if scout.get("transport", "api") != "api":
        raise ValueError("Unbekannter Scout-Transport")
    if scout.get("family") not in SUPPORTED_SCOUT_FAMILIES:
        raise ValueError(f"Kein freigegebener Web-Suche-Adapter für Scout-Familie {scout.get('family')!r}")


def _finding_key(finding):
    """Exakter, datenbasierter Vergleich; kein semantisches/Fuzzy-Raten."""
    return (
        str(finding.get("pillar") or "").strip().upper(),
        str(finding.get("topic") or "").strip().casefold(),
        str(finding.get("source") or "").strip().casefold(),
    )


def scout_divergence(parsed_reports):
    """Maschineller Ausweis für zwei oder drei gültige Scout-Berichte.

    Die Prozentzahl beschreibt nur die exakte Überschneidung strukturierter
    Finding-Schlüssel. Sie behauptet keine semantische Gleichheit.
    """
    if len(parsed_reports) not in (2, 3):
        raise ValueError("Divergenz-Ausweis verlangt zwei oder drei gültige Scout-Berichte")
    keyed = []
    for report in parsed_reports:
        keyed.append({_finding_key(f) for f in report.get("findings") or []})
    if len(keyed) == 3:
        shared = set.intersection(*keyed)
        union = set.union(*keyed)
        pairs = []
        for a, b in ((0, 1), (0, 2), (1, 2)):
            pair_union = keyed[a] | keyed[b]
            pairs.append({
                "report_a": a + 1, "report_b": b + 1,
                "overlap_percent": 100.0 if not pair_union else round(
                    len(keyed[a] & keyed[b]) / len(pair_union) * 100, 1
                ),
                "shared": [list(item) for item in sorted(keyed[a] & keyed[b])],
            })
        return {
            "method": "exact_structured_finding_keys_three_scouts",
            "report_count": 3,
            "overlap_percent": 100.0 if not union else round(len(shared) / len(union) * 100, 1),
            "shared": [list(item) for item in sorted(shared)],
            "pairwise": pairs,
            "unique_by_report": [
                {"report_index": i + 1, "findings": [list(item) for item in sorted(
                    own - set.union(*(other for j, other in enumerate(keyed) if j != i))
                )]}
                for i, own in enumerate(keyed)
            ],
        }
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
