import pymongo
import pandas as pd
from placeFunc import findRestaurant

class myDB():
    def __init__(self, client):
        self.DBclient = str(client)
        self.DB = pymongo.MongoClient(client)
    



myclient = pymongo.MongoClient('mongodb://mongo:463R2dK98HNM@infra.zeabur.com:30774')

mydb = myclient['userDB']
record_col = mydb["record"] # 餐廳紀錄 Collection
favorite_col = mydb["favorite"] # 收藏名單 Collection
rest_col = mydb["restaurant"] # 餐廳資料 Collection

# 測試
df = pd.read_pickle("data.pkl")
rest_name = [i for i in df]

def add_res_db():
    for res in rest_name:
        add_rest(res, df[res])
    return
def show_res_df():
    print(rest_col.find()[0])
def add_rest(restName, restInfo: dict):
    rest_col.insert_one({
        "name" : restName,
        "address" : restInfo["address"],
        "lat" : restInfo["lat"],
        "long" : restInfo["lng"],
        "place_id" : restInfo["place_id"]
        })
    return
def add_favrite(userId, rest: dict): # 新增收藏紀錄
    favorite_col.insert_one({
        "userID" : userId,
        "Info" : rest
    })
    print("新增了一項收藏名單")
    return

def add_record(userId, rest: dict): # 新增餐廳紀錄
    record_col.insert_one({
        "userID" : userId,
        "Info" : rest
        })
    print("您已新增了一筆資料 !")
    return True

def delete_info(userId): # 刪除某用戶的歷史紀錄
    myquery = { "userID": userId}
    record_col.delete_many(myquery)
    print("您已刪除了一筆資料 !")
    return True

def get_all_user_info(colName):
    for x in colName.find():
        print(x["Info"])
    return True

def delete_collection(colName):
    for x in colName.find():
        colName.delete_one(x)
    print("您刪除了所有資料 !")
    return True

# 測試 飲食紀錄 資料庫
def test_record():
    # 新增資料
    add_record("使用者A", df["亞廬義大利窯烤吃到飽餐廳"])
    add_record("使用者B", df["Onni韓食堂"])
    add_record("使用者C", df["SUBWAY 敦化和平店"])
    add_record("使用者A", df["三顧茅廬台北四維店"])
    add_record("使用者C", df["北平同慶樓"])
    print()
    # 刪除使用者資料 
    delete_info("使用者B")
    print()
    # 印出所有者資料
    get_all_user_info(record_col)

    # 刪除所有使用者資料
    delete_collection(record_col)
    return True

# 測試 用戶偏好資料庫
def test_favorite():

    add_favrite("使用者A", df["亞廬義大利窯烤吃到飽餐廳"])
    add_favrite("使用者B", df["Onni韓食堂"])
    add_favrite("使用者C", df["SUBWAY 敦化和平店"])
    add_favrite("使用者A", df["三顧茅廬台北四維店"])
    add_favrite("使用者C", df["北平同慶樓"])

    # 印出所有使用者資料
    get_all_user_info(favorite_col)

    # 刪除所有資料
    delete_collection(favorite_col)
    return

# print(mydb.list_collection_names())
# test_record()
# test_favorite()

# add_favrite(1234, "找餐。店")
# print(mydb["favorite"].find_one())