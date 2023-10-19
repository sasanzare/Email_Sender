import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter
from tkinter import messagebox
from tkinter import ttk
import time

# Function to send emails
def send_emails():
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

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.connect(smtp, port)  # Establish the connection
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

    # Close the SMTP server connection and destroy the progress window
    server.quit()
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

# Call the send_emails function
send_emails()