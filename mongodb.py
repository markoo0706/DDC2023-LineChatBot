import pymongo
import pandas as pd
from placeFunc import findRestaurant

# connectionID = "mongodb://mongo:463R2dK98HNM@infra.zeabur.com:30774"

# class myDB():
#     def __init__(self, client):
#         self.DBclient = str(client)
#         self.DB = pymongo.MongoClient(client)
    



myclient = pymongo.MongoClient('mongodb://mongo:463R2dK98HNM@infra.zeabur.com:30774')

mydb = myclient['userDB']
record_col = mydb["record"] # 餐廳紀錄 Collection
favorite_col = mydb["favorite"] # 收藏名單 Collection
rest_col = mydb["restaurant"] # 餐廳資料 Collection

# 測試
df = pd.read_pickle("data.pkl")
rest_name = [i for i in df]



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