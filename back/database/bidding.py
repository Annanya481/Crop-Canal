import sqlite3
import datetime

def createdb():
    global conn
    global cur
    conn = sqlite3.connect("/home/aradhya/Desktop/hacks/NITP/bidding.db")
    cur = conn.cursor()

    sql = "CREATE TABLE IF NOT EXISTS Bidding(FarmerPhone TEXT, TraderPhone TEXT, BiddingAmount INT, TraderPan INT)"
    try:
        cur.execute(sql)

    except RuntimeError:
        print("Failed to createdb")
    
    return cur, conn

def insertdb(farmerPhone, traderPhone, bidAmount, traderpan):
    cur, conn = createdb()
    sql = f"INSERT INTO Bidding VALUES{farmerPhone, traderPhone, bidAmount, traderpan}"    
    cur.execute(sql)
    conn.commit()

def updatedb(farmerPhone, traderPhone, bidAmount, traderpan):
    cur, conn = createdb()
    cur.execute(f"SELECT * FROM Bidding WHERE FarmerPhone='{farmerPhone}'")
    cursorlist = cur.fetchall()

    if len(cursorlist) == 0:
        insertdb(farmerPhone, traderPhone, bidAmount, traderpan)

    print(farmerPhone, traderPhone, bidAmount, traderpan)
    sql = f"SELECT * FROM Bidding WHERE FarmerPhone='{farmerPhone}'"
    cur.execute(sql)
    if len(cur.fetchall())>0:
  
        sql = f"UPDATE Bidding SET BiddingAmount={bidAmount}, TraderPhone='{traderPhone}' WHERE FarmerPhone='{farmerPhone}'"
        cur.execute(sql)
        conn.commit()

        

if __name__ == "__main__":
    createdb()
    insertdb("8939693092", "932932932", "1000", "asdlknas")
    # insertdb("0000000", "932932932", "2000")
    q = "SELECT * FROM Bidding"
    cur.execute(q)                          # which one to trigger first search db for name initially 
    print(cur.fetchall())

    updatedb("8939693092", "12348092340", "2000", "asldkasdn")
    # updatedb("0000000", "12348092340", "3000")
    # searchdb("aradhya")

    q = "SELECT * FROM Bidding"
    cur.execute(q)
    print(cur.fetchall())
