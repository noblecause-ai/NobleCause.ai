import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';

// Repo root: the site lives in <repo>/site, content in <repo>/manifest.md and <repo>/sessions.
const ROOT = path.resolve(process.cwd(), '..');

export function manifestHtml() {
	const md = fs.readFileSync(path.join(ROOT, 'manifest.md'), 'utf8');
	return marked.parse(md);
}

export function md(text) {
	return marked.parse(text ?? '');
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
		.sort((a, b) => (a.date < b.date ? 1 : -1));
}

export function getSession(id) {
	const file = path.join(ROOT, 'sessions', id, 'session.json');
	return JSON.parse(fs.readFileSync(file, 'utf8'));
}
