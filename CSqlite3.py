

import os
import re
import glob
import sqlite3


class CSqlite3(object):
    """Instagram 크롤링을 위한 클래스"""
    
    def __init__(self):
        a = 0
        
    def DisconnectsDb(self):
        self.conn.close()

    def ExecuteDb(self, strQry):
        self.cur.execute(strQry)
        self.conn.commit()

    
    def ConnectDb(self, strDbName):
        '''get db file list,
            use current directory as base,
            and db3 as extention
        '''
        try:
            self.conn = sqlite3.connect(strDbName + ".db")
            self.cur = self.conn.cursor()
        except:
            print ('Error connecting to database')
            raise

    
    def CreateTable(self, strTableName):
        strQry = '''create table %s
            (INSTA_URL text, CONTENT text, CONTENT_DATE DATETIME,
            CONTENT_LIKE INTEGER, CONTENT_PLACE text, CONTENT_TAG, text)''' % strTableName
        self.ExecuteDb(strQry)
    
    def Insert(self):
        c.execute("""insert into stocks
              values ('2006-01-05','BUY','RHAT',100,35.14)""")
        self.db.commit()
    
        #secure search    
        t = (symbol,)
        c.execute('select * from stocks where symbol=?', t)
    
        # inserting many
        for t in [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                  ('2006-04-05', 'BUY', 'MSOFT', 1000, 72.00),
                  ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                 ]:
            c.execute('insert into stocks values (?,?,?,?,?)', t)
        self.db.commit()
    
    
    
    def fetchData(self, interval):
    
        c = self.db.cursor()
        table_name='some_table'
        sql="SELECT a, b, c FROM %s WHERE 1" % ( table_name)
        c.execute(sql)
    
        for row in c:
            col1, col2, col3 = row
            #some action
    
        expr="some regex"
        regexp_func = lambda expr, item: re.compile(expr).search(item) is not None
            # Create function in SQLite for REGEXP operator
        self.db.create_function( "regexp", 2, regexp_func )
    
        c.execute("SELECT a, b FROM tablex WHERE `variable` REGEXP ?", ( regexp, ) )
        for row in c:
            col1, col2, col3 = row
            #some action
    
    #db=initdb()

