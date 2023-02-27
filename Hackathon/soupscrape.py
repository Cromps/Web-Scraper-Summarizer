import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Link to the Firestore Database
cred = credentials.Certificate(r"C:\Users\ayaan\OneDrive\Documents\Programming\mymoney-c54ad-firebase-adminsdk-i3h55-448eb274ff.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
#API url
urld = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-text/"

def transfer_data():
        #Get the user input
        prompt = input("Enter in keywords: ")
        #Find all sites related to user input
        sitelist = [str(sites) for sites in search(prompt, tld = "co.in", num = 5, stop = 5, pause = 3)]
        #Getting the text from the sites
        for i in range(0,5):
            url = sitelist[i]
            r = requests.get(url)
            c = r.content
            allitems = BeautifulSoup(c, "html.parser")
            title = allitems.find_all('title')
            soup = allitems.find_all("p")
            #Join all paragraphs in list into one string
            alltext = [paragraph.text for paragraph in soup]
            alltext = " ".join(alltext) 
            #Transfer data to the database
            data = {
                'paragraphInfo': alltext
            }
            db.collection('websiteInfo').document(title[0].text).set(data)
            payload = {
                "text": alltext,
                "min_length": 100,
                "max_length": 300
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "688f887998msh0a0e545e95d6e23p1c8aacjsn2997104127bd",
                "X-RapidAPI-Host": "tldrthis.p.rapidapi.com"
            }

            response = requests.request("POST", urld, json=payload, headers=headers)
            print(response.text)

transfer_data()