# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,LocationMessage,LocationSendMessage,TemplateSendMessage,ButtonsTemplate,URITemplateAction,PostbackAction,MessageAction,URIAction,CarouselTemplate,CarouselColumn,ImageCarouselTemplate,ImageCarouselColumn
from placeFunc import findRestaurant


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
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0ku_x7kvNmUyoAUNEllRYbn0pFkOaYYFsSic77ogtwi5aky-g5rCmhwoi5V9ohPShpceg8xDkbbp9FYv6YZnuAOzxLm71N_qFAvZJITpy6-bGQOSIlnqWhXIl2xtgWLs_fR6-2YnwMVHTlrIM4ye-r_e_chOv3CI1oczZnos7MoCROR&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='亞廬義大利窯烤吃到飽餐廳(4.3)',
                        text= '106台灣台北市大安区基隆路二段270號2樓',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                           URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJCVUzyjGqQjQR4-f5c8-keGc'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0n18FbrWHwJI34xiMtkKrB-rsNWMemgLE0F-5icbUMsBAnDw9ph9sNgKquFei5NaRQQX1btW-MYw7M4ofhF7gVbKQYnrL-ct4Kx-ZQm-XsBnaPSsLDTW82a-33LzpycStDILs9BtWT-NPf7KyLKc__-6nvZDK8XYI4xJRD8MYGl9JtB&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                         title= '月之義大利餐廳(4.4)',
                        text= '106台灣台北市大安區敦化南路二段265巷3號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJw3tHETKqQjQR_s7m4QZEEBY'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kq5_u7EamjmZd0mAJhH-jBwziL7VLxHenUmhjllwYtVAOYlwtP4tO3sTcKSqr7VmqB1H-cxQEXTepOJjRXpqYPQXdwy4kfRZOL859OOVY_yULvRQDSgBM7AwgfwvptWtWLY5TGqI0ouowapexZ-p93Mti4JOYpdTtrAWunU_LryhYz&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title= '蘇活義大利麵坊(4.2)',
                        text= '106台灣台北市大安區新生南路三段60巷3號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                           URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJtde7A4mpQjQR3cag3SFcF7c'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0lYl8dunk2iC4bHZVOYjfUcXVArBtBJ11Pe9pcschyOZizT6pHSirz70RTTCxoHZ2FW1_bfA6ci0Pv8hiQqBOkD3d1UqcNoL9i0cmBWoB-6ShNPj3T9KRsI2iRTkJuazuuhGy-i0YYAhWbvcnqePoas-5EE7ZOs6_auCKGQm5mX-hjy&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title= '卡帛素食烘培‧義式廚房‧港式餐點 總店(4.2)',
                        text= '106台灣台北市大安區復興南路二段308巷5號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJuWw81C6qQjQRD7lOTyFReqs'
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
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kJlqfj84bg8gfxcZktpL_2a22UWyzMKmWFHHVuzsu-2vn9avw_5aWhLkfM5zoTvogt8zeb-bOVtW-Vwcy1f-BZZXCuE353J1QzHKmT3iAqmjk_XJYDiXjiP7dsI7Mig-z16In7vq_jiVlW7FuvFwInXMhZvB2TQE8JucLHq5vO8NwU&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='莫宰羊-大安台大店(4.2)',
                        text= '106台灣台北市大安區新生南路三段28號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJ3xl5zIepQjQRGNQknIunDIs'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0ni5ewMZfHJQ0567H2r-e9hSDcSez7c8w3ucLpsARE_F-nOPl72UJ59ugehI1sVeSPci3K2MHRIQ4B1CHwtF_P1KlFSq86249_TopTqabRiHuWUZEKJTL21a8zhMRaTsIkJZR2IYKKwWDoJdO2dJTbGc96PnYBpxw45XosLlCTxTcGg&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                         title= '小李子清粥小菜(3.8)',
                        text= '106台灣台北市大安區復興南路二段142之1號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJ4yt0hyyqQjQRA905QCvA3O4'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0lIpUTLHhL0KWcECRrYZWKderXX_XrapcmnWhHTkq_Jf6-wW-txGge9d_muMK6KIsJsUMWhSLx6gmAn_c4DZssS9Lec94sLDD0Zq08g39_zR-6jncN1dtjoYNfAGIe30H_I_efpLieE7_LBiKg5U9bpYHg46et67H61LutaymCYNwjP&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title= '北平同慶樓(4.0)',
                        text= '106台灣台北市大安區敦化南路二段168號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJKZjIHy6qQjQRvQrWjQCwsi4'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kyMI7znwnJGf7CpNLGiQfZp8GhDlcEzv74PFuaNbbpaPQpKMvMcXZHJfdMqdClQ_peWJvE5yAkC9xSP4Tvw3l5RLLhqZv7BDGUAfX4SyD9N4ylR-fn7UgH2Nr3A380CCFWTMxk5o4fU9tI9QKEbI5mjQGfYXawfA3xnDHG_qNrRbI&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title= '阿玉水餃 (生水餃專賣店)(4.3)',
                        text= '106台灣台北市大安區辛亥路二段217號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJXzNlTS-qQjQRCvn2xhSfPAk'
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
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kbiSOBLqu3PjxT544LET1pgdi4WFH6Bt4kJ6MY9hcGSdUK3BmC-HCvHvHqPNHD-swhFcLQjEXaJ5S90Cphtatc8TPflf5g5RNW603WMhcPddXFlfnQco9pAbscx6cLRi8VI0HqbDUs5hIZPTZ7JnUC6C8AoROFJVSwPoqxh3-_DjDR&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title= '鐵匠 鉄板居酒屋 TEPPAN IZAKAYA TESSHO(4.2)',
                        text= '106台灣台北市大安區敦化南路二段265巷13號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJbQ51FjKqQjQRBps6FeHC6zc'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0k8tsyE-at1uJcgRFi6_xxHP-vN4aptDd00M37Z3Unf0Dbd3hAA4FQptyWpNkyiFzqxLA9u9-PJ4AqIbvaCZnFFgjWX7UE7_M2KOfaF-u7UPrFxoNKLEcCBTINYY0AYHqIy_7aAam7gHrjB0lrkHu1MIH3Z2dU0EXEEj4ZrOV7dXkLA&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                         title= 'ibuki 日本料理餐廳 -台北遠東香格里拉(4.4)',
                        text= '106台灣台北市大安区敦化南路二段201號7樓',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJeUp8ZTKqQjQRylE5RuNdug0'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0mZzxF_pqtOL8x5uePd9-qDINvCYGQGuOC-sMGk0HmIIEjdkY7TTIKbDQrOdTRFtia7S0Bexx6AY0Z25g3VrOzr1wgiFTNTap1m6Swqq_QHb3hg21nHAxBkX0vQ7bSDM7hXHWlCKdLwKJnUjg1XwqCmhEGUR47t4wqeoRscNjYVbL6p&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title= '禾豐日式涮涮鍋(4.4)',
                        text= '106台灣台北市大安區復興南路二段148巷16號1樓',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJMS8whyuqQjQRbqBGebOZsdc'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0l4hIBvmAy7lRHOhGIjpR4P54kjrGq1cJUYvR6SQnYZFxvjeFGnR9JAhYCUbtmf74mQ6L_AERPgCfCvoYRvhd_MWQIZNT7lMdL2_zR-RzYpy5cdNhLlt7E8c93LHEGQC4JTTMGCfM2Y7vfFuMFFbj9FM9OQ_WSUi0DcnYHuFwqSrdPh&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title= '角屋關東煮(4.2)',
                        text= '106台灣台北市大安區大安路二段141巷',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJ2YgDBS2qQjQRKbi_GSqboVg'
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
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0l569DhxMcrdWgufVWxlkqEPEDr61i7Ys_FGCaM8Y7M7d4wMeAuRBHW0lCzK1iZXBux0G0DJ1930qdo7v2cJLYGc08e00y_l1LOQ3uZFTO1otLRlkm6DjfkdaXs63PrTfq1KJudzSvDwzcnGec0iV_UyvjgrhaoePB53L5iYW3-9dFg&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title= 'the Diner 樂子瑞安店(4.3)',
                        text= '106台灣台北市大安區瑞安街145號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJvU5mgSmqQjQR0WhA_Zruk5E'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0mnTXvqo_RiA4D9PJnGar0n65c1-Zrw1iEts-4KPyOzWdWCfZmmGsXkhkLcj7Uzoh-rrS0LHkO5D3f3ZBMsy_6NtNxjlrcCurrN02K5QDxEHYxtUL_rFqg8oIjSgAb4sQkGltFmDpqsf5g_fICQytGS18VVXYjDagnZ-4NuO2l_fet8&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='遠東CAFÉ(4.5)',
                        text= '106台灣台北市大安區和平東路三段60號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJeUp8ZTKqQjQREjxsd92csjg'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kPQjYrRtN6xCc6WMld_xbZ9z1Dz3pZSxOrnEthJ6VkeN8IcYhMA20KN2B60YXI9W9XxHRxVk0UICSxkEHyklTmSHpSNYaIqc1Sdxqi8DOiHM-1SUD4tjrfreIJjiq4FZObN9Cb1U96ridN77_t-TD6bEiX-EZwLPxNEyQrmX7eV7Iw&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='Onni韓食堂(3.8)',
                        text='106台灣台北市大安區復興南路二段173號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJU20RbCyqQjQRjgb82A26DQw'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kypXa9rs804I-hm_PBIaDmYWT8IijS3KEzIUZRPTfYVsvpNPToWXpXP57nU2dCNZJ1zam6YsFJRmthYqM0hyaO_QZtQjRL9wblstsoE_x71z66yMg8Mwjc0q_g4P3SSI8KLxQsO5OccpmN3GW-d0I0HpZ0fe6qig7sVukXqxiACN91&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='找餐。店(3.8)',
                        text='106台灣台北市大安區和平東路三段1巷6-3號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                data='收藏'
                            ),
                           URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJq4Cddi6qQjQRtSouaYEUL9c'
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
