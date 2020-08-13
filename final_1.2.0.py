""" 
written by : Umair  Abbas

 project name : final
 version           : 1.2.0
 requirments  : requests, bs4
 Starting date : this project started in 2019 Nov..
 Stage.             : starting 
 
 	
Note:
	this program will fech your record from your tuf portal 
	for preesents and absents and show you here you just
	need to enter your cordentials.
	
Important :
	if you can improve it you are most welcome ,
	there is lots of things that can be implement to this project.
	this project started as hobbiest side projectcfor fun.
	i hope you can improve it... 

"""

from requests import post, HTTPError, ConnectionError
from bs4 import BeautifulSoup
from subprocess import call


#global variables
survey = False
subject =False


#function handling request and soup
def sending_req(url, values):
    try:
    	#sending post request to site
    	req = post(url, data=values)
    	req.raise_for_status()
    	web = req.content
    	
    	#making soup for parasing using bs4
    	soup = BeautifulSoup(web, features="html.parser")
    	
    	#storing main contents in variables
    	sub = soup.find_all("td", {"class":"atnd-sub"})
    	table = soup.find_all("tbody")
    	FECH = 1+len(sub)*2
    	
    	sur  = soup.find_all("div", {"class":"result"})
    	global survey, subject
    	if sur:
    		survey = True
    	if sub:
    		subject = True
    	#-------------------------------------------important variables--------------------------------------------------
    	
    	#all subject
    	raw_subject = [i.text for i in sub]
    	subject = [i for i in raw_subject]
    	
    	#total days
    	raw_total = [i.contents[j].find_all("span", {"class":"stat-round total"})[0].text for i in table for j in range(1,FECH,2)]
    	total = [i.replace(' ', '').strip() for i in raw_total]
    	
    	#presrent days
    	raw_present = [i.contents[j].find_all("span", {"class":"stat-round present"})[0].text for i in table for j in range(1,FECH,2)]
    	present = [i.replace(' ', '').strip() for i in raw_present]
    	
    	#absent days
    	raw_absent = [i.contents[j].find_all("span", {"class":"stat-round absent"})[0].text for i in table for j in range(1,FECH,2)]
    	absent = [i.replace(' ', '').strip() for i in raw_absent]
    	
    	#percentage of total presents
    	raw_percent = [i.contents[j].find_all("span", {"class":"stat-round per"})[0].text for i in table for j in range(1,FECH,2)]
    	percent = [i.replace(' ', '').strip() for i in raw_percent]
    	
    	
    	
    	#printing  the result to the console
    	for (a, b, c,d,e) in zip(subject, total, present, absent, percent):
    		print('\n{0} : {1}---{2}---{3}---{4}\n'.format(a, b, c, d, e))
    	return True
    	
    except HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
        e.response.status_code))
        
    except ConnectionError:
        print("No internet connection available.")
    return False


#main loop 
while True:
	# getting values from user 
	user = input(" \nEnter your user name : ")
	pas  = input(" Enter your password   : ")
	
	#storing link and cordentials  in variable 
	url = 'http://tufportal.com/Login/check_user'
	values = {'username': user,'password': pas}

	#clearing the console
	call(["clear"])
	#storing content which is returend    
	yes = sending_req(url, values)
		
	if survey and not subject:
		print(" \ngo to your portal and fill up the survey ")
	
	if  not subject and not survey:
			if yes is True:
				print('\nplease check your  username or password , \nor visit tufportal')
