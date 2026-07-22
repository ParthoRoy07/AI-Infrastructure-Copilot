import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Gemini API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

# Initialize and configure the non-deprecated google-genai Client
if api_key:
    print("API key loaded successfully")
    client = genai.Client(api_key=api_key)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables.")
    client = None

def analyze_log(log_content):
    """
    Analyzes system log content using Gemini to extract the issue description, 
    severity, root cause, and proposed resolution.
    
    Args:
        log_content (str): The raw log data to analyze.
        
    Returns:
        dict: A dictionary containing keys: 'issue', 'severity', 'root_cause', and 'resolution'.
    """
    # Define a safe fallback response if API request or parsing fails
    fallback_result = {
        "issue": "Unknown or unparsed log issue",
        "severity": "UNKNOWN",
        "root_cause": "Could not identify root cause from log content.",
        "resolution": "Check the log manually or monitor system behavior."
    }
    
    # Check if the Gemini client has been initialized
    if not client:
        print("Error: Gemini client is not initialized due to missing API key.")
        return fallback_result
        
    try:
        # Prompt instructing Gemini to analyze the log and output structured JSON
        prompt = f"""
You are an advanced AI Infrastructure Copilot. Analyze the following system log:

---
{log_content}
---

Identify the issue, determine its severity (e.g., LOW, MEDIUM, HIGH, CRITICAL), locate the root cause, and propose a resolution.
You must return your response in JSON matching this exact structure:
{{
    "issue": "string description",
    "severity": "string severity",
    "root_cause": "string root cause",
    "resolution": "string resolution"
}}
"""
        # Call the non-deprecated google-genai Client using the gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # Verify that we got a valid response body
        if not response or not response.text:
            return fallback_result
            
        # Parse the JSON response
        parsed_data = json.loads(response.text.strip())
        
        # Ensure all expected keys exist in the returned dictionary
        for key in ["issue", "severity", "root_cause", "resolution"]:
            if key not in parsed_data:
                parsed_data[key] = fallback_result[key]
                
        return parsed_data
        
    except Exception as e:
        print(f"Error during log analysis: {e}")
        return fallback_result
