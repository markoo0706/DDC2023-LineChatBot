# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,LocationMessage,LocationSendMessage,TemplateSendMessage,ButtonsTemplate,URITemplateAction,PostbackAction,MessageAction,URIAction,CarouselTemplate,CarouselColumn,ImageCarouselTemplate,ImageCarouselColumn
from placeFunc import findRestaurant
from mongodb import add_record, add_record


#line token
channel_access_token = 'fkoo8cmH1C29XiX7vKOqcXa3fJ5wpcHDZkkMw9Y6v7sxhIeT2QZW/VoE1legG4KY6ZaxTXjgtjKc9M9hyZ6oI+KlGbyUUQejNB17GKyMNrQcMwEHpSq7kI0ibsYn6bZO33jExHJ30qGPd+cXp8G6tgdB04t89/1O/w1cDnyilFU='
channel_secret = '14a2ec07a0be3dceff5b6cefcbf60b03'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

# 經緯度，可跟據LocationMessage獲得
lat = 25.020859 
lng = 121.542776

df = findRestaurant(lat, lng)

# 接收ChatGbt 推薦的飲食類型 function(lat, lng) = type1, type2, type3
def getType(loc, lat):
    # /...串接ChatGbt獲得推薦類別的函數，待修改。
    type1 = "義式料理"
    type2 = "中式料理"
    type3 = "日式料理" 
    return type1, type2, type3

resType1, resType2, resType3 = getType(25.020859, 121.542776)


# 套用函數並根據resType從資料庫中抓取相對應的資料

resname = [i for i in df.keys()]
resInfo1 = ['亞廬義大利窯烤吃到飽餐廳', '月之義大利餐廳', '蘇活義大利麵坊', '卡帛素食烘培‧義式廚房‧港式餐點 總店', 'ANTICO FORNO 老烤箱義式披薩餐酒']
resInfo2 = ['莫宰羊-大安台大店', '小李子清粥小菜', '北平同慶樓', '阿玉水餃 (生水餃專賣店)', '紅豆食府 遠企店', '恬園餐廳 - 福華國際文教會館', '溫州大餛飩', '涮八方紫銅鍋' '瑞安豆漿大王' '阿英海產粥', '蔣記家薌麵', '熱翻天生猛海鮮', '忠誠山東蔥油餅 - 此燈亮有餅', '小李子蘭州牛肉拉麵館', '大連風味館', '龍門客棧餃子館 瑞安店', '老龍牛肉麵大王', '花麻辣 麻辣鴛鴦 沙茶火鍋', '小辣椒魷魚羹', '三顧茅廬台北四維店', '八方雲集 (師院店)', '通化街米粉湯50年老店（胡記復興旗艦店）','鳳城燒臘粵菜']
resInfo3 = ['鐵匠 鉄板居酒屋 TEPPAN IZAKAYA TESSHO', '爭鮮迴轉壽司 科技店', '角屋關東煮', 'ibuki 日本料理餐廳 -台北遠東香格里拉', '禾豐日式涮涮鍋']
otherResName = [i for i in resname if i not in (resInfo1 + resInfo2 + resInfo3)]

# 自動生成 carousel＿columns的 函數
def generate_carousel(resInfo):
    carousel_columns = []
    for res in resInfo:
        if res >= 9:
            break
        # 根据需要设置每个 Carousel Column 的属性
        column = CarouselColumn(
            thumbnail_image_url= df[res]['photo_refernce'],
            title= res + "(" + str(df[res]['rating']) + ")",
            text= df[res]['address'],
            actions=[   PostbackAction(
                            label='收藏',
                            display_text ='您已收藏了: ' + res,
                            data = res
                        ),
                        URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:' + df[res]['place_id']
                        ),
                        ]  # 设置按钮或其他操作
        )
        carousel_columns.append(column)
    carousel_template = CarouselTemplate(columns=carousel_columns)
    return carousel_template

# 監聽所有來自 /callback 的 Post Request

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
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
                                        thumbnail_image_url='https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1654412348946.jpg',
                                        title='餐廳類型',
                                        text='請選擇餐廳類型',
                                        actions=[
                                            MessageAction(
                                                label= '日式料理',
                                                text= '日式料理'
                                            ),
                                            MessageAction(
                                                label='義式料理',
                                                text='義式料理'
                                            ),
                                            MessageAction(
                                                label ='中式料理',
                                                text = '中式料理'
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
        msg = "收藏名單：\n1. 莫宰羊-大安台大店\n2. 亞廬義大利窯烤吃到飽餐廳\n3. 遠東CAFÉ"
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token,message)
    else:
        msg= event.message.text
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token,message)

         

@handler.add(MessageEvent, message=LocationMessage)
def handle_loc_message(event):   
        lat = event.message.latitude
        long = event.message.longitude
        # 1. 經緯度位置轉天氣
        # 2. 天氣轉推薦類別(Chatgbt, 推薦系統)
        # 3. 推薦類別轉 Button Template 輸出
        # restaurant_info = findRestaurant(lat, long) # 根據經、緯度獲取附近餐廳名單(Dict)
        # message = TextSendMessage(text = "獲取位置資訊")
        # line_bot_api.reply_message(event.reply_token, message)
        buttons_template_message = TemplateSendMessage(
                                    alt_text='ButtonsTemplate',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url='https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1654412348946.jpg',
                                        title='餐廳類型',
                                        text='請選擇餐廳類型',
                                        actions=[
                                            MessageAction(
                                                label= '日式料理',
                                                text= '日式料理'
                                            ),
                                            MessageAction(
                                                label='義式料理',
                                                text='義式料理'
                                            ),
                                            MessageAction(
                                                label ='中式料理',
                                                text = '中式料理'
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

@handler.add(PostbackAction) # 監聽PostBackAciton

def add_favorite(event): # 收藏餐廳函數
     user_id = event.source.user_id
     resName = event.post.data
     add_favorite(user_id, resName)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
