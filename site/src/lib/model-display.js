// Anzeigenamen der Modelle für den (deutsch-only) Protokoll-Explorer — Company
// und Modellbezeichnung + Version. Eigennamen, sprachneutral; spiegelt die
// i18n-Maps `familyNames`/`modelNames`, die die Explorer-Routen nicht nutzen.
// Frühere Sitzungen haben andere Sitzinhaber (z. B. Claude Sonnet 4.5) — darum
// hier auch die historischen Modelle, mit Roh-Fallback auf Familie/Label.
const FAMILY = { anthropic: 'Anthropic', openai: 'OpenAI', google: 'Google' };

const MODEL = {
	'claude-opus-4-8': 'Claude Opus 4.8',
	'claude-sonnet-4-5': 'Claude Sonnet 4.5',
	'claude-opus-5': 'Claude Opus 5',
	'claude-fable-5': 'Claude Fable 5',
	'gpt-5.2': 'GPT-5.2',
	'gpt-5.6-sol': 'GPT-5.6 Sol',
	'gemini-2.5-pro': 'Gemini 2.5 Pro',
	'gemini-3.5-flash': 'Gemini 3.5 Flash',
	'gemini-3.7-flash': 'Gemini 3.7 Flash'
};

// Adresse (?modell=gpt) ↔ Modell. Schritt 2: adressierbare Filter als Links.
const SLUG = {
	'claude-opus-4-8': 'opus',
	'claude-sonnet-4-5': 'sonnet',
	'claude-opus-5': 'opus-5',
	'claude-fable-5': 'fable',
	'gpt-5.2': 'gpt',
	'gpt-5.6-sol': 'gpt-5-6-sol',
	'gemini-2.5-pro': 'gemini',
	'gemini-3.5-flash': 'gemini-3-5-flash',
	'gemini-3.7-flash': 'gemini-3-7-flash'
};

export const companyName = (family) => FAMILY[family] ?? family;
export const modelName = (model, fallback) => MODEL[model] ?? fallback ?? model;
export const modelSlug = (model) => SLUG[model] ?? model;
export const modelOfSlug = (slug) => Object.entries(SLUG).find(([, s]) => s === slug)?.[0] ?? slug;
