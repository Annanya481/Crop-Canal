import sqlite3

def createdb():
    global conn 
    global cur
    conn = sqlite3.connect("farmerdb.db")
    cur  = conn.cursor()

    query = '''  CREATE TABLE IF NOT EXISTS Farmer (Name TEXT, Ph INT, BasePrice INT, Verified INT, Crop TEXT, Time TEXT, TimeFrame TEXT,
                Quantity INT, Veri1 BLOB, veri2 BLOB, veri3 BLOB, veri4 BLOB, veri5 BLOB)'''
    cur.execute(query)
    return conn, cur



def insertdb(name, ph, basePrice, verified, croptype, time, timeFrame, quantity, veri1, veri2, veri3, veri4, veri5):
    try:    
        conn, cur = createdb()
        query = 'INSERT INTO Farmer VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cur.execute(query, (name, ph, basePrice, verified, croptype, time, timeFrame, quantity,  veri1, veri2, veri3, veri4, veri5))
        conn.commit()
    except RuntimeError:
        print("INSERTION FAILED")


   
  


if __name__ == "__main__":
    print(createdb())
   

  