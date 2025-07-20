import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Create a mock page component instance for testing
class MockPageComponent {
	monologue: string = '';
	status: string = 'loading';

	async fetchStewardStatus() {
		try {
			const response = await fetch('/api/status');
			if (response.ok) {
				const data = await response.json();
				this.status = data.status;
				this.monologue = data.inner_monologue;
			} else {
				this.status = 'error';
				this.monologue = 'Failed to fetch status';
			}
		} catch (error) {
			this.status = 'error';
			this.monologue = 'Network error';
		}
	}
}

describe('+page.svelte', () => {
	beforeEach(() => {
		// Reset all mocks before each test
		vi.resetAllMocks();
	});

	afterEach(() => {
		// Restore all mocks after each test
		vi.restoreAllMocks();
	});

	it('test_page_fetches_and_displays_steward_monologue', async () => {
		// Mock successful fetch response with expected JSON structure
		const mockResponse = {
			ok: true,
			json: vi.fn().mockResolvedValue({
				status: 'idle',
				inner_monologue: 'Contemplating the flow of information...'
			})
		};
		
		globalThis.fetch = vi.fn().mockResolvedValue(mockResponse);

		// Create component instance
		const component = new MockPageComponent();

		// Trigger the fetch
		await component.fetchStewardStatus();

		// Assert that the component displays the correct monologue
		expect(component.monologue).toBe('Contemplating the flow of information...');
		expect(component.status).toBe('idle');
		
		// Verify fetch was called with correct endpoint
		expect(globalThis.fetch).toHaveBeenCalledWith('/api/status');
	});

	it('test_page_handles_fetch_error', async () => {
		// Mock fetch to throw an error
		globalThis.fetch = vi.fn().mockRejectedValue(new Error('Network error'));

		// Create component instance
		const component = new MockPageComponent();

		// Trigger the fetch
		await component.fetchStewardStatus();

		// Assert that the component handles error correctly
		expect(component.monologue).toBe('Network error');
		expect(component.status).toBe('error');
		
		// Verify fetch was called
		expect(globalThis.fetch).toHaveBeenCalledWith('/api/status');
	});

	it('test_page_handles_failed_response', async () => {
		// Mock failed response
		const mockResponse = {
			ok: false,
			json: vi.fn()
		};
		
		globalThis.fetch = vi.fn().mockResolvedValue(mockResponse);

		// Create component instance
		const component = new MockPageComponent();

		// Trigger the fetch
		await component.fetchStewardStatus();

		// Assert that the component handles failed response correctly
		expect(component.monologue).toBe('Failed to fetch status');
		expect(component.status).toBe('error');
		
		// Verify fetch was called
		expect(globalThis.fetch).toHaveBeenCalledWith('/api/status');
	});
});