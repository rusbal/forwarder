#!/usr/bin/python
#
# Very basic example of using Python and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# RKI July 2013
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
# import os
import sys
import imaplib
import getpass
import email
import email.header
import datetime

from mail_gmx_sender import send_gmx_mail
from mail_gmail_sender import send_gmail_mail
from mail_yahoo_sender import send_yahoo_mail

from secrets import *
from settings import *
 

"""
Helper functions
"""
def save_last_timestamp(timestamp):
    f = open(TIMESTAMP_FILE, 'w')
    f.write(str(timestamp))
    f.close()
    if IS_VERBOSE:
        print "\nSaved timestamp:", timestamp

def read_last_timestamp():
    try:
        with open (TIMESTAMP_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def process_email(num, data, last_timestamp):
    global process_count, is_timestamp_logged

    msg = email.message_from_string(data[0][1])
    decode = email.header.decode_header(msg['Subject'])[0]
    subject = unicode(decode[0])

    # Now convert to local date-time
    date_tuple = email.utils.parsedate_tz(msg['Date'])
    local_date = None
    email_timestamp = 0

    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        email_timestamp = int(local_date.strftime("%s"))

        if email_timestamp <= last_timestamp:
            if IS_VERBOSE:
                print "Skipped: %s [ %s ]" % (num, email_timestamp,)
            email_timestamp = 0
        else: 
            if not is_timestamp_logged:
                is_timestamp_logged = True
                save_last_timestamp(email_timestamp)

            if subject == EMAIL_KIDSPLUS_SUBJECT:
                print_email("kidsplus", num, subject, msg['Date'], msg.get_payload())
                process_count += 1
            elif subject == EMAIL_ERLENBACH_SUBJECT:
                print_email("erlenbach", num, subject, msg['Date'], msg.get_payload())
                process_count += 1
            else:
                print "-"

    return email_timestamp

def print_email(campus, num, subject, raw_date, body):
    if campus == "kidsplus":
        for recipient in EMAIL_KIDSPLUS_RECIPIENTS:
            send_email(recipient, subject, body)

    elif campus == "erlenbach":
        for recipient in EMAIL_ERLENBACH_RECIPIENTS:
            send_email(recipient, subject, body)

    print '* %s (%s): %s' % (num, raw_date, subject)

def send_email(recipient, subject, body):
    if SMTP_PROVIDER == "gmx":
        send_gmx_mail(recipient, subject, body)
    elif SMTP_PROVIDER == "gmail":
        send_gmail_mail(recipient, subject, body)
    elif SMTP_PROVIDER == "yahoo":
        send_yahoo_mail(recipient, subject, body)

def process_mailbox(M):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """
 
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    last_timestamp = read_last_timestamp()

    for num in data[0].split()[::-1]:
        rv, data = M.fetch(num, '(RFC822)')
        if rv == 'OK':
            timestamp = process_email(num, data, last_timestamp) 
            if timestamp == 0:
                break
        else:
            print "ERROR getting message", num
            return

        if EMAIL_LIMIT and process_count >= EMAIL_LIMIT:
            break
    return timestamp
 
 
"""
Execution starts here
"""
M = imaplib.IMAP4_SSL('imap.gmail.com')
 
try:
    rv, data = M.login(EMAIL_GMAIL_FETCH_ACCOUNT, EMAIL_GMAIL_FETCH_PASSWORD)
except imaplib.IMAP4.error:
    print "ERROR: Gmail login failed"
    sys.exit(1)
 
if IS_VERBOSE:
    print rv, data
 
rv, mailboxes = M.list()
if rv == 'OK':
    if IS_VERBOSE:
        print "Mailboxes:"
        print mailboxes
 
rv, data = M.select(EMAIL_FOLDER)
if rv != 'OK':
    print "ERROR: Unable to open mailbox ", rv
    quit()


"""
Start processing
"""
if IS_VERBOSE:
    print "Processing mailbox...\n"

process_count = 0
is_timestamp_logged = False

timestamp = process_mailbox(M)

M.close() 
M.logout()
 
if process_count == 0:
    if not IS_VERBOSE:
        print "### REPORT"
        print "New:", process_count
else:
    print
    print "### REPORT"
    print "New:", process_count

