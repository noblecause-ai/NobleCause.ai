// Anzeigenamen der Modelle für den (deutsch-only) Protokoll-Explorer — Company
// und Modellbezeichnung + Version. Eigennamen, sprachneutral; spiegelt die
// i18n-Maps `familyNames`/`modelNames`, die die Explorer-Routen nicht nutzen.
// Frühere Sitzungen haben andere Sitzinhaber (z. B. Claude Sonnet 4.5) — darum
// hier auch die historischen Modelle, mit Roh-Fallback auf Familie/Label.
const FAMILY = { anthropic: 'Anthropic', openai: 'OpenAI', google: 'Google' };

const MODEL = {
	'claude-opus-4-8': 'Claude Opus 4.8',
	'claude-sonnet-4-5': 'Claude Sonnet 4.5',
	'gpt-5.2': 'GPT-5.2',
	'gemini-2.5-pro': 'Gemini 2.5 Pro'
};

// Adresse (?modell=gpt) ↔ Modell. Schritt 2: adressierbare Filter als Links.
const SLUG = {
	'claude-opus-4-8': 'opus',
	'claude-sonnet-4-5': 'sonnet',
	'gpt-5.2': 'gpt',
	'gemini-2.5-pro': 'gemini'
};

export const companyName = (family) => FAMILY[family] ?? family;
export const modelName = (model, fallback) => MODEL[model] ?? fallback ?? model;
export const modelSlug = (model) => SLUG[model] ?? model;
export const modelOfSlug = (slug) => Object.entries(SLUG).find(([, s]) => s === slug)?.[0] ?? slug;
