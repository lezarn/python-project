import sqlite3


class db_controler:
    pass
    
	
    def __init__(self):
        self.database = sqlite3.connect("database.db")
        self.cur = self.database.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS user(account text, password text,
        authority integer,token text,ltime integer, PRIMARY KEY(account))''')

        if(self.user_search("root")==None):
            self.user_insert("root","password",0)
		
		
		
    def user_insert(self, user_ac, user_pw, user_auth = 2,token = "",ltime = 0):
        info = (user_ac, user_pw ,user_auth,token,ltime)
        self.cur.execute("INSERT INTO user VALUES (?,?,?,?,?)", info)
        self.database.commit()
		
		
    def user_search(self, user_ac):
        info = (user_ac,)
        self.cur.execute("SELECT * FROM user WHERE account=?", info)
        self.database.commit()
        return self.cur.fetchone()

    def user_update(self, token, ltime, user_ac):
        info = (token, ltime, user_ac)
        self.cur.execute("UPDATE user SET token=?, ltime=? WHERE account=?",info)


    def user_delete(self, user_ac):
        info = (user_ac,)
        self.cur.execute("DELETE FROM user WHERE account=?", info)
        self.database.commit()


    def print_all(self):
        self.cur.execute("SELECT * FROM user ORDER BY authority")
        self.database.commit()
        return print(self.cur.fetchall())
    

    def delete_all(self):
        self.cur.execute("DELETE FROM user")
        self.database.commit()
        
	
    def __del__(self):
        self.database.close()
		
	
