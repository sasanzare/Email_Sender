import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter
from tkinter import messagebox
from tkinter import ttk
import time
import socket

# Function to show and close the message connection
def show_message_connection():
    messagebox.showinfo("Internet Connection", "Waiting for internet connection...")
    root.after(3000, root.destroy)

# Function to check internet connectivity
def check_internet():
    try:
        # Check if a connection to a well-known host can be established
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

# Function to send emails
def send_emails():
    # Wait for internet connectivity
    while not check_internet():
        # Display a message or progress indicator indicating waiting for internet connection
        show_message_connection()
        time.sleep(5)
    # Read the subject from the subject.txt file
    with open("subject.txt", "r") as subject_file:
        text_subject = subject_file.readline().strip()

    # Read the content from the index.html file
    with open("index.html", "r") as file:
        text_content = file.read()

    # Read the recipient emails from the emails.txt file
    with open('emails.txt', 'r') as file:
        recipients = [line.strip() for line in file.readlines()]

    # Extract sender email and password
    sender_email = recipients.pop(0)
    sender_password = recipients.pop(0)

    # SMTP server and port
    smtp = 'smtp.gmail.com'
    port = 587

    email_sent = False

    while not email_sent:
        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(smtp, port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Total number of recipients
            total_recipients = len(recipients)

            # Create a progress window using tkinter
            progress = tkinter.Tk()
            progress.title("Email Progress")
            progress.geometry("400x100")

            # Label to display the progress
            progress_label = tkinter.Label(progress, text="Sending Emails: 0/{0}".format(total_recipients))
            progress_label.pack()

            # Progress bar to visualize the progress
            progress_bar = ttk.Progressbar(progress, length=300, mode="determinate", maximum=total_recipients)
            progress_bar.pack()

            # List to store invalid email addresses
            invalid_emails = []

            # Loop through each recipient and send the email
            for index, recipient_email in enumerate(recipients, 1):
                try:
                    # Create the email message
                    message = MIMEMultipart()
                    message['From'] = sender_email
                    message['To'] = recipient_email
                    message['Subject'] = text_subject
                    message.attach(MIMEText(text_content, 'html'))

                    # Convert the message to string and send the email
                    text = message.as_string()
                    server.sendmail(sender_email, recipient_email, text)

                    # Update the progress label and bar
                    progress_label.config(text="Sending Emails: {0}/{1}".format(index, total_recipients))
                    progress_bar['value'] = index
                    progress.update()

                    # Wait for 1 minute after sending every 50 emails
                    if index % 50 == 0:
                        time.sleep(60)

                except Exception as e:
                    # Handle exceptions and store invalid email addresses
                    print(f"Failed to send email to {recipient_email}. Error: {str(e)}")
                    invalid_emails.append(recipient_email)

            # Close the progress window
            progress.destroy()

            # Calculate the success count
            success_count = total_recipients - len(invalid_emails)

            # Show appropriate message boxes based on the result
            if invalid_emails:
                error_message = "Failed to send emails to the following recipients:\n\n"
                error_message += "\n".join(invalid_emails)
                messagebox.showerror("Email Sending Error", error_message)
            else:
                messagebox.showinfo("Email Sent", "All emails sent successfully.")

            messagebox.showinfo("Email Summary", f"Total Emails: {total_recipients}\nSuccessfully Sent: {success_count}")

            # Close the SMTP server connection
            server.quit()

            email_sent = True

        except smtplib.SMTPException as e:
            # Handle SMTP exceptions
            print(f"SMTPException occurred: {str(e)}")
            server.quit()

        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {str(e)}")
            server.quit()

        # Wait for some time before reattempting to send emails
        time.sleep(5)


# Call the send_emails function
send_emails()