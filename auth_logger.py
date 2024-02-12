import logging
# import smtplib
# from email.message import EmailMessage
import matplotlib.pyplot as plt
from collections import defaultdict

# Set up logging
logging.basicConfig(filename='authentication.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def log_attempt(username, success):
    try:
        if success:
            logging.info(f"Successful login attempt: {username}")
            login_attempts['successful'] += 1
        else:
            logging.info(f"Failed login attempt: {username}")
            login_attempts['failed'] += 1
    except Exception as e:
        logging.error(f"Error logging attempt: {e}")
        # send_email(f"Error logging attempt: {e}")

def authenticate(username, password):
    try:
        # Replace this with your actual authentication logic
        if username == 'admin' and password == 'password':
            log_attempt(username, True)
            return True
        else:
            log_attempt(username, False)
            return False
    except Exception as e:
        logging.error(f"Error authenticating: {e}")
        # send_email(f"Error authenticating: {e}")

def visualize_data(login_attempts):
    try:
        labels = list(login_attempts.keys())
        counts = list(login_attempts.values())
        plt.bar(labels, counts)
        plt.xlabel('Login Attempt Result')
        plt.ylabel('Number of Attempts')
        plt.title('Number of Successful and Failed Login Attempts')
        plt.show()
    except Exception as e:
        logging.error(f"Error visualizing data: {e}")
        # send_email(f"Error visualizing data: {e}")

# def send_email(message):
#     # Replace with your email details
#     email = EmailMessage()
#     email['From'] = 'your-email@example.com'
#     email['To'] = 'your-email@example.com'
#     email['Subject'] = 'Authentication Logger Error'
#     email.set_content(message)

#     with smtplib.SMTP('smtp.example.com', 587) as smtp:
#         smtp.login('your-email@example.com', 'your-password')
#         smtp.send_message(email)

if __name__ == "__main__":
    login_attempts = defaultdict(int)
    # Test the authentication function
    authenticate('admin', 'password')
    authenticate('admin', 'wrongpassword')
    visualize_data(login_attempts)