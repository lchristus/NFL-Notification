import os
import urllib.request
import json
import telebot
from bs4 import BeautifulSoup
import time

gameids = [401671807]
bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])
chatid = os.environ["NFLCHAT"]
hosturl = "https://nfl-notification.onrender.com/status"
espnurl = "https://espn.com/nfl/game/_/gameId/"
scores = dict()

def start():
    while True:
        scrape()
        with urllib.request.urlopen(hosturl) as response:
            response.read()  # Trigger the request and read the response
        time.sleep(60)

def scrape():
    for id in gameids:
        try:
            with urllib.request.urlopen(espnurl + str(id)) as response:
                page_content = response.read()
            
            soup = BeautifulSoup(page_content, "html.parser")
            
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
                scores.update({id: complete_score})

        except urllib.error.URLError as e:
            print(f"URL error: {e}")
        except urllib.error.HTTPError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"Error parsing page or sending message: {e}")

# To start the process
if __name__ == "__main__":
    start()
