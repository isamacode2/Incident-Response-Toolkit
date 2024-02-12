from prettytable import PrettyTable
import argparse
import re
import logging
# import smtplib
# from email.message import EmailMessage
import matplotlib.pyplot as plt
from collections import defaultdict

# Set up logging
logging.basicConfig(filename='log_parser.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

class LogParser:
    def __init__(self, log_file):
        self.log_file = log_file
        self.table = PrettyTable(field_names=["Timestamp", "Level", "Message"])  # Adjust field names as needed
        self.word_counts = defaultdict(int)

    def parse_line(self, line):
        try:
            match = re.findall(r'\b\w+\b', line)
            if match:
                return match
        except Exception as e:
            logging.error(f"Error parsing line: {e}")
            # send_email(f"Error parsing line: {e}")

    def parse_log(self):
        try:
            with open(self.log_file, 'r') as file:
                for line in file:
                    parsed_line = self.parse_line(line.strip())
                    if parsed_line:
                        self.handle_parsed_line(parsed_line)
        except IOError as e:
            logging.error(f"Error opening log file: {e}")
            # send_email(f"Error opening log file: {e}")

    def handle_parsed_line(self, parsed_line):
        try:
            self.table.add_row(parsed_line)
            for word in parsed_line:
                self.word_counts[word.lower()] += 1
        except Exception as e:
            logging.error(f"Error handling parsed_line: {e}")
            # send_email(f"Error handling parsed_line: {e}")

    def print_table(self):
        print(self.table)

    def visualize_data(self):
        try:
            words = list(self.word_counts.keys())
            counts = list(self.word_counts.values())
            plt.bar(words, counts)
            plt.xlabel('Word')
            plt.ylabel('Frequency')
            plt.title('Frequency of Words in Log File')
            plt.show()
        except Exception as e:
            logging.error(f"Error visualizing data: {e}")
            # send_email(f"Error visualizing data: {e}")

# def send_email(message):
#     # Replace with your email details
#     email = EmailMessage()
#     email['From'] = 'your-email@example.com'
#     email['To'] = 'your-email@example.com'
#     email['Subject'] = 'Log Parser Error'
#     email.set_content(message)

#     with smtplib.SMTP('smtp.example.com', 587) as smtp:
#         smtp.login('your-email@example.com', 'your-password')
#         smtp.send_message(email)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Parse a log file.')
    arg_parser.add_argument('logfile', help='The log file to parse.')
    args = arg_parser.parse_args()

    log_parser = LogParser(args.logfile)
    log_parser.parse_log()
    log_parser.print_table()
    log_parser.visualize_data()