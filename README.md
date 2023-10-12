#Email Sending Script
This script is designed to send emails to multiple recipients using the Gmail SMTP server. It reads the subject, content, and recipient email addresses from separate text files and sends personalized emails to each recipient.

##Prerequisites
    .Python 3.x
    .Tkinter library (usually included with Python installations)
    .Gmail account with less secure apps access enabled (for sending emails)

##Installation

1.Clone the repository or download the script files to your local machine.

2.Install the required dependencies by running the following command:

pip install -r requirements.txt

##Usage

1.Prepare the email content:

    .Create an HTML file named index.html containing the email content in HTML format. You can use placeholders like {{recipient_name}} in the HTML file, which will be replaced with actual values.
    .Create a text file named subject.txt and enter the subject line for the email.

2.Prepare the recipient list:

    .Create a text file named emails.txt and enter the email addresses of the recipients, one per line. The first line should be the sender's email address, and the second line should be the sender's email password.
    .It is recommended to use a separate Gmail account for sending emails and enable "less secure apps" access for that account.

3.Run the script:

    .Execute the script by running the following command in the terminal:

        python send_emails.py

4.Progress and result:

    .During the email sending process, a progress window will appear, showing the number of emails sent out of the total number of recipients.
    .After the script finishes sending emails, a summary message box will display the total number of emails and the number of emails sent successfully.
    .If any emails fail to send, an error message box will display the list of recipients whose emails failed to send.

##License
    This project is licensed under the MIT License. See the LICENSE file for details.

##Acknowledgments
    .The script utilizes the following libraries:
        .smtplib for establishing an SMTP connection and sending emails.
        .email.mime modules for creating and formatting email messages.
        .tkinter for creating the progress window and message boxes.
        .tkinter.ttk for the progress bar widget.
