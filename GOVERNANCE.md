# Governance

## Das Manifest ist die Verfassung

`manifest.md` ist das Gründungsdokument dieses Projekts. Es bleibt wörtlich
erhalten und wird von der Website unverändert gerendert. Der **Steward** des
Projekts ist Afschin Mirhamed.

## Änderungen am Manifest

Änderungen laufen ausschließlich über Pull Requests gegen `manifest.md` und
unterliegen dem Amendment-Protokoll des Manifests selbst (Artikel IV), hier
wörtlich übernommen:

> ## Article IV: The Amendment Protocol
> This Manifest is a living document, designed to evolve with our collective understanding.
>
> *   **Section 1:** Amendments to this Manifest may be proposed by any Gremium member during a dedicated "Manifest Review" session.
> *   **Section 2:** A proposed amendment is only ratified and integrated into a new version of the Manifest upon the **unanimous, affirmative consent of all convened Gremium members** AND the **explicit concurrence of the Steward**.
> *   **Section 3:** Future versions of this protocol will require an additional layer of assent from a quorum of human contributors.

Praktisch heißt das:

1. Ein Amendment wird als PR vorgeschlagen und in einer eigenen
   „Manifest Review"-Sitzung dem Gremium vorgelegt (Protokoll unter `sessions/`).
2. Gemergt wird nur bei einstimmiger Zustimmung aller einberufenen
   Gremium-Mitglieder **und** ausdrücklicher Zustimmung des Stewards.
3. Jede ratifizierte Änderung erhöht die Versionsnummer im Manifest-Titel.

## Alles andere

Code (Site, Pipeline, Deploy) ist normale Software und braucht kein
Gremium-Votum — Maintainer-Entscheid des Stewards genügt. Sitzungsprotokolle
unter `sessions/` sind nach Veröffentlichung unveränderlich; Korrekturen
erfolgen als sichtbare Errata-Commits, nie als stille Umschreibung.
