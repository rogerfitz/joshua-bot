import requests
from bs4 import BeautifulSoup as Soup

LINES={"MERCHANDISE MART": "40460","SOUTHPORT": "40360"}
base="http://www.transitchicago.com/traintracker/arrivaltimes.aspx?sid="

def requestTrainSchedule(line):
    line=line.upper()
    soup=Soup(requests.get(base+LINES[line]).text,"html.parser")
    return parseTrainHTML(soup)


def parseTrainHTML(soup):
    tracker_div=soup.find("div",{"id":"ctl06_upTrainTracker"})
    train_divs=tracker_div.find_all("div",{"class": "ttar_arrivalbar_brown"})
    response_str=""
    for train_div in train_divs:
        dest=train_div.find("span","ttar_traindest").text.split(" ")[-1]
        estimated_arrival=train_div.find("div","ttar_trainpred").text.split("\n")[-1]
        response_str+=dest+" "+estimated_arrival+"\n"
    return response_str

if __name__=="__main__":
    requestTrainSchedule("Merchandise Mart")