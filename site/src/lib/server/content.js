import fs from 'node:fs';
import path from 'node:path';
import { md } from '../markdown.js';
export { md } from '../markdown.js';

// Repo root: the site lives in <repo>/site, content in <repo>/manifest.md and <repo>/sessions.
const ROOT = path.resolve(process.cwd(), '..');

// --- Rekord-Text sicher rendern (Sanitizing-Auflage, Opus-5-Auftrag 2026-08-01) ---
//
// Der gerenderte Markdown-Text stammt aus Modellantworten und Web-Recherche des Warts
// und landet per {@html} im Browser eines Besuchers unter unserer Domain. „Build-time"
// macht die Quelle unveränderlich, nicht vertrauenswürdig. Deshalb wird hier ausschließlich
// das neutralisiert, was ausführbar ankommt — der WORTLAUT bleibt vollständig erhalten
// (escapen statt entfernen; kein still kürzender Sanitizer, der die Datennaht verletzen würde).
//
// Diese eine Stelle ist der einzige Markdown-Pfad des Frontends: manifestHtml() und md()
// speisen jede {@html}-Senke (Sitzungen, Journal, Archiv, Manifest, DE und EN).

export function manifestHtml() {
	const source = fs.readFileSync(path.join(ROOT, 'manifest.md'), 'utf8');
	return md(source);
}


export function listSessions() {
	const dir = path.join(ROOT, 'sessions');
	if (!fs.existsSync(dir)) return [];
	return fs
		.readdirSync(dir, { withFileTypes: true })
		.filter((e) => e.isDirectory())
		.map((e) => {
			const file = path.join(dir, e.name, 'session.json');
			if (!fs.existsSync(file)) return null;
			const s = JSON.parse(fs.readFileSync(file, 'utf8'));
			return {
				id: s.id ?? e.name,
				number: s.number,
				date: s.date,
				title: s.title,
				question: s.question,
				total_eur: s.costs?.total ?? null
			};
		})
		.filter(Boolean)
		// Nach Sitzungsnummer absteigend (deterministisch); Datum nur als Fallback.
		// Die drei Sitzungen teilen dasselbe Datum — ein reiner Datums-Vergleich
		// wäre nicht eindeutig und die „jüngste" Sitzung zufällig.
		.sort((a, b) => (b.number ?? 0) - (a.number ?? 0) || (a.date < b.date ? 1 : -1));
}

export function getSession(id) {
	const file = path.join(ROOT, 'sessions', id, 'session.json');
	return JSON.parse(fs.readFileSync(file, 'utf8'));
}

export function getSessionEvents(id) {
	return JSON.parse(fs.readFileSync(path.join(ROOT, 'sessions', id, 'events.json'), 'utf8'));
}

export function getSessionResearch(id) {
	return JSON.parse(fs.readFileSync(path.join(ROOT, 'sessions', id, 'research.json'), 'utf8'));
}

export function getOrganizations() {
	const file = path.join(ROOT, 'organizations.json');
	return JSON.parse(fs.readFileSync(file, 'utf8'));
}

// Medaillon-Register (models.json, Repo-Root): je Modell die Selbstdarstellung
// (Motiv/Begründung/Person) und das Medaillon-Asset. Der Explorer hängt sie an
// die Voten (Konzept §4 — Motiv/Begründung „eine Ebene unter dem Medaillon").
// Rückgabe als Map model → Eintrag; fehlt die Datei, leere Map (kein Wurf).
export function getModelsRegistry() {
	const file = path.join(ROOT, 'models.json');
	if (!fs.existsSync(file)) return new Map();
	const data = JSON.parse(fs.readFileSync(file, 'utf8'));
	return new Map((data.models ?? []).map((entry) => [entry.model, entry]));
}

export function getAllSessions() {
	return listSessions().map((item) => getSession(item.id));
}

export function getLatestSession() {
	const sessions = listSessions();
	if (sessions.length === 0) return null;
	return getSession(sessions[0].id);
}

export function getSchedule() {
	const file = path.join(ROOT, 'schedule.json');
	if (!fs.existsSync(file)) return null;
	return JSON.parse(fs.readFileSync(file, 'utf8'));
}

export function listJournalEntries() {
	const dir = path.join(ROOT, 'journal');
	if (!fs.existsSync(dir)) return [];
	return fs
		.readdirSync(dir, { withFileTypes: true })
		.filter((e) => e.isDirectory() && /^\d{4}-\d{2}-\d{2}(?:[a-z]|-[a-z0-9-]+)?$/.test(e.name))
		.map((e) => {
			const file = path.join(dir, e.name, 'entry.json');
			if (!fs.existsSync(file)) return null;
			const j = JSON.parse(fs.readFileSync(file, 'utf8'));
			return {
				id: e.name,
				date: j.date ?? e.name,
				convene: j.convene ?? null,
				convene_rationale: j.convene_rationale ?? null,
				kind: j.kind ?? null,
				refusal: j.refusal === true,
				refusal_note: j.refusal_note ?? null,
				session_ref: j.session_ref ?? null,
				model: j.model ?? null,
				model_label: j.model_label ?? null,
				type: j.type ?? null,
				commission_ref: j.commission_ref ?? null,
				deputation: Boolean(j.deputation_note),
				findings_count: (j.findings ?? []).length,
				queries_count: (j.search_queries ?? []).length,
				cost_eur: j.costs?.total ?? null
			};
		})
		.filter(Boolean)
		.sort((a, b) => (a.date < b.date ? 1 : -1));
}

export function getJournalEntry(id) {
	const file = path.join(ROOT, 'journal', id, 'entry.json');
	return JSON.parse(fs.readFileSync(file, 'utf8'));
}

// Bestell-Kommission (commissions/<date>/commission.json). ref wie
// "/commissions/2026-07-27/". Fehlt sie, null (kein Wurf).
export function getCommission(ref) {
	const name = (ref ?? '').replace(/^\/?commissions\//, '').replace(/\/$/, '');
	if (!name) return null;
	const file = path.join(ROOT, 'commissions', name, 'commission.json');
	if (!fs.existsSync(file)) return null;
	const record = JSON.parse(fs.readFileSync(file, 'utf8'));
	const reorderFile = path.join(ROOT, 'commissions', name, 'reorders.json');
	const completionFile = path.join(ROOT, 'commissions', name, 'completion.json');
	return { ...record,
		completion: fs.existsSync(completionFile) ? JSON.parse(fs.readFileSync(completionFile, 'utf8')) : null,
		reorders: fs.existsSync(reorderFile) ? JSON.parse(fs.readFileSync(reorderFile, 'utf8')) : [] };
}
