import sys
import os 
from flask import Flask, render_template, request
from flask import redirect
import pandas as pd 
import sqlite3
sys.path.append("back")
from getPrediction import predictMain
from PIL import Image
from metric import ptcalMetric
import datetime
import time 
sys.path.append("back/database")
from database.farmer import createdb, insertdb
sys.path.append("/home/aradhya/Desktop/hacks/NITP/back")
sys.path.append("/home/aradhya/Desktop/hacks/NITP/back/database")
from placeBid import checkCurrentBid
# import trader 
from changeImages import imgBytes
import os 
app = Flask(__name__, static_folder="/home/aradhya/Desktop/hacks/NITP/showImages")   
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
createdb()

@app.route("/index", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")  ## landing bs 

@app.route("/farmer", methods=["POST", "GET"])
def farmer():
    global name
    global ph
    global basePrice
    global timeFrame
    global quantity
    if request.method == "POST":
        name = request.form["nm"]
        ph = request.form["ph"]
        basePrice = request.form["pr"]
        quantity = request.form["quantity"]
        timeFrame = request.form["Time"]  
        if timeFrame == "1":
            timeFrame = datetime.datetime.now() + datetime.timedelta(hours=24)
            timeFrame = timeFrame.strftime("%c")
        if timeFrame == "2":
            timeFrame = datetime.datetime.now() + datetime.timedelta(hours=48)
            timeFrame = timeFrame.strftime("%c")
        if timeFrame == "3":
            timeFrame = datetime.datetime.now() + datetime.timedelta(hours=72)
            timeFrame = timeFrame.strftime("%c")
        return redirect("http://localhost:5000/upload") ##upload time
    
    return render_template("farmer.html")

@app.route("/upload", methods=["GET", "POST"])
def upload(postCount=0):
    print("entered")
    test = predictMain()      
    global cropType 
    global avg
    if request.method == "POST": 
        print("POSTING IMAGES")
        postCount+=1
        mainImage = request.files["main-image"]
        
        veri1 = request.files["image(1)"]
        
        veri2 = request.files["image(2)"]
        veri3 = request.files["image(3)"]
        
        veri4 = request.files["image(4)"]
        veri5 = request.files["image(5)"]

        veri1bo, veri2bo, veri3bo, veri4bo, veri5bo = imgBytes(veri1, veri2, veri3, veri4, veri5)

        cropType, veri1, veri2, veri3, veri4, veri5 = test.predict(mainImage, veri1, veri2, veri3, veri4, veri5)
        print(veri1, veri2, veri3, veri4, veri5)
        avg = round(ptcalMetric([veri1, veri2, veri3, veri4, veri5])*100, 2)

        dateNow = datetime.datetime.now()
        dateNow = dateNow.strftime("%c")
        insertdb(name, ph, basePrice, avg, cropType, dateNow, timeFrame, quantity, veri1bo, veri2bo, veri3bo, veri4bo, veri5bo)
        return redirect("http://localhost:5000/finalFarmer")
    
    return render_template("diffViews.html") 

@app.route("/finalFarmer", methods=["GET", "POST"])
def finalFarmer():
    return render_template("success.html", cropType=cropType, avg=avg)



# @app.route("/trader", methods=["GET", "POST"])
# def traderDetails():
#     global table
#     if request.method == "POST":
#         name = request.form["tradernm"]
#         ph = request.form["traderph"]
#         trader.insertdb(name, ph)
        
        
#         return redirect("http://localhost:5000/tableImages")
#     return render_template("trader.html")



@app.route("/farmerbid", methods=["GET", "POST"])
def farmerbid():
    bid = 0

    if request.method == "POST":
        FarmerPhone = request.form["farmerPhone"]
        try:    
            conn = sqlite3.connect("/home/aradhya/Desktop/hacks/NITP/bidding.db")
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM Bidding WHERE FarmerPhone='{FarmerPhone}'")
            cursorlist = cur.fetchall()
            if len(FarmerPhone) > 0 :
                bid = cursorlist[0][2]
                traderPhone = cursorlist[0][1]
                return render_template("farmerbid.html", currentBid=bid, traderPhone=traderPhone)
            # else:
                # return render_template("farmerbid.html", currentBid="No bids yet", traderPhone=traderPhone)

            return render_template("farmerbid.html", currentBid="No bids Yet")
        except:
            pass

    return render_template("farmerbid.html")

@app.route("/tableImages", methods=["GET", "POST"])
def showImages():
    bid = 0
    path = 'farmerdb.db'
    conn = sqlite3.connect(path)
        
    df = pd.read_sql("SELECT * FROM Farmer", conn)
        
    table = df.to_html(columns=["Name", "Ph", "BasePrice", "Verified", "Crop", "Time", "TimeFrame", "Quantity"])
    if request.method == "POST":
        farmerPhone = request.form["farmerPhone"]
        bid = checkCurrentBid(farmerPhone) 
    
        return render_template("traderPageTable.html", table=table, currentBid=bid)
    return render_template("traderPageTable.html", table=table)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    