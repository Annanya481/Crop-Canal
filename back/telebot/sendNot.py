import requests
import configparser as cfg
import sqlite3

class tele_chat():
    def __init__(self, config):
        self.config_token = self.read_token(config)
        self.baseurl = f"https://api.telegram.org./bot{self.config_token}/"

    def getUpdates(self, offset=None):
        res = requests.get(self.baseurl + "getUpdates")
        return res.json()
    
    def sendMessage(self, chatId, message):
        urlToMessage = self.baseurl + f"sendMessage?text={message}&chat_id={chatId}"
        if message:
            requests.get(urlToMessage)

    def read_token(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('cred', 'token')


    def getName(self):
        names = []
        for name in self.getUpdates()["result"]:
            names.append(name["message"]["from"]["first_name"])    
        return names

    def getChatId(self, name):
        for names in self.getUpdates()["result"]:
            firstName = names["message"]["chat"]["first_name"]
            if name == firstName:
                return names["message"]["chat"]["id"]

if __name__ == "__main__":
    bot = tele_chat("back/telebot/config.cfg")
    print(bot.getName())
    chat = bot.getChatId("A")

    bot.sendMessage(chat, "hello")
