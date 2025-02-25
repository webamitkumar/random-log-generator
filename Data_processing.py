import pandas as pd
import random
import logging
import string
import numpy as np
import matplotlib.pyplot as plt
import os


# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_log_entry():
    """Generate a random log entry."""
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    action = random.choice(['login', 'logout', 'view', 'edit', 'delete'])
    user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{timestamp} - {log_level} - {action} - user: {user}"


def write_logs_to_file(log_filename, num_entries=100):
    """Write random logs to a file."""
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                file.write(log + '\n')
        print(f"Logs have been successfully written to {log_filename}")
    except Exception as e:
        logging.error(f"Error in write_logs_to_file function: {e}")
        print(f"An error occurred while writing logs to the file.")


def load_and_process_logs(log_filename="generated_logs.txt"):
    """Load and process logs from a file."""
    try:
        if not os.path.exists(log_filename):
            print(f"File {log_filename} does not exist.")
            return None

        df = pd.read_csv(
            log_filename,
            sep=' - ',
            header=None,
            names=['timestamp', 'log_level', 'action', 'user'],
            engine='python'
        )

        # Clean and trim spaces around the timestamp
        df['timestamp'] = df['timestamp'].str.strip()

        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # Drop rows with invalid timestamps
        df = df.dropna(subset=['timestamp'])

        if df.empty:
            print("No valid data found in the log file.")
            return None
        else:
            print("Data loaded and processed successfully.")
            print(df.head())

        # Set the timestamp column as the index for time-based operations
        df.set_index('timestamp', inplace=True)

        return df
    except Exception as e:
        print(f"Error processing log file: {e}")
        return None


def analyze_data(df):
    """Perform basic statistical analysis on the logs."""
    try:
        if df is None or df.empty:
            print("No data to analyze")
            return None, None

        # Count the occurrence of each log level and action
        log_level_counts = df['log_level'].value_counts()
        action_counts = df['action'].value_counts()

        log_count = len(df)                # Total number of logs
        unique_users = df['user'].nunique()  # Number of unique users
        logs_per_day = df.resample('D').size()  # Logs per day

        # Average and max logs per day
        average_logs_per_day = logs_per_day.mean()
        max_logs_per_day = logs_per_day.max()

        # Display summary statistics
        print("\nLog Level Counts:\n", log_level_counts)
        print("\nAction Counts:\n", action_counts)
        print(f"\nTotal Number of Logs: {log_count}")
        print(f"\nNumber of Unique Users: {unique_users}")
        print(f"\nAverage Logs per Day: {average_logs_per_day:.2f}")
        print(f"\nMax Logs per Day: {max_logs_per_day}")

        # Create a dictionary of the analysis results
        stats = {
            "log_level_counts": log_level_counts.to_dict(),
            "action_counts": action_counts.to_dict(),
            "log_count": log_count,
            "unique_users": unique_users,
            "average_logs_per_day": average_logs_per_day,
            "max_logs_per_day": max_logs_per_day
        }
        return stats
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return None


def visualize_trends(df):
    """Visualize trends over time using matplotlib."""
    try:
        logs_by_day = df.resample('D').size()

        # Plot log frequency over time using matplotlib
        plt.figure(figsize=(10, 5))
        plt.plot(logs_by_day.index, logs_by_day.values, marker='o', linestyle='-', color='b')

        plt.title("Log Frequency Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Logs")
        plt.xticks(rotation=45)
        plt.grid()

        # Show the plot
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error visualizing data: {e}")


# Main script execution
log_filename = "generated_logs.txt"  # Assumes this file does not exist initially

# Step 1: Write random logs to the file
write_logs_to_file(log_filename, num_entries=200)

# Step 2: Load and process the logs from the file
df_logs = load_and_process_logs(log_filename)

# Step 3: Perform basic analysis on the logs data
if df_logs is not None:
    stats = analyze_data(df_logs)

    # Step 4: Visualize trends over time
    visualize_trends(df_logs)
