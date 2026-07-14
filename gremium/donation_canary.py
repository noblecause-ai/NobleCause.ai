#!/usr/bin/env python3
"""Spendenlink-Canary — bewacht die einzigen Artefakte, die das Projekt ausliefert.

Prüft jede nicht-leere donation_url aus organizations.json: Statuscode, Redirect-
Ziel und ob das Ziel noch nach einem Spendenweg aussieht. Klassifikation:

  OK      2xx und das Ziel ist NICHT die bloße Startseite.
  BROKEN  4xx/5xx (außer bot-Wall) ODER Redirect landet auf der Startseite
          (Pfad leer) — genau der HKI-Fehlermodus „200, aber kein Formular".
  BLOCKED 403/429 — Seite steht, ist nur bot-gewallt. WARNUNG, KEIN Fail
          (sonst Dauer-Alarm bei Seiten wie Malaria Consortium/NTI).

`sys.exit(1)` nur bei mindestens einem BROKEN. Läuft in CI (wöchentlich).
"""

import glob
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

HERE = Path(__file__).parent
ROOT = HERE.parent

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")
FORM_HINTS = ("donate", "donation", "spende", "give", "gift", "amount",
              "every.org", "donorbox", "givingwhatwecan", "paypal", "stripe")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects nicht automatisch folgen — wir folgen manuell, um die Kette zu
    kontrollieren (urllib stolpert bei manchen 307/308)."""

    def redirect_request(self, *args, **kwargs):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def check(url):
    """(status, code, detail) — status in {OK, BROKEN, BLOCKED}. Folgt Redirects
    explizit (max. 6 Hops) und erkennt den HKI-Fehlermodus (Landung auf Startseite)."""
    conf_path = urlparse(urldefrag(url)[0]).path.strip("/")
    current = urldefrag(url)[0]  # #/donate ist client-seitig
    for _ in range(6):
        req = urllib.request.Request(current, headers={"User-Agent": UA}, method="GET")
        try:
            resp = _OPENER.open(req, timeout=25)
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308):
                loc = e.headers.get("Location")
                if not loc:
                    return "BROKEN", e.code, "Redirect ohne Location"
                current = urljoin(current, loc)
                continue
            if e.code in (403, 429):
                return "BLOCKED", e.code, "bot-gewallt (Sicht-Check)"
            return "BROKEN", e.code, "HTTP-Fehler"
        except Exception as e:  # noqa: BLE001
            return "BROKEN", f"ERR:{type(e).__name__}", "nicht erreichbar"
        code = resp.status
        body = resp.read(8192).decode("utf-8", "ignore").lower()
        if conf_path and not urlparse(current).path.strip("/"):
            return "BROKEN", code, f"Redirect auf Startseite → {current} (kein Formular)"
        hint = "" if any(k in body for k in FORM_HINTS) else " (Achtung: keine Spenden-Stichworte im HTML)"
        return "OK", code, f"→ {current}{hint}"
    return "BROKEN", "loop", "zu viele Redirects"


def published_org_ids():
    """org_ids, die in einer Sitzung als Konsens PUBLIZIERT sind (= gerenderte
    Spendenlinks). Nur deren Bruch ist ein echter Alarm."""
    ids = set()
    for sf in sorted(glob.glob(str(ROOT / "sessions" / "*" / "session.json"))):
        try:
            s = json.loads(Path(sf).read_text())
        except Exception:  # noqa: BLE001
            continue
        for r in s.get("recommendations", []) or []:
            if r.get("has_consensus") and r.get("organization_id"):
                ids.add(r["organization_id"])
    return ids


def main():
    data = json.loads((ROOT / "organizations.json").read_text())
    published = published_org_ids()
    broken_pub, broken_unpub = [], []
    print("=== Spendenlink-Canary ===")
    for o in data["organizations"]:
        url = o.get("donation_url")
        tag = "publiziert" if o["id"] in published else "nicht publ."
        if not url:
            print(f"  —       {o['id']} ({tag}): keine donation_url")
            continue
        status, code, detail = check(url)
        print(f"  {status:7} {o['id']} ({tag}): [{code}] {url}  {detail}")
        if status == "BROKEN":
            (broken_pub if o["id"] in published else broken_unpub).append(o["id"])
    print()
    if broken_unpub:
        print(f"WARN (nicht publiziert, kein Fail): {', '.join(broken_unpub)}")
    if broken_pub:
        print(f"BROKEN — PUBLIZIERTE Spendenwege defekt: {', '.join(broken_pub)}")
        sys.exit(1)
    print("Alle PUBLIZIERTEN Spendenwege OK/BLOCKED (BLOCKED = bot-gewallt, Sicht-Check).")


if __name__ == "__main__":
    main()
