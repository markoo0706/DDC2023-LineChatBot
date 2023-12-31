import pymongo
import pandas as pd
from placeFunc import findRestaurant

class mongoDB():
    def __init__(self, client):
        self.client = pymongo.MongoClient(client)
        self.DB = self.client["myDB"]
        # 建立 DB 下的四個 Collection : favorite, restaurant, penalty, recommend.
        self.favDB = self.DB["favorite"]
        self.resDB = self.DB["restaurant"]
        self.penDB = self.DB["penalty"]
        self.recDB = self.DB["recommend"]
    def add_rest_info(self, colName, df: dict, resName): # 把json檔丟入資料庫 
        query = {'resName': resName}
        existing_document  = self.DB[colName].find_one(query)
        if not existing_document:
            self.DB[colName].insert_one({
                    "resName" : resName,
                    "place_id" : df[resName]["place_id"],
                    "lat" : df[resName]["lat"],
                    "lng" : df[resName]["lng"],
                    "address" : df[resName]["address"],
                    "photo_refernce" : df[resName]['photo_refernce'],
                    "rating" : df[resName]["rating"],
                    "open_hour" : df[resName]["open_hour"],
                    #"review" : df[resName]["review"]
                })
        return
    # 把收藏餐廳丟入收藏資料庫
    def add_favo_rest(self, df, userId, resName):
        query = {'resName': resName, "user" : userId}
        existing_document  = self.DB["favorite"].find_one(query)
        if not existing_document: # 若不在資料庫中
            self.DB["favorite"].insert_one({
                    "resName" : resName,
                    "user" : userId,
                })
        return
    def show_favo_rest(self, userId): 
        query = {"user" : userId}
        result  = self.DB["favorite"].find(query)
        document = list(result)
        return document
    def delete_user_info(self, userId): # 刪除使用者的資料
        return
    def delete_res_info(self, colName, resName): # 刪除餐廳資料
        return
    def delete_collection(self, colName):
        result = self.DB[colName].delete_many({})
    def show_colleciton(self, colName):
        cursor = self.DB[colName].find({})
        for document in cursor:
            print(document)     
    def clear_all_DB(self): # 刪除資料庫中所有資料
        self.favDB.delete_many({})
        self.penDB.delete_many({})
        self.resDB.delete_many({})
        self.recDB.delete_many({})
    def collection_to_df(self, colName):
        data = self.DB[colName].find()
        data_list = [record for record in data]
        df = pd.DataFrame(data_list)
        return df
    def close_connection(self):
        self.client.close()
    
def Test(): # 測試函數
    lat = 25.020859 
    lng = 121.542776
    df = findRestaurant(lat, lng)
    # key = 'your mongoDB key'
    mydb = mongoDB(key)
    mydb.add_favo_rest(df, 123, list(df.keys())[0]) 
    mydb.add_favo_rest(df, 123, list(df.keys())[1])
    mydb.add_favo_rest(df, 123, list(df.keys())[2])
    document = mydb.show_favo_rest(123)
    # for instance in document:
        # print(instance)
    # for resName in [i for i in df.keys()]:
    #     mydb.add_rest_info("restaruant", df, resName)
    print(mydb.collection_to_df("favorite"))
    mydb.show_colleciton("restaruant")
    mydb.show_colleciton("favorite")
    mydb.delete_collection("restaruant")
    mydb.delete_collection("favorite")
    mydb.close_connection()

# Test()
