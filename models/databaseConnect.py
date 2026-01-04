import pymysql


class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.pwd = "root"
        self.db = "dana"

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            cursorclass=pymysql.cursors.DictCursor, 
        )
    
