# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,LocationMessage,LocationSendMessage,TemplateSendMessage,ButtonsTemplate,URITemplateAction,PostbackAction,MessageAction,URIAction,CarouselTemplate,CarouselColumn,ImageCarouselTemplate,ImageCarouselColumn
from placeInfo import findRestaurant


#line token
channel_access_token = 'fkoo8cmH1C29XiX7vKOqcXa3fJ5wpcHDZkkMw9Y6v7sxhIeT2QZW/VoE1legG4KY6ZaxTXjgtjKc9M9hyZ6oI+KlGbyUUQejNB17GKyMNrQcMwEHpSq7kI0ibsYn6bZO33jExHJ30qGPd+cXp8G6tgdB04t89/1O/w1cDnyilFU='
channel_secret = '14a2ec07a0be3dceff5b6cefcbf60b03'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

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
    if event.message.text == "位置":
        buttons_template_message = TemplateSendMessage(
                alt_text="Please tell me where you are",
                template=ButtonsTemplate(
                    text="Please tell me where you are",
                    actions=[
                        # 傳送目前位置
                        URITemplateAction(
                            label="Send my location",
                            uri="line://nv/location"
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "義式料理":
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                        title='亞廬義大利窯烤吃到飽餐廳',
                        text= '106台灣台北市大安区基隆路二段270號2樓',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                         title= '月之義大利餐廳',
                        text= '106台灣台北市大安區敦化南路二段265巷3號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title= '蘇活義大利麵坊',
                        text= '106台灣台北市大安區新生南路三段60巷3號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title= '卡帛素食烘培‧義式廚房‧港式餐點 總店',
                        text= '106台灣台北市大安區復興南路二段308巷5號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "中式料理":
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                        title='莫宰羊-大安台大店',
                        text= '106台灣台北市大安區新生南路三段28號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                         title= '小李子清粥小菜',
                        text= '106台灣台北市大安區復興南路二段142之1號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title= '北平同慶樓',
                        text= '106台灣台北市大安區敦化南路二段168號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title= '阿玉水餃 (生水餃專賣店)',
                        text= '106台灣台北市大安區辛亥路二段217號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "日式料理":
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                        title= '鐵匠 鉄板居酒屋 TEPPAN IZAKAYA TESSHO',
                        text= '106台灣台北市大安區敦化南路二段265巷13號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                         title= 'ibuki 日本料理餐廳 -台北遠東香格里拉',
                        text= '106台灣台北市大安区敦化南路二段201號7樓',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title= '禾豐日式涮涮鍋',
                        text= '106台灣台北市大安區復興南路二段148巷16號1樓',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title= '角屋關東煮',
                        text= '106台灣台北市大安區大安路二段141巷',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "其他類別":
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                        title= 'the Diner 樂子瑞安店',
                        text= '106台灣台北市大安區瑞安街145號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title='遠東CAFÉ',
                        text= '106台灣台北市大安區和平東路三段60號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title='Onni韓食堂',
                        text='106台灣台北市大安區復興南路二段173號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                        title='找餐。店',
                        text='106台灣台北市大安區和平東路三段1巷6-3號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            MessageAction(
                                label='打開地圖',
                                text='地圖'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "地圖":
        buttons_template_message = TemplateSendMessage(
                                    alt_text='ButtonsTemplate',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url='https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1625226724815.jpg',
                                        title='前往地圖',
                                        text='Google map',
                                        actions=[
                                            URIAction(
                                                label='前往Queencard',
                                                uri='https://www.youtube.com/watch?v=UhD8-HYw13A'
                                            )
                                        ]
                                    )
                                )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
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

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
