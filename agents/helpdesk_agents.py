# Helpdesk agents module
import random

# Small built-in knowledge base
KNOWLEDGE_BASE = {
    "vpn": (
        "Troubleshooting VPN Connection Issues:\n"
        "1. Check your local internet connection to ensure you are online.\n"
        "2. Verify VPN credentials and the server address are correct.\n"
        "3. Restart the VPN client and try reconnecting.\n"
        "4. If using a corporate network, verify you are not blocked by a local firewall."
    ),
    "password": (
        "Password Reset Procedures:\n"
        "1. Navigate to the login page and click 'Forgot Password'.\n"
        "2. Enter your registered email address.\n"
        "3. Follow the link in the password reset email received.\n"
        "4. Choose a new password meeting the complexity requirements (min 12 characters)."
    ),
    "database": (
        "Database Connection Issues:\n"
        "1. Check database server status to ensure it is running.\n"
        "2. Verify database connection string and network credentials.\n"
        "3. Check for any database locks or connection pool saturation.\n"
        "4. Review the database error logs for recent issues."
    )
}

def issue_analyzer_agent(issue: str):
    """
    Categorizes the issue and returns the category and priority.
    """
    issue_lower = issue.lower()
    if "vpn" in issue_lower or "network" in issue_lower or "wifi" in issue_lower or "internet" in issue_lower:
        category = "Network"
        priority = "High"
    elif "password" in issue_lower or "login" in issue_lower or "access" in issue_lower:
        category = "Access/Auth"
        priority = "Medium"
    elif "database" in issue_lower or "server" in issue_lower or "down" in issue_lower:
        category = "Infrastructure"
        priority = "Critical"
    else:
        category = "General"
        priority = "Low"
        
    return category, priority

def documentation_agent(issue: str):
    """
    Searches the small built-in knowledge base and returns troubleshooting documentation.
    """
    issue_lower = issue.lower()
    for key, doc in KNOWLEDGE_BASE.items():
        if key in issue_lower:
            return doc
    return "No specific troubleshooting documentation found for this issue."

def resolution_agent(issue: str, documentation: str):
    """
    Generates a resolution recommendation.
    """
    if "No specific troubleshooting documentation" in documentation:
        return (
            f"Unable to find standard resolution for issue: '{issue}'.\n"
            "Recommendation: Escalate to Tier 2 IT support for manual investigation."
        )
    return (
        f"Recommended Resolution Workflow for '{issue}':\n"
        f"{documentation}\n"
        "If the steps above do not resolve the issue, escalate to IT support."
    )

def ticket_agent(issue: str, priority: str, resolution: str):
    """
    Creates a ticket dictionary containing ticket_id, issue, priority, status, and resolution.
    """
    ticket_id = f"TCK-{random.randint(10000, 99999)}"
    return {
        "ticket_id": ticket_id,
        "issue": issue,
        "priority": priority,
        "status": "Open",
        "resolution": resolution
    }

def run_helpdesk_pipeline(issue: str):
    """
    Executes all agents sequentially and returns the final ticket.
    """
    # 1. Analyze issue
    category, priority = issue_analyzer_agent(issue)
    
    # 2. Get documentation
    documentation = documentation_agent(issue)
    
    # 3. Generate resolution recommendation
    resolution = resolution_agent(issue, documentation)
    
    # 4. Create and return ticket
    ticket = ticket_agent(issue, priority, resolution)
    return ticket

if __name__ == "__main__":
    sample_issue = "VPN not connecting"
    final_ticket = run_helpdesk_pipeline(sample_issue)
    
    # Pretty print the final ticket dict
    print("Final IT Helpdesk Ticket:")
    for key, value in final_ticket.items():
        print(f"{key}: {value}")
