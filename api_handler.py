import os
import logging
import google.generativeai as genai
from google.cloud import secretmanager

def get_gemini_response(prompt):
    api_key = None
    
    # SECURITY FLEX: Attempt to pull key from Google Secret Manager Vault
    try:
        client = secretmanager.SecretManagerServiceClient()
        # Your specific project ID from your earlier terminal logs
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "pw-war-494117") 
        name = f"projects/{project_id}/secrets/gemini-api-key/versions/latest"
        
        response = client.access_secret_version(request={"name": name})
        api_key = response.payload.data.decode("UTF-8")
        logging.info("Security: Key retrieved from Google Secret Manager.")
    except Exception as e:
        # SAFETY NET: If the vault isn't set up on GCP yet, fall back to environment variables safely
        logging.warning("Secret Manager unavailable, falling back to Environment Variables.")
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return "Error: API Key completely missing from all secure locations."

    # Initialize Gemini 2.5 Flash
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"