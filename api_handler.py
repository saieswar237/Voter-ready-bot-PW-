import os
from dotenv import load_dotenv
# THE CORRECT IMPORT FOR THE NEW SDK
from google import genai

# Force Python to read the .env file immediately
load_dotenv()

import time

def get_gemini_response(prompt_text):
    """
    Sends the user's input to Gemini using the new SDK and returns the response.
    Includes a retry mechanism for 503 High Demand errors.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "System Error: API Key not found. Please check your .env file."

    try:
        # Initialize the new Client
        client = genai.Client(api_key=api_key)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Use the stable gemini-flash-latest model
                response = client.models.generate_content(
                    model='gemini-flash-latest',
                    contents=prompt_text,
                )
                return response.text
            except Exception as e:
                error_str = str(e)
                # If it's a 503 High Demand error, wait and retry
                if "503" in error_str or "UNAVAILABLE" in error_str:
                    if attempt < max_retries - 1:
                        time.sleep(2)  # Wait 2 seconds before retrying
                        continue
                # If it's a different error or we ran out of retries, return the error
                return f"API Error: {error_str}"
            
    except Exception as e:
        return f"System Error: {str(e)}"