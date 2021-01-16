from flask_restful import Resource, Api
from flask import Flask, redirect
import sqlite3
import os
import PIL.Image as Image
import glob
import sys 
sys.path.append("/home/aradhya/Desktop/hacks/NITP/back")
sys.path.append("/home/aradhya/Desktop/hacks/NITP/back/database")
sys.path.append("/home/aradhya/Desktop/hacks/NITP/back/telebot")
from sendNot import tele_chat
from placeBid import checkCurrentBid
import notificationsdb
from bidding import updatedb
import datetime

app = Flask(__name__)
api = Api(app)

bot = tele_chat("/home/aradhya/Desktop/hacks/NITP/back/telebot/config.cfg")
class returnImages(Resource):
    def get(self, name):
        files = glob.glob('/home/aradhya/Desktop/hacks/NITP/showImages/*')
        for f in files:
            os.remove(f)

        conn = sqlite3.connect("/home/aradhya/Desktop/hacks/NITP/farmerdb.db")
        cur = conn.cursor()
        sql = f"SELECT * FROM Farmer WHERE NAME='{name}'"
        cur.execute(sql)
        for column in cur.fetchall():
            print("saving")
            Image.frombuffer(mode="RGB", size=(500,500), data=column[8]).save("/home/aradhya/Desktop/hacks/NITP/showImages/img1.jpg")
            Image.frombuffer(mode="RGB", size=(500,500), data=column[9]).save("/home/aradhya/Desktop/hacks/NITP/showImages/img2.jpg")
            Image.frombuffer(mode="RGB", size=(500,500), data=column[10]).save("/home/aradhya/Desktop/hacks/NITP/showImages/img3.jpg")
            Image.frombuffer(mode="RGB", size=(500,500), data=column[11]).save("/home/aradhya/Desktop/hacks/NITP/showImages/img4.jpg")
    
        return redirect("http://localhost:5000/tableImages")
    
class chechBid(Resource):
    def get(self, farmerPhone):
        currentBid = checkCurrentBid(farmerPhone=farmerPhone)
        return {"result":currentBid}


def notify(farmerName, bidAmount, traderPhone):
    conn, cur = notificationsdb.createdb()

    cur.execute(f"SELECT * FROM Notify WHERE FARMERNAME='{farmerName}'")
    
    cursorlist = cur.fetchall() 
    
    if len(cursorlist) > 0:  ##up for notifications
        for i in cursorlist:
            HIGHESTBID = i[1]      
            
        if HIGHESTBID == bidAmount or HIGHESTBID<bidAmount:
            chatId = bot.getChatId(farmerName)
            print(bot.getName())
            bot.sendMessage(chatId, f"Hey the this is the notifcation for the higestbit placed by {traderPhone} bid amount is {bidAmount}")
            print("message sent")



def placeBid(farmerName, farmerPhone, traderPhone, bidAmount):
    conn = sqlite3.connect("/home/aradhya/Desktop/hacks/NITP/farmerdb.db")
    cur  = conn.cursor()

    cur.execute(f"SELECT * FROM Farmer WHERE NAME='{farmerName}'")

    for i in cur.fetchall():
        startTime = datetime.datetime.strptime(i[5], "%c")
        timeFrame = datetime.datetime.strptime(i[6], "%c")
        if startTime < timeFrame:
    
            notify(farmerName, bidAmount, traderPhone)
            updatedb(farmerPhone, traderPhone, bidAmount)
    

    return redirect("http://localhost:5000/tableImages")
            
        


class notifications(Resource):
    def get(self, farmerName, desiredBid):
        notificationsdb.insertdb(farmerName, desiredBid)
        return redirect("http://localhost:5000/farmerbid")
        



class bid(Resource):
    def get(self, farmerName, farmerPhone, traderPhone, bidAmount):
        result = placeBid(farmerName, farmerPhone, traderPhone, bidAmount)
        return redirect("http://localhost:5000/tableImages")


api.add_resource(returnImages, "/showimages/<string:name>")     
api.add_resource(chechBid, "/checkbid/<string:farmerPhone>")
api.add_resource(bid, "/placebid/<string:farmerName>/<string:farmerPhone>/<string:traderPhone>/<string:bidAmount>")
api.add_resource(notifications, "/notifyfarmer/<string:farmerName>/<string:desiredBid>")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
