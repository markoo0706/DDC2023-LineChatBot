# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,LocationMessage,LocationSendMessage,TemplateSendMessage,ButtonsTemplate,URITemplateAction,PostbackAction,MessageAction,URIAction,CarouselTemplate,CarouselColumn,ImageCarouselTemplate,ImageCarouselColumn
import pymongo

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
    elif event.message.text == "Queencard":
        buttons_template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                        title='餐廳 1',
                        text='說明文字 1',
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
                        title='餐廳 2',
                        text='說明文字 2',
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
        # message = TextSendMessage(text = '收到位置訊息')
        # line_bot_api.reply_message(event.reply_token, event.message)
        buttons_template_message = TemplateSendMessage(
                                    alt_text='ButtonsTemplate',
                                    template=ButtonsTemplate(
                                        thumbnail_image_url='https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1654412348946.jpg',
                                        title='選擇餐廳類型',
                                        text='沒事多吃飯',
                                        actions=[
                                            MessageAction(
                                                label='查看Queencard',
                                            text='Queencard'
                                            ),
                                            URIAction(
                                                label='前往Queencard',
                                                uri='https://www.youtube.com/watch?v=UhD8-HYw13A'
                                            )
                                        ]
                                    )
                                )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
