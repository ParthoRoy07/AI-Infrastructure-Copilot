import os
import sqlite3

# Define the default database file path.
# It is located in the same directory as this script.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'copilot.db')

def create_database(db_path=DB_PATH):
    """
    Creates the SQLite database and initializes the 'incidents' and 'tickets' tables
    if they do not already exist.
    
    Args:
        db_path (str): The file path to the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the 'incidents' table
    # Schema:
    #   - id: Auto-incrementing primary key
    #   - log_content: Text of the logs describing the incident
    #   - severity: Severity level of the incident (e.g., LOW, MEDIUM, HIGH, CRITICAL)
    #   - root_cause: Identified cause of the incident
    #   - resolution: Description of how the incident was resolved
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_content TEXT NOT NULL,
            severity TEXT,
            root_cause TEXT,
            resolution TEXT
        )
    ''')
    
    # Create the 'tickets' table
    # Schema:
    #   - ticket_id: Auto-incrementing primary key
    #   - issue: Description of the issue reported in the ticket
    #   - priority: Priority level of the ticket (e.g., P0, P1, P2, P3)
    #   - resolution: Steps taken or proposed to resolve the ticket
    #   - status: Current status of the ticket (e.g., OPEN, IN_PROGRESS, CLOSED)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT NOT NULL,
            priority TEXT,
            resolution TEXT,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_incident(log_content, severity, root_cause, resolution, db_path=DB_PATH):
    """
    Inserts a new incident record into the 'incidents' table.
    
    Args:
        log_content (str): The log content associated with the incident.
        severity (str): The severity level of the incident.
        root_cause (str): The root cause of the incident.
        resolution (str): The resolution details for the incident.
        db_path (str): The file path to the SQLite database.
        
    Returns:
        int: The auto-generated ID of the inserted incident record.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO incidents (log_content, severity, root_cause, resolution)
        VALUES (?, ?, ?, ?)
    ''', (log_content, severity, root_cause, resolution))
    
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def insert_ticket(issue, priority, resolution, status, db_path=DB_PATH):
    """
    Inserts a new ticket record into the 'tickets' table.
    
    Args:
        issue (str): The description of the issue.
        priority (str): The priority level of the ticket.
        resolution (str): The resolution details.
        status (str): The current status of the ticket.
        db_path (str): The file path to the SQLite database.
        
    Returns:
        int: The auto-generated ticket_id of the inserted ticket record.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tickets (issue, priority, resolution, status)
        VALUES (?, ?, ?, ?)
    ''', (issue, priority, resolution, status))
    
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_all_incidents(db_path=DB_PATH):
    """
    Retrieves all incident records from the database.
    
    Args:
        db_path (str): The file path to the SQLite database.
        
    Returns:
        list of dict: A list of dictionaries representing the incident records.
                      Each dictionary has keys: 'id', 'log_content', 'severity',
                      'root_cause', and 'resolution'.
    """
    conn = sqlite3.connect(db_path)
    # Use Row row_factory to easily convert rows to dictionaries.
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, log_content, severity, root_cause, resolution FROM incidents')
    rows = cursor.fetchall()
    
    incidents = [dict(row) for row in rows]
    conn.close()
    return incidents

def get_all_tickets(db_path=DB_PATH):
    """
    Retrieves all ticket records from the database.
    
    Args:
        db_path (str): The file path to the SQLite database.
        
    Returns:
        list of dict: A list of dictionaries representing the ticket records.
                      Each dictionary has keys: 'ticket_id', 'issue', 'priority',
                      'resolution', and 'status'.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT ticket_id, issue, priority, resolution, status FROM tickets')
    rows = cursor.fetchall()
    
    tickets = [dict(row) for row in rows]
    conn.close()
    return tickets

if __name__ == "__main__":
    create_database()
    print("Database initialized successfully.")
