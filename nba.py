import requests
from bs4 import BeautifulSoup as Soup
base="http://localhost:8000"

def toText(s):
    return s.text

def getPreds(soup):
    games=soup.find("table").find_all("tr")[1:]
    response=[]
    for game in games:
        print(game)
        home,away,home_spread,away_spread=map(toText, game.find_all("th"))
        response.append("HOME"+home+" AWAY"+away+" HOME_SPREAD "+home_spread)
    return response

def getOdds():
    response=[]
    url="http://www.oddsshark.com/nba/odds"
    soup=Soup(requests.get(url).text,"html.parser")
    #get teams
    games=[]
    for game in soup.find_all("div", {"class": "op-matchup-right"}):
        games.append(game.find("div", "op-team-top").text+"@"+game.find("div", "op-team-bottom").text)
    #get odds
    bovada=1
    betonline=7
    for idx,game in enumerate(games):
        odds=soup.find("div", {"class": "op-frame"}).find_all("div", {"class": "op-item-row-wrapper not-futures"})[idx].find_all("div", "op-item-wrapper")
        bovada_away_odds=eval(odds[bovada].find("div", "op-item").get("data-op-info"))['fullgame']
        dimes_away_odds=eval(odds[bovada].find("div", "op-item").get("data-op-info"))['fullgame']
        response.append(game.upper())
        if len(away_odds)>1:
            
            response.append("bovada away "+bovada_away_odds)
            response.append("5dimes away "+dimes_away_odds)
    return response

def request(type="preds"):
    response=[]
    if type=="preds":
        soup=Soup(requests.get(base).text,"html.parser")
        response=getPreds(soup)
    elif type=="odds":
        response=getOdds()
    else:
        soup=Soup(requests.get(base).text,"html.parser")
        response=getPower(soup)
    return '\n'.join(response)

if __name__=="__main__":
    print(request("power"))