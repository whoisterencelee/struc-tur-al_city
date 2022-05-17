from pymongo import MongoClient

class MongoDBClient:
    
    def __init__ (
        self,
        host = "",
        port = "",
        username = "",
        password = "",
        database = ""
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database
    
    def connectDB(self):
        try:
            self.client = MongoClient(self.host, self.port, username=self.username, password=self.password)
        except:
            raise Exception('DB connection failed!')

    def insertData(self, data, colection=""):
        try:
            database = self.client[self.database_name]
            colection_ = database[colection]
            colection_.insert_one(data)
        except:
            print('DB failed to insert a data!')
