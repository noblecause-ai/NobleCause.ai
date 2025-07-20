import '@testing-library/jest-dom';

// Mock browser environment for Svelte 5
Object.defineProperty(globalThis, 'window', {
	value: globalThis,
	writable: true
});

Object.defineProperty(globalThis, 'document', {
	value: globalThis.document || {},
	writable: true
});

// Set up browser-like environment
if (typeof globalThis.requestAnimationFrame === 'undefined') {
	globalThis.requestAnimationFrame = (callback: FrameRequestCallback) => {
		return setTimeout(callback, 16);
	};
}

if (typeof globalThis.cancelAnimationFrame === 'undefined') {
	globalThis.cancelAnimationFrame = (id: number) => {
		clearTimeout(id);
	};
}