import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

def send_bulk_emails(recipients, subject, from_name, body, attachments):
    smtp_server = "smtp.zoho.com"
    smtp_port = 587
    sender_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    successful_sends = 0
    unsuccessful_sends = 0
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        
        for recipient in recipients:
            try:
                message = MIMEMultipart()
                message["From"] = f"{from_name} <{sender_email}>"
                message["To"] = recipient
                message["Subject"] = subject
                
                message.attach(MIMEText(body, "plain"))
                
                # Handle attachments
                for attachment in attachments:
                    part = MIMEApplication(
                        attachment.getvalue(),
                        Name=attachment.name
                    )
                    part['Content-Disposition'] = f'attachment; filename="{attachment.name}"'
                    message.attach(part)
                
                server.send_message(message)
                successful_sends += 1
                
            except Exception as e:
                print(f"Error sending to {recipient}: {str(e)}")
                unsuccessful_sends +=1
                continue
                
        server.quit()
        return successful_sends, unsuccessful_sends
        
    except Exception as e:
        print(f"SMTP Error: {str(e)}")
        return successful_sends

def send_cc_email(recipients, subject, from_name, body, attachments):
    smtp_server = "smtp.zoho.com"
    smtp_port = 587
    sender_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        
        message = MIMEMultipart()
        message["From"] = f"{from_name} <{sender_email}>"
        message["To"] = recipients[0]  # First recipient in To field
        message["Cc"] = ", ".join(recipients[1:])  # Rest in CC
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "plain"))
        
        # Handle attachments
        for attachment in attachments:
            part = MIMEApplication(
                attachment.getvalue(),
                Name=attachment.name
            )
            part['Content-Disposition'] = f'attachment; filename="{attachment.name}"'
            message.attach(part)
        
        # Send to all recipients (including CC)
        server.send_message(message)
        server.quit()
        return True, ""
        
    except Exception as e:
        return False, str(e)