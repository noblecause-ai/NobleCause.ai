import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
export default {
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: null,
			strict: true
		}),
		prerender: {
			handleHttpError: 'fail',
			// /sessions/[id] has no pages as long as sessions/ is empty — that's fine.
			handleUnseenRoutes: 'ignore'
		}
	}
};
