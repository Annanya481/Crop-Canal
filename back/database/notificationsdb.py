import sqlite3

def createdb():
    conn = sqlite3.connect("/home/aradhya/Desktop/hacks/NITP/noticationsdb.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS Notify (FARMERNAME TEXT, HIGHESTBID TEXT)''')
    return conn, cur

def insertdb(farmerName, desiredBid):
    conn, cur = createdb()
    sql = f"INSERT INTO Notify VALUES{farmerName, desiredBid}"
    cur.execute(sql)
    conn.commit()


