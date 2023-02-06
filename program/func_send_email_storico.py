
import smtplib
import ssl

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
  # Define the transport variables
  ctx = ssl.create_default_context()
  password = "bhbvoftuqdowcoqq"    # Your app password goes here
  sender = "77bot77bot77@gmail.com"    # Your e-mail address
  receiver = "77bot77bot77@gmail.com" # Recipient's address

  # Create the message
  message = MIMEMultipart("mixed")
  message["Subject"] = "Hello Mixed Multipart World!"
  message["From"] = sender
  message["To"] = receiver

  # Attach message body content
  message.attach(MIMEText("Hello from Python", "plain"))

  # Attach image
  filename = 'storico.json'
  with open(filename, "rb") as f:
      file = MIMEApplication(f.read())
  disposition = f"attachment; filename={filename}"
  file.add_header("Content-Disposition", disposition)
  message.attach(file)

  # Connect with server and send the message
  with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
      server.login(sender, password)
      server.sendmail(sender, receiver, message.as_string())
  return      