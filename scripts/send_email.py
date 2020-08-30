import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

port = 465 
smtp_server = "smtp.gmail.com"
sender_email = "healthdeclarations@gmail.com"
password = "health1234"
body = ""

def send_email(name, receiver_email, bcc_email, file_name): 
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "הצהרת בריאות" + " " + name + "-" + date.today().strftime("%d/%m/%Y")
    message["Bcc"] = bcc_email

    message.attach(MIMEText(body, "plain"))

    with open(file_name, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_name}",
    )

    message.attach(part)
    text = message.as_string()
  
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
