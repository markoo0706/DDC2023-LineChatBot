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
        # 根据需要设置每个 Carousel Column 的属性
        column = CarouselColumn(
            thumbnail_image_url= df[res]['photo_refernce'],
            title= res + str(df[res]['rating']),
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
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kJlqfj84bg8gfxcZktpL_2a22UWyzMKmWFHHVuzsu-2vn9avw_5aWhLkfM5zoTvogt8zeb-bOVtW-Vwcy1f-BZZXCuE353J1QzHKmT3iAqmjk_XJYDiXjiP7dsI7Mig-z16In7vq_jiVlW7FuvFwInXMhZvB2TQE8JucLHq5vO8NwU&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='莫宰羊-大安台大店(4.2)',
                        text= '106台灣台北市大安區新生南路三段28號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                display_text ='您已收藏了: ' + '莫宰羊-大安台大店',
                                data = '莫宰羊-大安台大店'
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
                                display_text ='您已收藏了: ' + '小李子清粥小菜',
                                data = '小李子清粥小菜'
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
                                display_text ='您已收藏了: ' + '北平同慶樓',
                                data = '北平同慶樓'
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
                                display_text ='您已收藏了: ' + '阿玉水餃',
                                data = '阿玉水餃'
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
    elif event.message.text == resType3:
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
                                display_text ='您已收藏了: ' + '鐵匠 鉄板居酒屋 TEPPAN IZAKAYA TESSHO',
                                data = '鐵匠 鉄板居酒屋 TEPPAN IZAKAYA TESSHO'
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
                                display_text ='您已收藏了: ' + 'ibuki 日本料理餐廳 -台北遠東香格里拉',
                                data = 'ibuki 日本料理餐廳 -台北遠東香格里拉'
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
                                display_text ='您已收藏了: ' + '禾豐日式涮涮鍋',
                                data = '禾豐日式涮涮鍋'
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
                                display_text ='您已收藏了: ' + '角屋關東煮',
                                data = '角屋關東煮'
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
                                display_text ='您已收藏了: ' + 'the Diner 樂子瑞安店',
                                data = 'the Diner 樂子瑞安店'
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJvU5mgSmqQjQR0WhA_Zruk5E'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0mnTXvqo_RiA4D9PJnGar0n65c1-Zrw1iEts-4KPyOzWdWCfZmmGsXkhkLcj7Uzoh-rrS0LHkO5D3f3ZBMsy_6NtNxjlrcCurrN02K5QDxEHYxtUL_rFqg8oIjSgAb4sQkGltFmDpqsf5g_fICQytGS18VVXYjDagnZ-4NuO2l_fet8&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='遠東CAFÉ(4.5)',
                        text= '106台灣台北市大安區和平東路三段60號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                display_text ='您已收藏了: ' + '遠東CAFÉ',
                                data = "遠東CAFÉ"
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJeUp8ZTKqQjQREjxsd92csjg'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kPQjYrRtN6xCc6WMld_xbZ9z1Dz3pZSxOrnEthJ6VkeN8IcYhMA20KN2B60YXI9W9XxHRxVk0UICSxkEHyklTmSHpSNYaIqc1Sdxqi8DOiHM-1SUD4tjrfreIJjiq4FZObN9Cb1U96ridN77_t-TD6bEiX-EZwLPxNEyQrmX7eV7Iw&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='Onni韓食堂(3.8)',
                        text='106台灣台北市大安區復興南路二段173號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                display_text ='您已收藏了: ' + 'Onni韓食堂',
                                data = "Onni韓食堂"
                            ),
                            URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJU20RbCyqQjQRjgb82A26DQw'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=AZose0kypXa9rs804I-hm_PBIaDmYWT8IijS3KEzIUZRPTfYVsvpNPToWXpXP57nU2dCNZJ1zam6YsFJRmthYqM0hyaO_QZtQjRL9wblstsoE_x71z66yMg8Mwjc0q_g4P3SSI8KLxQsO5OccpmN3GW-d0I0HpZ0fe6qig7sVukXqxiACN91&key=AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog',
                        title='找餐。店(3.8)',
                        text='106台灣台北市大安區和平東路三段1巷6-3號',
                        actions=[
                            PostbackAction(
                                label='收藏',
                                display_text ='您已收藏了: ' + '找餐。店',
                                data = "找餐。店"
                            ),
                           URIAction(
                                label='打開地圖',
                                uri='https://www.google.com/maps/place/?q=place_id:ChIJq4Cddi6qQjQRtSouaYEUL9c'
                            )
                        ]
                    )
                ]
            )
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
