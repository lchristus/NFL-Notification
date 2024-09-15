import os
import requests
import telebot
from bs4 import BeautifulSoup
import time

gameids = [401671807]
bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])
chatid = os.environ["NFLCHAT"]
hosturl = "https://nfl-notification.onrender.com/status"
espnurl = "https://espn.com/nfl/game/_/gameId/"
scores = Dictionary()

def start():
    while True:
        scrape()
        s.get(hosturl)
        time.sleep(60)  

def scrape():
    for id in gameids:
        try:
            s = requests.Session()
            page = s.get(espnurl + str(id))
            page.raise_for_status() 
            soup = BeautifulSoup(page.content, "html.parser")
            
            scorecard = soup.find("div", class_="Gamestrip_Competitors relative flex Gamestrip_Competitors--boarder")
            if not scorecard:
                print("not found")
                continue
            
            names = scorecard.find_all("div", class_="ScoreCell_Teamname Scorecell_Teamname--abrev")
            score = scorecard.find_all("div", class_="Gamestrip_Score relative tc w-100 fw-heading-100 h3 clr-gray-01")
            
            if len(score) != 2 or len(names) != 2:
                print("not right content")
                continue
            
            complete_score = f"{score[0].text}:{score[1].text}"
            if scores.get(id) != complete_score:
                message = f"{names[0].text} {complete_score} {names[1].text}"
                bot.send_message(chatid, message)
                scores.update({id : complete_score})

        except requests.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Error parsing page or sending message: {e}")
