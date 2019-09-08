README for AnimationFilmWebScraper.py

#AUTHOR: JOHN SY
#EMAIL: sy.john.r@gmail.com
#PURPOSE: a webscraper that scrapes the Anime/Animation genre film listings of Consolidated Theatres of Hawaii's website and sends an sms text summary of each film and related information such as screening location and screening dates to the recipient.
#If the URL being scraped is modified or no longer exists, feel free to email me and let me know. This script is an exercise in Python programming and is primarily for personal entertainment and practice. 
#LAST MODIFIED: September 6, 2019

#This script was written in Python 3.7

#This script requires the following libraries to be installed: 
# requests
# twilio
# beautifulsoup4

#Documentation for used libraries can be found:
# https://www.twilio.com/docs/sms/quickstart/python#install-python-and-the-twilio-helper-library
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

#Services Paid or Otherwise you must register for to use this script:
# a paid or trial twilio account and phone number with twilio is required to utilize the sms feature of this script

#In the variables section, you will need to supply the values of the following variables, which are associated with your unique twilio account and (sending/sender) phone number, in addition to the recipient's phone number. All values should be entered as strings, with all phone numbers formated in E.164 international formatting:
#account_sid
#auth_token
#sender_phone_number
#recipient_phone_number
