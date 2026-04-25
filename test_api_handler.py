import pytest
from unittest.mock import patch, MagicMock
from api_handler import get_gemini_response

# Mock a successful response object from the new genai SDK
class MockResponse:
    def __init__(self, text):
        self.text = text

def test_get_gemini_response_success():
    """Test that a normal API call returns the expected text."""
    with patch('api_handler.genai.Client') as MockClient:
        # Set up the mock client to return a predefined response
        mock_instance = MockClient.return_value
        mock_instance.models.generate_content.return_value = MockResponse("Mocked voting info.")
        
        result = get_gemini_response("Tell me about voting.")
        
        assert result == "Mocked voting info."
        # Verify the model was called with the correct parameters
        mock_instance.models.generate_content.assert_called_once_with(
            model='gemini-flash-latest',
            contents="Tell me about voting."
        )

def test_get_gemini_response_missing_api_key():
    """Test edge case where API key is missing."""
    with patch('api_handler.os.getenv', return_value=None):
        result = get_gemini_response("Hello")
        assert "System Error: API Key not found" in result

def test_get_gemini_response_503_retry_success():
    """Test that the bot retries on a 503 error and succeeds on the second try."""
    with patch('api_handler.genai.Client') as MockClient:
        mock_instance = MockClient.return_value
        
        # Make the first call raise a 503, and the second call succeed
        mock_instance.models.generate_content.side_effect = [
            Exception("503 UNAVAILABLE"),
            MockResponse("Recovered response.")
        ]
        
        # Patch time.sleep so the test runs instantly instead of waiting 2 seconds
        with patch('api_handler.time.sleep'):
            result = get_gemini_response("Hello")
            
        assert result == "Recovered response."
        assert mock_instance.models.generate_content.call_count == 2