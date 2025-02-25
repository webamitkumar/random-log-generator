                       #new one  by own 
import pandas as pd
import random
import logging
import string
import sqlite3
import os
from datetime import datetime

# Configure logging for errors
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection setup
DB_FILE = "logs.db"

def setup_database():
    """Create a database table for storing logs."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                log_level TEXT,
                action TEXT,
                user TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("Database setup complete.")
    except Exception as e:
        logging.error(f"Error setting up the database: {e}")
        print(f"Error setting up the database: {e}")

def generate_log_entry():
    """Generate a random log entry."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    action = random.choice(['login', 'logout', 'view', 'edit', 'delete'])
    user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return timestamp, log_level, action, user

def write_log_to_database(timestamp, log_level, action, user):
    """Insert a log entry into the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (timestamp, log_level, action, user)
            VALUES (?, ?, ?, ?)
        """, (timestamp, log_level, action, user))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error writing log to database: {e}")
        print(f"Error writing log to database: {e}")

def write_logs_to_file_and_db(log_filename, num_entries=100):
    """Generate logs and write them to both a file and the database."""
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                timestamp, log_level, action, user = generate_log_entry()
                log_entry = f"{timestamp} - {log_level} - {action} - user: {user}"
                
                # Write to file
                file.write(log_entry + '\n')
                
                # Write to database
                write_log_to_database(timestamp, log_level, action, user)
                
        print(f"Logs have been successfully written to {log_filename} and the database.")
    except Exception as e:
        logging.error(f"Error writing logs to file and database: {e}")
        print(f"Error writing logs to file and database: {e}")

def view_logs_from_database():
    """Fetch and display logs from the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs")
        rows = cursor.fetchall()
        conn.close()
        
        print("\nLogs from Database:")
        for row in rows:
            print(row)
    except Exception as e:
        logging.error(f"Error fetching logs from database: {e}")
        print(f"Error fetching logs from database: {e}")

# Main Script Execution
if __name__ == "__main__":
    log_filename = "generated_logs.txt"
    
    # Step 1: Setup database
    setup_database()
    
    # Step 2: Generate logs and store in file and database
    write_logs_to_file_and_db(log_filename, num_entries=200)
    
    # Step 3: View logs from database (optional)
    view_logs_from_database()
