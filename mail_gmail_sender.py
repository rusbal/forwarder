import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
from secrets import *

 
def send_gmail_mail(to_addr, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ACCOUNT
    msg['To'] = to_addr
    msg['Subject'] = subject
     
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ACCOUNT, to_addr, text)
    server.quit()

