import { getAmfCase } from '$lib/server/amf.js';

export function load() {
	return { amf: getAmfCase() };
}
