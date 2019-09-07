README for AnimationFilmWebScraper.py

#AUTHOR: JOHN SY
#EMAIL: sy.john.r@gmail.com
#PURPOSE: a webscraper that scrapes the Anime/Animation genre film listings of Consolidated Theatres of Hawaii's website and sends an sms text summary of each film and related information such as screening location and screening dates to the recipient.
#If the URL being scraped is modified or no longer exists, feel free to email me and let me know.
#As of September 6, 2019, I am beginning as a second year Computer Science student at Oregon State University. I am currently self-studying Python, though I have prior experience in IA-32 Assembly, C, C++, HTML/CSS, and JavaScript.
#This script is strictly as a personal project in order to exercise my recently acquired Python knowledge. As of this point I have not learned Python classes and objects yet (though I am familiar with OOP concepts and use in C++),
#Which is why direct definition and instantiation of classes/objects is not practiced here, even if it may be more appropriate to addressing the functions of this script. This script will be updated at a later time as my knowledge in Python grows.
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
