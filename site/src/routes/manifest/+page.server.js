import { manifestHtml } from '$lib/server/content.js';

export function load() {
	return { manifest: manifestHtml() };
}
