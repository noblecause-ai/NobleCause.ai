"""Web content fetching utility for Noble Cause Steward."""

import httpx


class WebAdapter:
    """Utility class for fetching web content."""

    def fetch(self, url: str, timeout: int = 30) -> str | None:
        """
        Fetch web content from the given URL.
        
        Args:
            url: The URL to fetch content from
            timeout: Request timeout in seconds (default: 30)
            
        Returns:
            The text content of the response, or None if an error occurred
        """
        try:
            response = httpx.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError:
            # HTTP error (4xx, 5xx status codes)
            return None
        except httpx.ConnectError:
            # Connection error (network unreachable, DNS failure, etc.)
            return None
        except httpx.TimeoutException:
            # Request timeout
            return None