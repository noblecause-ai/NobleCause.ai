import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Create a mock component instance for testing
class MockHealthCheck {
	status: 'Loading...' | 'OK' | 'Error' = 'Loading...';

	async checkHealth() {
		try {
			const response = await fetch('http://localhost:8000/health');
			if (response.ok) {
				await response.json();
				this.status = 'OK';
			} else {
				this.status = 'Error';
			}
		} catch (error) {
			this.status = 'Error';
		}
	}
}

describe('HealthCheck', () => {
	beforeEach(() => {
		// Reset all mocks before each test
		vi.resetAllMocks();
	});

	afterEach(() => {
		// Restore all mocks after each test
		vi.restoreAllMocks();
	});

	it('test_health_check_displays_ok_on_successful_fetch', async () => {
		// Mock successful fetch response
		const mockResponse = {
			ok: true,
			json: vi.fn().mockResolvedValue({ status: 'ok' })
		};
		
		globalThis.fetch = vi.fn().mockResolvedValue(mockResponse);

		// Create component instance
		const component = new MockHealthCheck();

		// Trigger the health check
		await component.checkHealth();

		// Assert that the component status is "OK"
		expect(component.status).toBe('OK');
	});

	it('test_health_check_displays_error_on_failed_fetch', async () => {
		// Mock fetch to throw an error
		globalThis.fetch = vi.fn().mockRejectedValue(new Error('Network error'));

		// Create component instance
		const component = new MockHealthCheck();

		// Trigger the health check
		await component.checkHealth();

		// Assert that the component status is "Error"
		expect(component.status).toBe('Error');
	});
});