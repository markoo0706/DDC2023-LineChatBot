import pymongo
 
myclient = pymongo.MongoClient('mongodb://mongo:463R2dK98HNM@infra.zeabur.com:30774')
 
mydb = myclient['runoobdb']
mycol = mydb["sites"]
 
# mylist = [
#   { "_id": 1, "userID": "使用者A", "餐廳類型": "西式", "餐廳名稱": "麥當勞新生店" },
#   { "_id": 2, "userID": "使用者B", "餐廳類型": "中式", "餐廳名稱": "阿英滷肉飯" },
#   { "_id": 3, "userID": "使用者C", "餐廳類型": "泰式", "餐廳名稱": "泰泰" },
#   { "_id": 4, "userID": "使用者A", "餐廳類型": "日式", "餐廳名稱": "割烹料理" },
#   { "_id": 5, "userID": "使用者C", "餐廳類型": "中式", "餐廳名稱": "魷魚焿麵" }
# ]
 
# x = mycol.insert_many(mylist)
# print(x.inserted_ids)


def insert_user_info(userId, resType, resName):
    x = mycol.insert_one({"userID" : userId, "餐廳類型" : resType, "餐廳名稱" : resName})
    print("您已新增了一筆資料 !\n")
    return True
def delete_single_user_info(userId):
    myquery = { "userID": userId}
    mycol.delete_one(myquery)
    print("您已刪除了一筆資料 !\n")
    return True
def get_all_user_info():
    for x in mycol.find():
        print(x)
    return True
def delete_all_user_info():
    for x in mycol.find():
        mycol.delete_one(x)
    print("您刪除了所有資料 !\n")
    return True

# 新增使用者資料
insert_user_info("使用者A", "西式", "麥當勞新生店" )
insert_user_info("使用者B", "中式", "阿英滷肉飯")
insert_user_info("使用者C", "泰式", "泰泰" )
insert_user_info("使用者A", "日式", "割烹料理")
insert_user_info("使用者C", "中式", "魷魚焿麵")

# 刪除使用者資料 
delete_single_user_info("使用者B")

# 印出所有使用者資料
get_all_user_info()

# 刪除所有使用者資料
delete_all_user_info()

