# coding: utf-8
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,LocationMessage,LocationSendMessage,TemplateSendMessage,ButtonsTemplate,URITemplateAction,PostbackAction,MessageAction,URIAction,CarouselTemplate,CarouselColumn,ImageCarouselTemplate,ImageCarouselColumn,PostbackEvent
from placeFunc import findRestaurant
from mongodb import mongoDB
from recommmendation_system import Recommendation
import requests
import json
from getType import getType

# ========================================= 初始變數 ========================================= 

#line token
channel_access_token = 'fkoo8cmH1C29XiX7vKOqcXa3fJ5wpcHDZkkMw9Y6v7sxhIeT2QZW/VoE1legG4KY6ZaxTXjgtjKc9M9hyZ6oI+KlGbyUUQejNB17GKyMNrQcMwEHpSq7kI0ibsYn6bZO33jExHJ30qGPd+cXp8G6tgdB04t89/1O/w1cDnyilFU='
channel_secret = '14a2ec07a0be3dceff5b6cefcbf60b03'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# MongoDB Connection Key
mongoDB_key = 'mongodb://mongo:463R2dK98HNM@infra.zeabur.com:30774'

# 連接 mongoDB 資料庫 
myDB = mongoDB(mongoDB_key)
# 把抓取資料丟入餐廳資料庫 (Merge)
# for resName in [i for i in df.keys()]:
#     myDB.add_rest_info("restaruant", df, resName)

# ========================================= App ========================================= 

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

### 全域變數宣告
TaipeiLoc = (25.020859, 121.542776)
df = findRestaurant(TaipeiLoc[0], TaipeiLoc[1]) 
resname = [i for i in df.keys()]

resType1 = "義式料理" 
resType2 = "日式料理" 
resType3 = "中式料理" 

resInfo1 = ['亞廬義大利窯烤吃到飽餐廳', '月之義大利餐廳', '蘇活義大利麵坊', '卡帛素食烘培‧義式廚房‧港式餐點 總店', 'ANTICO FORNO 老烤箱義式披薩餐酒']
resInfo2 = ['莫宰羊-大安台大店', '小李子清粥小菜', '北平同慶樓', '阿玉水餃 (生水餃專賣店)', '紅豆食府 遠企店', '恬園餐廳 - 福華國際文教會館', '溫州大餛飩', '涮八方紫銅鍋', '瑞安豆漿大王', '阿英海產粥', '蔣記家薌麵', '熱翻天生猛海鮮', '忠誠山東蔥油餅 - 此燈亮有餅', '小李子蘭州牛肉拉麵館', '大連風味館', '龍門客棧餃子館 瑞安店', '老龍牛肉麵大王', '花麻辣 麻辣鴛鴦 沙茶火鍋', '小辣椒魷魚羹', '三顧茅廬台北四維店', '八方雲集 (師院店)', '通化街米粉湯50年老店（胡記復興旗艦店）','鳳城燒臘粵菜']
resInfo3 = ['鐵匠 鉄板居酒屋 TEPPAN IZAKAYA TESSHO', '爭鮮迴轉壽司 科技店', '角屋關東煮', 'ibuki 日本料理餐廳 -台北遠東香格里拉', '禾豐日式涮涮鍋']

def getInfo(df, resname, resType):
    info = [name for name in resname if resType in df[name]["type"]]
    return info

def getTypeApi():
    r = requests.get("https://testapi.zeabur.app/result")
    recommend_list = json.loads(r.text)
    return recommend_list

# 自動生成 carousel＿columns的 函數
def generate_carousel(resInfo):
    carousel_columns = []
    sugNum = 0
    for res in resInfo:
        if sugNum >= 9:
            break
        # 根据需要设置每个 Carousel Column 的属性
        column = CarouselColumn(
            thumbnail_image_url= df[res]['photo_refernce'],
            title= res + "(" + str(df[res]['rating']) + ")",
            text= df[res]['address'],
            actions=[   PostbackAction(
                            label='收藏',
                            data = res
                        ),
                        URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:' + df[res]['place_id']
                        ),
                        ]  # 设置按钮或其他操作
        )
        carousel_columns.append(column)
        sugNum += 1
    carousel_template = CarouselTemplate(columns=carousel_columns)
    return carousel_template

# ========================================= LineChatBot控制 ========================================= 
# 監聽所有來自 /callback 的 Post Request

@app.route("/callback", methods=['POST'])

def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print("body: "  + body, "signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text == "開始":
        buttons_template_message = TemplateSendMessage(
                alt_text="分享目前位置",
                template=ButtonsTemplate(
                    text="請分享您的位置",
                    actions=[
                        # 傳送目前位置
                        URITemplateAction(
                            label="分享位置",
                            uri="line://nv/location"
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    
    elif event.message.text == resType1:
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template = generate_carousel(resInfo1)
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

    elif event.message.text == resType2:
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template = generate_carousel(resInfo2)
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == resType3:
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template = generate_carousel(resInfo3)
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "其他類別":
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template = generate_carousel(otherResName)
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "返回選單":
        buttons_template_message = TemplateSendMessage(
                                    alt_text='ButtonsTemplate',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url='https://i.imgur.com/ZVgyDSs.png',
                                        title='餐廳類型',
                                        text='請選擇餐廳類型',
                                        actions=[
                                            MessageAction(
                                                label= resType1,
                                                text= resType1
                                            ),
                                            MessageAction(
                                                label= resType2,
                                                text= resType2
                                            ),
                                            MessageAction(
                                                label = resType3,
                                                text = resType3
                                            ),
                                            MessageAction(
                                                label = "其他類別",
                                                text = "其他類別"
                                            )
                                        ]
                                    )
                                )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        return 
    elif event.message.text == "收藏名單":
        userId = event.source.user_id
        msg = ""
        document = myDB.show_favo_rest(userId)
        for instance in document:
            msg = msg + instance['resName'] + "\n"
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token,message)
    elif event.message.text == "範例地點:台中":
        TaichungLoc = (24.086310772481895, 120.69548929568965)
        df = findRestaurant(TaichungLoc[0], TaichungLoc[1]) 
        resname = [i for i in df.keys()] # 餐廳名稱(df.keys)的 List
        resType1 = "中式料理"
        resType2 = "日式料理"
        resType3 = "美式料理"
        resInfo1 = ["大呼過癮臭臭鍋", "客家本色Natural Hakka 大里店", "豪記排骨飯",
            "大世紀無骨鵝肉", "古都台南擔仔麵（大里店）傳統小吃、平價美食、爌肉飯", 
            "大里清真黃牛肉水餃館","好妙天然手作坊", "江家小吃麵店", "兩披索靚鍋（外帶燒肉飯、肉羹）", 
            "莊家嘉義火雞肉飯-中興仁化店","金燄鐵板燒", "福鹿手工水餃-大里店 (原:福元寶水餃)", 
            "丐幫滷味大里分舵", "半伴拌麵食館(大里成功總店)｜大里美食｜會議餐客製｜大里麵食...",
            "台北江麻辣臭豆腐火鍋專賣鋪（塗城店）", "麻辣女王（成功店）", 
            "尚食在餐廳 Shang Shi Zai Restaurant", "三媽臭臭鍋大里成功店", "肉圓李（大里店）愛團購",
            "甯客串串鍋-大里旗艦店", "大腸麵線", "阿娘喂...排骨酥麵"] #中式
        resInfo2 = ["すき家 SUKIYA 台中軟體園區店", "禾荳家-Curry(北海道湯咖哩專賣店)科技店 台中美食 台...", "大和川日式料理（大里成功店）",
            "屋裡ウリ - 巷弄裡的日式家常料理"] # 日式
        resInfo3 = ["弘爺漢堡", "Subway台中大里店", "弘爺漢堡 - 青年店", "早安美芝城大里活力成功", "弘爺漢堡 - 達日好店", 
            "Hong Ya Hamburger", "多客牛排", "翡翠精品莊園咖啡-大里杙棧門市", "斐比樂斯咖啡甜點", 
            "漢堡大師 青年店", "8C Origin Coffee|包場|家庭聚會|手沖咖啡廳...", 
            "隨便，坐 sit anywhere 大里必吃早午餐|輕食便當..."] # 美式
        otherResName = [i for i in resname if i not in (resInfo1 + resInfo2 + resInfo3)]
        buttons_template_message = TemplateSendMessage(
                                    alt_text='ButtonsTemplate',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url='https://i.imgur.com/ZVgyDSs.png',
                                        title='餐廳類型',
                                        text='請選擇餐廳類型',
                                        actions=[
                                            MessageAction(
                                                label= resType1,
                                                text= resType1
                                            ),
                                            MessageAction(
                                                label= resType2,
                                                text= resType2
                                            ),
                                            MessageAction(
                                                label = resType3,
                                                text = resType3
                                            ),
                                            MessageAction(
                                                label = "其他類別",
                                                text = "其他類別"
                                            )
                                        ]
                                    )
                                )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        return
    elif event.message.text == "範例地點:台北":
        TaipeiLoc = (25.020859, 121.542776)
        df = findRestaurant(TaipeiLoc[0], TaipeiLoc[1]) 
        resname = [i for i in df.keys()]  
        resType1 = "義式料理"
        resType2 = "日式料理"
        resType3 = "中式料理"
        # # 類別一 的餐廳名稱
        resInfo1 = ['亞廬義大利窯烤吃到飽餐廳', '月之義大利餐廳', '蘇活義大利麵坊', '卡帛素食烘培‧義式廚房‧港式餐點 總店', 'ANTICO FORNO 老烤箱義式披薩餐酒']
        # # 類別二 的餐廳名稱
        resInfo2 = ['莫宰羊-大安台大店', '小李子清粥小菜', '北平同慶樓', '阿玉水餃 (生水餃專賣店)', '紅豆食府 遠企店', '恬園餐廳 - 福華國際文教會館', '溫州大餛飩', '涮八方紫銅鍋', '瑞安豆漿大王', '阿英海產粥', '蔣記家薌麵', '熱翻天生猛海鮮', '忠誠山東蔥油餅 - 此燈亮有餅', '小李子蘭州牛肉拉麵館', '大連風味館', '龍門客棧餃子館 瑞安店', '老龍牛肉麵大王', '花麻辣 麻辣鴛鴦 沙茶火鍋', '小辣椒魷魚羹', '三顧茅廬台北四維店', '八方雲集 (師院店)', '通化街米粉湯50年老店（胡記復興旗艦店）','鳳城燒臘粵菜']
        # # 類別三 的餐廳名稱
        resInfo3 = ['鐵匠 鉄板居酒屋 TEPPAN IZAKAYA TESSHO', '爭鮮迴轉壽司 科技店', '角屋關東煮', 'ibuki 日本料理餐廳 -台北遠東香格里拉', '禾豐日式涮涮鍋']
        # # 其他類別 的餐廳名稱
        otherResName = [i for i in resname if i not in (resInfo1 + resInfo2 + resInfo3)]
        buttons_template_message = TemplateSendMessage(
                                    alt_text='ButtonsTemplate',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url='https://i.imgur.com/ZVgyDSs.png',
                                        title='餐廳類型',
                                        text='請選擇餐廳類型',
                                        actions=[
                                            MessageAction(
                                                label= resType1,
                                                text= resType1
                                            ),
                                            MessageAction(
                                                label= resType2,
                                                text= resType2
                                            ),
                                            MessageAction(
                                                label = resType3,
                                                text = resType3
                                            ),
                                            MessageAction(
                                                label = "其他類別",
                                                text = "其他類別"
                                            )
                                        ]
                                    )
                                )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        return

    elif event.message.text == "刪除收藏":
        userId = event.source.user_id
        myDB.delete_collection("favorite") # bug,需傳入id
        msg = "您已清空收藏名單"
        line_bot_api.reply_message(event.reply_token,message)
    else:
        msg= event.message.text
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token,message)


         

@handler.add(MessageEvent, message=LocationMessage)
def handle_loc_message(event):
        global resType1, resType2, resType3, resInfo1, resInfo2, resInfo3, otherResName, df# 把lat, lng, df 設為global 
        lat = event.message.latitude
        lng = event.message.longitude
        print(lat, lng) # log 測試用
        df = findRestaurant(lat, lng) # 爬取餐廳資料
        resType1, resType2, resType3 = getType(lat, lng) # 獲取推薦類別
        resInfo1, resInfo2, resInfo3 = getInfo(df, list(df.keys()), resType1), getInfo(df, list(df.keys()), resType2), getInfo(df, list(df.keys()), resInfo3)
        buttons_template_message = TemplateSendMessage(
                                    alt_text='ButtonsTemplate',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url='https://i.imgur.com/ZVgyDSs.png',
                                        title='餐廳類型',
                                        text='請選擇餐廳類型',
                                        actions=[
                                            MessageAction(
                                                label= resType1,
                                                text= resType1
                                            ),
                                            MessageAction(
                                                label= resType2,
                                                text= resType2
                                            ),
                                            MessageAction(
                                                label = resType3,
                                                text = resType3
                                            ),
                                            MessageAction(
                                                label = "其他類別",
                                                text = "其他類別"
                                            )
                                        ]
                                    )
                                )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        return

@handler.add(PostbackEvent) # 監聽PostBackAciton
def add_favorite(event): # 收藏餐廳函數
     user_id = event.source.user_id
     resName = event.postback.data
     reply_text = "您已收藏該餐廳: " + resName
     line_bot_api.reply_message(event.reply_token, TextMessage(text=reply_text))
     myDB.add_favo_rest(df, user_id, resName)

@app.route('/athena', methods=["POST"])
def athena():
    # restaurant = request.get_data(as_text=True)
    restaurant = request.get_json()
    
    recommend = restaurant['context']
    recommend = recommend.split('},')
    alist = []
    for i in recommend:
        d = dict()
        if '{' in i:
            i = i.replace('{','')
        if '}' in i:
            i = i.replace('}','')
        for j in i.split(','):
            d[j[:j.index(':')].strip()] = j[j.index(':')+1:]
        alist.append(d)
    mydict = dict()
    for it in alist:
        mydict[it['地點'].strip()] = it['推薦列表'].strip()

    restaurant = restaurant['data']
    for it in restaurant:
        it['recommend'] = mydict[it['LocationName']]

    global RECOMMEND_RESTAURANT
    RECOMMEND_RESTAURANT = restaurant
    
    return {'user': restaurant}

@app.route('/test', methods=['GET']) 
def test():
    return jsonify(RECOMMEND_RESTAURANT)

@app.route('/testapi', methods=['GET'])
def testapi():
    recommend_list = getTypeApi()
    return jsonify(recommend_list)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
