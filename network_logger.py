import argparse
import logging
import smtplib
from email.message import EmailMessage
from scapy.all import *
from collections import Counter
import matplotlib.pyplot as plt

# Suppress Scapy warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set up logging
logging.basicConfig(filename='network_logger.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def packet_callback(packet):
    try:
        wrpcap(args.logfile, packet, append=True)  # append=True to add packets to the existing file
    except Exception as e:
        logging.error(f"Error writing to log file: {e}")
        send_email(f"Error writing to log file: {e}")

def parse_traffic(filename):
    try:
        packets = rdpcap(filename)
        parsed_data = []
        for packet in packets:
            data = {}
            if IP in packet:
                data['src_ip'] = packet[IP].src
                data['dst_ip'] = packet[IP].dst
                data['protocol'] = packet[IP].proto
            parsed_data.append(data)
        return parsed_data
    except Exception as e:
        logging.error(f"Error parsing traffic: {e}")
        send_email(f"Error parsing traffic: {e}")

def generate_report(parsed_data):
    try:
        src_ips = [data['src_ip'] for data in parsed_data if 'src_ip' in data]
        ip_counts = Counter(src_ips)
        
        # Print IP frequencies
        print("IP Address Frequency:")
        for ip, count in sorted(ip_counts.items(), key=lambda item: item[1], reverse=True):
            print(f"{ip}: {count}")
        
        # Plot IP frequencies
        ips = list(ip_counts.keys())
        counts = list(ip_counts.values())
        plt.bar(ips, counts)
        plt.xlabel('IP Address')
        plt.ylabel('Frequency')
        plt.title('IP Address Frequency')
        plt.show()
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        send_email(f"Error generating report: {e}")

def network_logger():
    try:
        sniff(prn=packet_callback, count=args.count, filter=args.filter, iface="en0")
        parsed_data = parse_traffic(args.logfile)
        generate_report(parsed_data)
        return args.logfile  # Return the log file path
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        send_email(f"An error occurred: {e}")

def send_email(message):
    # Replace with your email details
    email = EmailMessage()
    email['From'] = 'your-email@example.com'
    email['To'] = 'your-email@example.com'
    email['Subject'] = 'Network Logger Error'
    email.set_content(message)

    with smtplib.SMTP('smtp.example.com', 587) as smtp:
        smtp.login('your-email@example.com', 'your-password')
        smtp.send_message(email)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network packet logger.')
    parser.add_argument('--count', type=int, default=1000, help='Number of packets to capture.')
    parser.add_argument('--filter', type=str, default=None, help='Packet filter.')
    parser.add_argument('--logfile', type=str, default='network.log', help='Log file to write to.')
    args = parser.parse_args()

    logfile = network_logger()  # Capture the returned log file path
    print(f"Log file: {logfile}")