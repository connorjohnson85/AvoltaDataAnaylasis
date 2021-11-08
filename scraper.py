import requests
from bs4 import BeautifulSoup
import csv
from obituary import Obituary

baseUrl = "https://appalachianfuneralservices.com"
url = "https://appalachianfuneralservices.com/tribute/all-services/index.html"
links = []
response = requests.get(url)
obituaries = []
soup = BeautifulSoup(response.text, 'html.parser')
response.close()
names = soup.findAll('h2', attrs={"class":"deceased-name"})
datesOfDeaths = soup.findAll('div', attrs={'class': "deceased-date-of-death"})
condolences = []

    
for obit in names:
    newObituary = Obituary()
    newObituary.name = obit.text.strip()
    obituaries.append(newObituary)
    

for i in range(len(datesOfDeaths)):
    obituaries[i].dateOfDeath = str(datesOfDeaths[i]).split("span")[1][1:-2]

    
obituaryLinks = soup.findAll('div', attrs={"class":"deceased-image"})
for link in obituaryLinks: 
    links.append(str(link).split("href=\"")[1].split(" ")[0])

for i in range(len(links)):
    newResponse = requests.get(baseUrl+links[i])
    newSoup = BeautifulSoup(newResponse.text, 'html.parser')
    newResponse.close()
    lol = newSoup.find('div', attrs={"class":"obituary-text"})
    obituaries[i].obituary = lol.text
    splitLink = links[i].split("/")
    imageLink = str(newSoup.find("img", attrs={"alt": splitLink[4].replace("-", " ")})).split("src=\"")
    obituaries[i].images.append(baseUrl + imageLink[1][0: -3])
    condolences.append(newSoup.findAll("a", attrs={"class":"tribute-store-btn add-memory-btn"}))

for i in range(len(condolences)):
    newResponse = requests.get(baseUrl+str(condolences[i]).split("href=\"")[1].split("\"")[0])
    newSoup = BeautifulSoup(newResponse.text, 'html.parser')
    newResponse.close()
    divs = newSoup.findAll("div", attrs={"class":"tribute-message-wrapper"})
    for condolence in divs:
        if (str(condolence).split(">")[2] != "</span"):
                if (str(condolence).split(">")[2].split("<")[0] != ''):
                    obituaries[i].condolences.append(str(condolence).split(">")[2].split("<")[0])


with open("test.csv", 'w', encoding="utf-8") as csv_file:
    wr = csv.writer(csv_file, delimiter=',')
    for cdr in obituaries:
        wr.writerow(list(cdr))  # @Shankar suggestion