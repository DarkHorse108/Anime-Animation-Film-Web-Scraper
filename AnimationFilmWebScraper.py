#############################################ABOUT Section####################################################################################################################################################################################################
#AUTHOR: JOHN SY
#EMAIL: sy.john.r@gmail.com
#PURPOSE: a webscraper that scrapes the Anime/Animation film listings of Consolidated Theatres of Hawaii's website and sends an sms text summary of each film and related information such as screening location and screening dates to the recipient.
#Please refer to the README for any additional information on proper use, updates, etc.
#LAST MODIFIED: September 6, 2019
#############################################LIBRARY/MODULES Section##########################################################################################################################################################################################

#Import requests to send a GET request to the website
import requests

#Import necessary methods, etc. from BeautifulSoup4 to parse contents of the GET request
from bs4 import BeautifulSoup

#import twilio SDK in order to send sms message from account-bound twilio phone number to recipient phone number
from twilio.rest import Client

#############################################VARIABLES Section#################################################################################################################################################################################################

#REPLACE account_sid value with your twilio account_sid as a string
account_sid = ""

#REPLACE auth_token value with your twilio auth_token as a string
auth_token = ""

#REPLACE sender_phone_number value with your twilio account phone number in E.164/International formatting as a string, i.e. for U.S. based numbers "+15556666666"
sender_phone_number = ""

#REPLACE recipient_phone_number value with your recipient's phone number in E.164/International formatting as a string, i.e. for U.S. based numbers "+15556666666"
recipient_phone_number = ""

#This is the specific page that is being parsed, in this case Consolidate Theatres of Hawaii's webpage listing upcoming movies from the Anime genre
website_url = "https://www.consolidatedtheatres.com/ward/showtimes-and-tickets/special-screen/anime/coming-soon"

#Create the GET request to the URL of interest, assign contents of the GET request to var website_request
website_request = requests.get(website_url)

#bool variable to determine whether or not there are films now or in the future based on the information within the website_url
#films_available is initialized to false and is only changed to true once it has been determined that there is at least
#one film available for ticket purchases listed in the website_url
films_available = False

#Create new global soup object using the html body content of the GET request from the URL of interest, and specify to parse it using html.parser that is part of the Python standard library
soup = BeautifulSoup(website_request.content, "html.parser")

#Take the beautiful soup object, which contains the html body of the website_url, and create a global list where each list element is an html element that matches the criteria of having class="film status-advance_tickets".
#This essentially takes all div html elements with this class, including each of their child elements, and packages them into a single index in a list pointed to by raw_film_metadata. You can think of each element
#in the raw_film_metadata as corresponding to a unique film listing and all of the unparsed information regarding it, such as its title, description, etc. Each element therefore represents a unique film listing. If there are
#for example, 3 elements in the raw_film_metadata list, then there are 3 films listed on the website_url of interest.
raw_film_metadata = soup.find_all(class_="film status-advance_tickets")

#if films are available/listed in the website_url of interest, filmdata will be a list in which each element is a dictionary object. Each dictionary object in the list will contain pertinent information
#regarding a single movie. Each dictionary object will have keys associated with the title, description, theatre location, and screening date values of a single film. For example, if
#the film "Pokemon" is showing, a dictionary object with the keys "title", "description", "location", and "dates", i.e. {"title":"Pokemon", "description":"A movie about fictional creatures", "location":"Consolidated Theatre Ward Ave.", "dates":["Thur, Sept 14", "Fri, Sept 15"]}
#will be added as an element of the list filmdata using the function extract_film_information() defined in the Function Definitions Section
filmdata = []

#############################################CONSTANTS Section#################################################################################################################################################################################################

#Newline constant used for formatting the string to be sent in the body of the text message to the recipient
NEWLINE = "\n"

#Tab constant used for formatting the string to be sent in the body of the text message to the recipient
TAB = "\t"

#The message string used in the body of the text message sent to recipient in the event that there are no films listed in the website_url of interest
NO_FILM_MESSAGE = "There are currently no films of interest listed."

#############################################FUNCTION Definitions Section#######################################################################################################################################################################################

#############################################################################################################################
#NAME: check_for_films()
#PURPOSE: check_for_films creates a list wherein each element is an h4 html element from website_url that matches the find_all("h4", class="name") criteria. Within any given h4 element in that list, the title of the films belongs to a child element of said h4 element.
#If that list contains no elements, then there are no available films within the website_url of interest.
#RECIEVES: None
#MODIFIES: local film_titles
#RETURNS: Boolean Value
#############################################################################################################################
def check_for_films():

	#createa a list where each element corresponds to an h4 html element that contains the name of a unique film
	film_titles = soup.find_all("h4", class_="name")

	#if the list of film names has zero elements, that means no films are available.
	if len(film_titles) == 0:
		return False

	else:
		return True

#END check_for_films()
#############################################################################################################################

#############################################################################################################################
#NAME: add_film()
#PURPOSE: Appends arguments passed to it as elements of the global list object filmdata 
#RECIEVES: Any valid object(s)
#MODIFIES: global filmdata, 
#		   local film
#RETURNS: None
#############################################################################################################################
def add_film(film):

	filmdata.append(film)

	return

#END add_film()
#############################################################################################################################

#############################################################################################################################
#NAME: extract_film_information()
#PURPOSE: Iterate over every unique film listing in the website_url of interest, and create a dictionary object corresponding to each film listing. Each dictionary object created will contain pertinent information
#regarding the film. Each dictionary object will have keys associated with the title, description, theatre screening location, and screening date values of each film. For example, if
#the film "Pokemon" is showing, a dictionary object with the keys "title", "description", "location", and "dates", is created with corresponding related value. Note that the dates key is associated with a list of values corresponding
#to multiple screening dates of the particular film, if applicable. Each dictionary object is added to the global list object filmdata, as an element of that list using the function add_film().
#i.e. {"title":"Pokemon", "description":"A movie about fictional creatures", "location":"Consolidated Theatre Ward Ave.", "dates":["Thur, Sept 14", "Fri, Sept 15"]}
#RECEIVES: None
#MODIFIES: global filmdata, 
#		   global raw_film_metadata, 
#		   local raw_film_dates, 
#RETURNS: None
#############################################################################################################################
def extract_film_information():

	#For each of the films listed in the website_url of interest, which corresponds to the number of elements in global list object raw_film_metadata, create a new local dictionary object called film.
	#Each film dictionary object will have the keys "title", "description", "location", and "dates". All values associated with each key are strings obtained by parsing for specific html elements
	#within the website_url of interest that is unique to that particular page, then extracting the string values by stripping away the html element tags of the html elements we are interested
	#in isolating. The exception to this rule is the key "dates", which instead of having a singular string value, instead is a list whose elements are strings, which correspond to the multiple
	#screening dates of the film if applicable.
	for i in range(0, len(raw_film_metadata)):
		
		film = {}

		#the follwing 3 lines create the keys "title" "description" and "location" and assigns string values to them
		film["title"] = raw_film_metadata[i].find(class_="name").get_text()
		film["description"] = raw_film_metadata[i].find(class_="desc").find_next("p").get_text()
		film["location"] = raw_film_metadata[i].find(class_="red").get_text()
		
		#create the key "dates", which is initialized with an empty list 
		film["dates"] = []
		
		#We parse the html "option" elements, which include the text for each film screening date, and create a list object called raw_film_dates where each element
		#corresponds to an html options element and its children that contains the flim screening date text
		raw_film_dates = raw_film_metadata[i].find("option").find_next_siblings()

		#Iterate over each "option" element collected in raw_film_dates, extract the string/text that explicitly states a screening date, and append it to the list
		#object corresponding to the "dates" key
		for j in range(0, len(raw_film_dates)):
			film["dates"].append(raw_film_dates[j].get_text())

		#Take the fully populated flim dictionary object and send it as an argument to add_film(), which will append the dictionary object to the global list object filmdata
		add_film(film)

	return
#END extract_film_information()
#############################################################################################################################

#############################################################################################################################
#NAME: text_film_information()
#PURPOSE: For each dictionary object element which corresponds to a film listing in the website_url of interest within the global list object filmdata, combine every string value associated
#with said dictionary object's keys into a singular string object. This singular string object which contains the title, description, screening location, and screening dates, is then sent
#as an argument to sms_information() to be texted to the recipient. Note that each film and its corresponding information will constitute a single text message. For example, if there are 2 films
#the recipient will receive 2 text messages in total, with each message containing the information regarding each unique film.
#RECEIVES: A list of dictionary objects
#MODIFIES: global filmdata, 
#		   local text_body_1, 
#		   local text_body_2,
#		   local complete_text_body
#RETURNS: None
#############################################################################################################################
def text_film_information(filmdata):

	# for each film listing, concatenate the strings corresponding to title, description, and screening location information, and assign the result to text_body_1
	for i in range(0, len(filmdata)):

		text_body_1 = NEWLINE + filmdata[i]["title"] + NEWLINE + filmdata[i]["description"] + NEWLINE + filmdata[i]["location"] + NEWLINE

		text_body_2 = ""

		complete_text_body = ""

		#the below for loop examines the value of the "dates" key of a particular film dictionary object, which should be a list object of strings.
		#We take each string in the list and concatenate it with TAB/whitespace for readability and assign it to another strinb object, text_body_2
		for j in range(0, len(filmdata[i]["dates"])):

			text_body_2 = text_body_2 + filmdata[i]["dates"][j] + TAB

		#the string values in string objects text_body_1 and text_body_2 are concatenated into a prettified string and assigned to string object compelte_text_body
		complete_text_body = text_body_1 + text_body_2

		#string object complete_text_body is then passed as an argument to sms_information() wherein the string is sms texted to the recipient
		sms_information(complete_text_body)

	return
#END text_film_information()
#############################################################################################################################

#############################################################################################################################
#NAME: sms_information()
#PURPOSE: Receives a string object and sends the string to the recipient associated with global string object sender_phone_number,
# from the phone number associated with the global string object recipient_phone_number. The algorithm was taken directly from
#twilio's library quickstart guide at https://www.twilio.com/docs/sms/quickstart/python#install-python-and-the-twilio-helper-library
#RECEVIES: A string object
#MODIFIES: local body
#		   local from_
#		   local to
#RETURNS: None
#############################################################################################################################
def sms_information(message):

	client = Client(account_sid, auth_token)

	message = client.messages \
                .create(
                     body= message,
                     from_= sender_phone_number,
                     to= recipient_phone_number
                 		)
#END sms_information()
#############################################################################################################################

#############################################################################################################################
#NAME: text_no_films_notification()
#PURPOSE: Passes string constant NO_FILM_MESSAGE as an argument to sms_information(), essentially sending the recpient an sms text message
#that there are no film listings in the website_url of interest
#RECEIVES: None
#MODIFIES: None
#RETURNS: None
#############################################################################################################################
def text_no_films_notification():

	sms_information(NO_FILM_MESSAGE)

	return

#END text_no_films_notification()
#############################################################################################################################

#############################################EXECUTABLE/MAIN Section#######################################################################################################################################################################################

if __name__ == "__main__":

	films_available = check_for_films()

	if films_available:
		
		extract_film_information()
		text_film_information(filmdata)

	else:

		text_no_films_notifcation()