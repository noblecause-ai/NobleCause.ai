import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		fs: {
			// Build reads manifest.md and sessions/ from the repo root.
			allow: ['..']
		}
	}
});
