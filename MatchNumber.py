'''

@author: yu
'''
from bs4 import BeautifulSoup
import requests
import re
import csv

def get_match_number(link):
    numbers = []
    while not numbers:
    
        source_code = requests.get(link)
        soup = BeautifulSoup(source_code.text,"html.parser")
        numbers = soup.findAll(text = re.compile("场"))
    
    return numbers[0]
def get_recent_match_number(link,pageNumber):
    number = 0
    link = link[:-1] + str(pageNumber)
    print(link)
    trytime = 0
    while number == 0:
        trytime += 1
        source_code = requests.get(link)
        soup = BeautifulSoup(source_code.text,"html.parser")
        numberInMonth = len(soup.findAll(text = re.compile("天前|时前")))
        numberOther = soup.findAll(text = re.compile("月前"))
        print(numberOther)
        number += numberInMonth
        if len(numberOther) == 0:
            pageNumber = pageNumber+1
            number += int(get_recent_match_number(link,pageNumber))
        return number
time = 1
started = False
print(str(time) + "st time try" )
while not started:

    with open('MatchNumber.csv','w+') as csvFile:
        fieldNames = ["ID" , "MatchNumber"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()
        teamList = ["IG","LGD","VG","EHOME","CDEC","OG","Alliance","EG","MVP","Secret","coL","Liquid","Newbee","Archon"]
        pro_players_url = "http://dotamax.com/player/pro/"
        url_dict = dict()
        source_code = requests.get(pro_players_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        if not soup.findAll(text = re.compile("504 Gateway Time-out")):
            started = True
        else:
            time+=1
        for player in soup.findAll("tr"):
            linkdata = player.find("a")
            namedata = player.find("div")
            names = namedata.findAll(text = re.compile("   "))
            names = " ".join(names).split()
            name = "".join(names)
            href = linkdata.get("href")
            link = "http://dotamax.com" + href
            
            if name.split('.')[0] in teamList:
                match_link = link.replace("detail","match") + "/?skill=vh&hero=-1&p=" + str(1)
                number = get_recent_match_number(match_link,1)
                writer.writerow({'ID' : name , 'MatchNumber' : number})
                print (name + "  "  +  str(number))
        

    
   


    
