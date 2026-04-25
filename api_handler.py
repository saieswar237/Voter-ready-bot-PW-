import os
import google.generativeai as genai

def get_gemini_response(prompt):
    # This pulls the key from the Environment Variables we set in Cloud Run
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment."
        
    genai.configure(api_key=api_key)
    
    # FIXED: Upgraded to the currently active 2.5 model!
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"