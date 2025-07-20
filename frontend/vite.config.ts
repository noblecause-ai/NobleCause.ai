import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}'],
		environment: 'happy-dom',
		setupFiles: ['./src/setupTests.ts'],
		globals: true
	},
	define: {
		// Define globals for testing
		global: 'globalThis'
	}
});
