import time
import sys
import logging
from collections import defaultdict

# Set up logging
logging.basicConfig(filename='server_logger.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def tail(file):
    print("Starting to tail file")  # Add this line
    file.seek(0, 2)  # Go to the end of the file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)  # Sleep briefly
            continue
        print(f"Read line: {line}")  # Print the line to the console
        yield line

def process_line(line):
    try:
        # Parse the line to extract the relevant fields
        fields = line.split()
        timestamp = fields[0]
        source_ip = fields[1]
        dest_ip = fields[2]
        protocol = fields[3]
        status_code = fields[4]

        # Log the extracted information
        logging.info(f"Timestamp: {timestamp}, Source IP: {source_ip}, Destination IP: {dest_ip}, Protocol: {protocol}, Status Code: {status_code}")

        # Check for security-relevant events
        if status_code == "404":
            logging.warning(f"Possible security incident detected: {line}")

    except Exception as e:
        logging.error(f"Error processing line: {e}")

def monitor_logfile(filepath):
    print(f"Opening log file: {filepath}")  # Add this line
    try:
        with open(filepath, 'r') as file:
            loglines = tail(file)
            for line in loglines:
                process_line(line)
    except Exception as e:
        logging.error(f"Error monitoring log file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server_monitor.py <logfile>")
        sys.exit(1)
    logfile = sys.argv[1]
    monitor_logfile(logfile)