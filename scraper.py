import urllib.request
import requests
import re
from datetime import datetime
from mySql import MySql
import smtplib
import time
from game import Game as Game
import urllib.parse
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Scraper():
    pageCounter = 1
    gameObjectList = []
    dateList = []
    titleList = []
    titleCounter = 0
    datecounter = 0
    sql = MySql()

    def getGameDate(self, dateTag):
        for date in dateTag:
            dateString = date.text

            if "beschikbaar op" in dateString or "verschenen" in dateString:

                match = re.search(r'\d{2}-\d{2}-\d{4}', dateString)
                if match:
                    date = datetime.strptime(match.group(), '%d-%m-%Y').date()
                    print(date)
                    self.dateList.append(date)
                    self.datecounter += 1
                else:
                    date = "date unknown"
                    print(date)
                    self.dateList.append(date)
                    self.datecounter += 1

    def makeGameObjects(self, title, releaseDate):

        gameObject = Game(title, releaseDate)
        return gameObject


    def notifyGameFound(self, gameObjectList):
        import smtplib

        i = 0

        fromaddr = "vincentluder@hotmail.com"
        toaddr = "vincentluder@hotmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "new Games on Bol.com"

        body = "list of new games: \n"
        while i < len(gameObjectList):
            body += Game.getName(gameObjectList[i]) + "\n"

            i += 1

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(fromaddr, "#enterpassword")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)

    def mainSpider(self):
        gameFound = False

        while self.pageCounter < 4:
            url = "https://www.bol.com/nl/l/games/videogames/N/18200+7288/filter_N/25101/index.html?page=%s&view=tiles" % self.pageCounter

            headers = {
                "User-Agent":
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            }

            req = requests.get(url, headers=headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text, 'html.parser')

            titleTag = soup.findAll("a", attrs={"class": "product-title product-title--placeholder"})
            for title in titleTag:
                gameFound = self.sql.getGameFromDatabase(title.text)
                if not gameFound:
                    self.titleList.append(title.text)
                    self.titleCounter += 1
                    #self.notifyGameFound(title.text)
                    print(title.text)

            # dit blok is verantwoordelijk voor de datum
            if not gameFound:
                dateTag = soup.findAll("div", attrs={"class": "medium--is-visible"})

                for date in dateTag:
                    dateString = date.text
                    if "beschikbaar op" in dateString or "verschenen" in dateString:

                        match = re.search(r'\d{2}-\d{2}-\d{4}', dateString)
                        if match:
                            date = datetime.strptime(match.group(), '%d-%m-%Y').date()
                            print(date)
                            self.dateList.append(date)
                            self.datecounter += 1
                        else:
                            date = "date unknown"
                            print(date)
                            self.dateList.append(date)
                            self.datecounter += 1

            self.pageCounter += 1

        print("datecounter: " , self.datecounter)

        if not gameFound:

            self.makeGameObjects()
            self.notifyGameFound(self.gameObjectList)
            for game in self.gameObjectList:
                self.sql.insertGame(Game.getName(game), Game.getReleasedate(game))

    def mainSpider1(self):
        gameFound = False
        i = 0
        while self.pageCounter < 4:
            url = "https://www.bol.com/nl/l/games/videogames/N/18200+7288/filter_N/25101/index.html?page=%s&view=tiles" % self.pageCounter

            headers = {
                "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
                    }

            req = requests.get(url, headers=headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text, 'html.parser')

            titleTag = soup.findAll("a", attrs={"class": "product-title product-title--placeholder"})

            #titleList vullen
            for title in titleTag:
                self.titleList.append(title.text)
                self.titleCounter += 1
                # self.notifyGameFound(title.text)
                print(title.text)

            # dit blok is verantwoordelijk voor de datumList vullen
            dateTag = soup.findAll("div", attrs={"class": "medium--is-visible"})

            for date in dateTag:
                dateString = date.text
                if "beschikbaar op" in dateString or "verschenen" in dateString:

                    match = re.search(r'\d{2}-\d{2}-\d{4}', dateString)
                    if match:
                        date = datetime.strptime(match.group(), '%d-%m-%Y').date()
                        print(date)
                        self.dateList.append(date)
                        self.datecounter += 1
                    else:
                        date = "date unknown"
                        print(date)
                        self.dateList.append(date)
                        self.datecounter += 1

            self.pageCounter += 1

        print("datecounter: ", self.datecounter)


        #check of de namen in de database zitten
        while i < len(self.titleList):
            title = self.titleList[i]
            gameFound = self.sql.getGameFromDatabase(title)

            if not gameFound:
                game = self.makeGameObjects(title, self.dateList[i])
                self.gameObjectList.append(game)

            i += 1
        if len(self.gameObjectList) > 0:
            self.notifyGameFound(self.gameObjectList)
            for game in self.gameObjectList:
                self.sql.insertGame(Game.getName(game), Game.getReleasedate(game))



#Scraper.mainSpider(Scraper)
scraper = Scraper()
#scraper.notifyGameFound("call of fuck jou")
scraper.mainSpider1()