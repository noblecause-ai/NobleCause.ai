# Verfahren: Host-Key-Pinning für den Deploy-Pfad — und was noch offen ist

**Von:** Leitstand · **Datum:** 2026-08-02 · **Schliesst:** Gate-Zeile 3, Befund P8.2
**Betrifft:** `deploy.yml` in `noblecause-ai/NobleCause.ai` · VPS `185.143.100.222` (`ov-29e4ac`)

---

## 1 · Zwei Schlüsselpaare, die leicht verwechselt werden

| | Was es beweist | Wo es liegt | Name hier |
|---|---|---|---|
| **Client-Key** | dass der Aufrufer eintreten darf | privat beim Client, öffentlich in `authorized_keys` auf dem Server | `aion-vps-key` (Bitwarden), `VPS_SSH_KEY` (GitHub-Secret) |
| **Host-Key** | dass der Server der richtige ist | privat auf dem Server unter `/etc/ssh/ssh_host_*_key`, öffentlich in `known_hosts` beim Client | **`VPS_KNOWN_HOSTS`** |

Der Fingerprint im bestehenden Bitwarden-Eintrag `aion-vps-key` gehört zum **Client**-Schlüssel. Er
taugt nicht als Vergleichswert für den Host-Key. Ein Vergleich dagegen prüfte etwas gegen sich
selbst und sähe wie eine Verifikation aus.

---

## 2 · Normal gegen gehärtet

**Normal:** Der Runner weist sich mit dem Deploy-Key aus, der Server prüft ihn. In die Gegenrichtung
nimmt der Runner per `ssh-keyscan` hin, was das Netz auf die Adresse antwortet. Das entspricht TLS
ohne Zertifikatsprüfung: ein verschlüsselter Kanal zu irgendwem.

**Gehärtet:** Der Host-Key kommt aus einem einmal an der Quelle verifizierten Wert. Präsentiert die
Gegenstelle einen anderen, verweigert SSH. Dazu ein Preflight: fehlt das Secret, bricht der Lauf ab,
statt still auf den Keyscan zurückzufallen.

**Was das konkret verhindert:** Antwortet während des Deploys jemand anderes für diese Adresse,
nimmt er den rsync entgegen und meldet Erfolg. Der echte Server bekommt die Auslieferung nie, der
Lauf ist grün, die Seite bleibt alt, niemand erfährt es. Derselbe Fehlermodus wie beim toten
Wacht-Benachrichtigungspfad: etwas sieht aus wie Erfolg und ist keiner.

**Was es nicht schützt:** einen kompromittierten Server, einen abgeflossenen Deploy-Key, GitHub
selbst. Es schliesst genau eine Lücke, die Vortäuschung des Servers auf dem Netzweg.

---

## 3 · Das Verfahren, wie es durchgeführt wurde

Der Wert der Prüfung liegt darin, dass die beiden Seiten über **verschiedene Wege** kommen. Ein
Vergleich zweier Werte aus derselben Quelle belegt nichts.

**Auf dem VPS, lokal an der Quelle** — kein SSH, kein `sudo`, `.pub` ist lesbar:

```bash
for f in /etc/ssh/ssh_host_*_key.pub; do ssh-keygen -lf "$f"; done
```

**Auf dem Mac, über das Netz von aussen:**

```bash
ssh-keyscan -t rsa,ecdsa,ed25519 185.143.100.222 > ~/nc_known_hosts.txt
ssh-keygen -lf ~/nc_known_hosts.txt
```

**Vergleich** der `SHA256:`-Werte je Schlüsseltyp. Die Kommentare unterscheiden sich erwartungsgemäss
(`root@ov-29e4ac` gegen die IP) und sind nicht Teil des Vergleichs.

**Setzen, ebenfalls vom Mac:**

```bash
gh secret set VPS_KNOWN_HOSTS --repo noblecause-ai/NobleCause.ai < ~/nc_known_hosts.txt
gh secret list --repo noblecause-ai/NobleCause.ai
rm ~/nc_known_hosts.txt
```

### Ein Stolperstein, der real aufgetreten ist

Der erste Versuch lief mit `ssh -i ~/.ssh/aion_vps_key ubuntu@185.143.100.222 …` **auf dem VPS
selbst**. Dort gibt es den Client-Key nicht, die Verbindung scheiterte mit
`Permission denied (publickey)`.

Die Auflösung ist nicht, den Key dorthin zu kopieren, sondern die Erkenntnis, dass auf der Maschine
kein SSH nötig ist: wer auf dem Server steht, liest die Datei direkt. Das ist zugleich der
**stärkere** Anker. Der ursprünglich vorgeschlagene Weg über SSH stützte sich auf einen bestehenden
`known_hosts`-Eintrag des Macs und war damit leicht zirkulär. Der lokale Lesevorgang ist es nicht.

---

## 4 · Das Ergebnis

Alle drei Fingerprints stimmten überein, inklusive Schlüssellängen:

| Typ | SHA256 |
|---|---|
| RSA 3072 | `JnZzkMn6Q2CFI/bYXt0hLZW27OY/6XlAYvYvZlD1ffo` |
| ECDSA 256 | `1+Njy7zOtpMDqffN9Ab8og8kkHXHO5WeNShOhF+BIIA` |
| ED25519 256 | `QQu/txHGcc20Qw+R+uipROc8kD1OTiljo8w8ElT+068` |

`VPS_KNOWN_HOSTS` ist gesetzt und in `gh secret list` bestätigt.

**Diese Fingerprints stehen hier absichtlich.** Sie sind öffentliche Werte; sie zu notieren gibt
niemandem etwas, was er nicht durch eine Verbindung selbst erhielte. Umgekehrt sind sie der Anker
für jede spätere Prüfung und für den Sweep aus Abschnitt 5. Sie gehören nicht entfernt.

**Zusätzlich in Bitwarden ablegen**, als **eigener** Eintrag neben `aion-vps-key`, nicht darin. Wird
der Server je neu aufgesetzt, ändern sich die Host-Keys, der Deploy bricht laut ab, und dann muss
niemand das Verfahren neu herleiten.

---

## 5 · Was offen bleibt: drei Repos mit demselben Mangel

Die Härtung war kein Nachziehen einer bestehenden Praxis. NobleCause ist der **erste** gehärtete
Deploy-Pfad:

| Repo | Stand |
|---|---|
| `noblecause-ai/NobleCause.ai` | gepinnt, mit Preflight |
| `aion-lumen/aion-lumen.com` | `ssh-keyscan -H 185.143.100.222` blind |
| `AfshinMirhamed/carta` | `ssh-keyscan -H 185.143.100.222` blind |
| `AfshinMirhamed/Frag-Shifu` | `ssh-keyscan -H ${{ secrets.VPS_HOST }}` blind |

Alle vier zeigen auf dieselbe Maschine, der verifizierte Wert aus Abschnitt 4 trägt für alle.

**Bewusst nicht jetzt.** Jedes Repo braucht eine eigene Workflow-Änderung und einen eigenen Push;
drei davon anzufassen, während der NobleCause-Deploy im Anflug ist, wäre Scope-Mixing. Der Vorgang
gehört in den 0.4.0-Strang und lässt sich mit dem aion-lumen-Cache-Doppelmangel zusammenlegen
(Unterseiten ohne `Cache-Control`, endungsbasierter Asset-Matcher) — dieselben Sites, dieselbe
Sitzung.
