import os
import requests
import telebot
from bs4 import BeautifulSoup
import time

gameids = [401671807]
bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])
chatid = os.environ["NFLCHAT"]
hosturl = "nfl-notification.onrender.com/status"
espnurl = "espn.com/nfl/game/_/gameId/"
scores = {}

def start():
  bot.send_message(chatid, "this still work")
  return

def scrape():
  for id in ids:
    s = requests.Session()
    page = s.get(espnurl + id)
    soup = BeautifulSoup(page, "html.parser")
    scorecard = soup.find("div", "Gamestrip_Competitors relative flex Gamestrip_Competitors--boarder")
    names = scorecard.findall("div", "ScoreCell_Teamname Scorecell_Teamname--abrev")
    score = scorecard.findall("div", "Gamestrip_Score relative tc w-100 fw-heading-100 h3 clr-gray-01")
    if score.size() != 2 or names.site() != 2:
      continue
    complete_score = score[0].text+':'+score[1].text
    if scores.get(id) != complete_score:
      bot.send_message(chatid, names[0].text+' '+complete_score+' '+names[1].text)
      s.get(hosturl)
      scores.update({id : complete_score})
