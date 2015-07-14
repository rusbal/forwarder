"""
Settings
"""

IS_VERBOSE = False
PROGRAMMERS_TEST = False # False means LIVE

SMTP_PROVIDER = "gmail" # Used for sending emails

TIMESTAMP_FILE = "last_fetch_timestamp.log"
EMAIL_LIMIT = 0
EMAIL_FOLDER = "INBOX" 

"""
Kidsplus
"""
EMAIL_KIDSPLUS_SUBJECT = "Anmeldeformular auf der Internetseite"
if PROGRAMMERS_TEST:
    EMAIL_KIDSPLUS_RECIPIENTS = ["raymond@philippinedev.com"]
else:
    EMAIL_KIDSPLUS_RECIPIENTS = ["raymond@philippinedev.com", "info@kidsplus.ch", "tanji@gmx.ch", "ps@gedec.org"]

"""
Erlenbach
"""
EMAIL_ERLENBACH_SUBJECT = "Erlenbach: Anmeldeformular auf der Internetseite"
if PROGRAMMERS_TEST:
    EMAIL_ERLENBACH_RECIPIENTS = ["raymond@philippinedev.com"]
else:
    EMAIL_ERLENBACH_RECIPIENTS = ["raymond@philippinedev.com", "info.erlenbach@kidsplus.ch"]

