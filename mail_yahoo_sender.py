import smtplib
import time

from secrets import *


def send_yahoo_mail(to_addr, subject, body): 
    from_email = EMAIL_YAHOO_SEND_ACCOUNT
    date = time.strftime("%m/%d/%Y")

    msg_1 = "From: %s" % from_email
    msg_2 = "To: %s" % to_addr
    msg_3 = "Subject: %s" % subject
    msg_4 = "Date: %s" % date
    msg_5 = "%s" % body

    msg = "%s\n%s\n%s\n%s\n\n%s" % (msg_1, msg_2, msg_3, msg_4, msg_5,)

    try :
        server = smtplib.SMTP("smtp.mail.yahoo.com",587)
        server.starttls()
        server.login(EMAIL_YAHOO_SEND_ACCOUNT, EMAIL_YAHOO_SEND_PASSWORD)
        server.sendmail(from_email, to_addr, msg)
        server.quit()
        print '* [YAHOO SENT]',
    except :
        print '* [YAHOO SENDING ERROR]',

