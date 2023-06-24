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
                    "review" : df[resName]["review"]
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
                    "place_id" : df[resName]["place_id"],
                    "lat" : df[resName]["lat"],
                    "lng" : df[resName]["lng"],
                    "address" : df[resName]["address"],
                    "rating" : df[resName]["rating"]
                })
        return
    def show_favo_rest(self, userId): 
        query = {"user" : userId}
        existing_document  = self.DB["favorite"].find_many(query)



    def delete_user_info(self, userId):
        return
    def delete_res_info(self, colName, resName):
        return
    def delete_collection(self, colName):
        result = self.DB[colName].delete_many({})
        
    # def delete_db(self, colName):
    #     for i in ["favorite", "restaurant", "penalty", "recommend"]:
    #         d
    def show_colleciton(self, colName):
        print(self.DB[colName].count_documents({}))
        
def Test(): # 測試函數
    lat = 25.020859 
    lng = 121.542776
    df = findRestaurant(lat, lng)

    key = 'mongodb://mongo:463R2dK98HNM@infra.zeabur.com:30774'
    mydb = mongoDB(key)

    for resName in [i for i in df.keys()]:
        mydb.add_rest_info("restaruant", df, resName)
    mydb.show_colleciton("restaruant")
    
    mydb.delete_collection("restaruant")
    mydb.delete_collection("favorite")

Test()