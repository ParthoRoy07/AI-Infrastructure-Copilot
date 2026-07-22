import json
from agents.log_agent import analyze_log

# Define the sample log content for testing
sample_log = """ERROR: Database connection failed
Timeout after 30 seconds
Connection refused"""

if __name__ == "__main__":
    print("Analyzing sample log via Log Agent...\n")
    print(f"--- Log Input ---\n{sample_log}\n-----------------\n")
    
    # Perform analysis using the Log Agent
    analysis_result = analyze_log(sample_log)
    
    # Format and print the resulting dictionary nicely
    print("--- Analysis Result ---")
    print(json.dumps(analysis_result, indent=4))
