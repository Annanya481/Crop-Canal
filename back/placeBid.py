import datetime
import time

import sys
sys.path.append("/home/aradhya/Desktop/hacks/NITP/back/database")
from bidding import updatedb, createdb
import sqlite3

conn = sqlite3.connect("/home/aradhya/Desktop/hacks/NITP/farmerdb.db")
cur  = conn.cursor()

def checkCurrentBid(farmerPhone):
    cur, conn = createdb()
    sql = f"SELECT * FROM Bidding WHERE FarmerPhone='{farmerPhone}'"        
    cur.execute(sql)
    try:
        currentBid = cur.fetchall()[0][2]
        return currentBid
        
    except Exception as e:
        return "No farmer with that phone number / No bids yet"

if __name__ == "__main__":
    print(checkCurrentBid("8939693092"))
    # print(placeBid("aradhya", "8939693092", "someone", "2000"))
    # checkCurrentBid("8939693092")
