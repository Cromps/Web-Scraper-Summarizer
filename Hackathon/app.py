from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from googlesearch import search
import json
import requests

app = Flask(__name__)
urld = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-text/"

@app.route("/", methods = ['POST', 'GET'])
def webpage():
    link = ''
    data = ''
    prompt = ''
    if request.method == 'POST':
        prompt = request.form['inputform']
        sitelist = [str(sites) for sites in search(prompt, tld = "co.in", num = 1, stop = 1, pause = 3)]
        #Getting the text from the sites
        for i in range(0,1):
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
            payload = {
                "text": alltext,
                "min_length": 100,
                "max_length": 300
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "c1df1cd5c1msh9856464570022a9p1a8e75jsn48f43ad8d5d7",
                "X-RapidAPI-Host": "tldrthis.p.rapidapi.com"
            }

            response = requests.request("POST", urld, json=payload, headers=headers)
            data = data + response.text
            #Clean the response string
            data = data.replace('{', '')
            data = data.replace('}', '')
            data = data.replace('"', '')
            data = data.replace("summary", "Summary")
            link = link + url
    return render_template("soupscrape.html", link = link, data = data)



if __name__ == '__main__':
    app.debug = True
    app.run()