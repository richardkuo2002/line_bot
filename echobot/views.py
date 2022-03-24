from cgi import test
from random import random
from django.shortcuts import render
# Create your views here.
from django.conf import settings
from django.http import  HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from echobot.models import *
import random




line_bot_api = LineBotApi('8q9MjJrPlCYTK9c/tVoaHfLkZMMhjsfihsw1f4s03ZE4erq1i7N/nponVQJ+c+zVPtBQ1X35q/wUSN0WFODYdmyitlZn9fF1SDoCSkHV+4RS5gKcS8uN9OeyV1R3lSazWtWdod1SrLs2o8lHU7sjQAdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('fc08e253935409bac40d3a6b8846b71b')

@csrf_exempt
def callback(request):
    
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            # if isinstance(event, MessageEvent):
            #     line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=event.message.text)
            #      )
        
            if isinstance(event, MessageEvent):
                
                mtext=event.message.text
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=profile.picture_url
                message=[]
                yalin_keyword = [ "510","吳彥霖","彥霖","@Yalin"]
                banword = ["幹","你媽","操","耖","靠北","靠杯","白痴","e04"]
                questionword = ["幫我素","幫素","吃ㄐㄐ","ㄐㄐ","雞雞","打手槍","手槍","?","？"]
                bot_keyword = ["機器人","雞雞人","ㄐㄐ人","bot","BOT","Bot","Robot","robot","🤖️"]
                for text_check in bot_keyword:
                    if mtext.find(text_check)!=-1:
                        bot_message = "機油好難喝"
                        oil = []
                        for i in bot_message:
                            oil.append(i)
                            if random.random()>0.5:
                               oil.append("...")
                        stroil = "".join(oil)
                        message.append(TextSendMessage(text=stroil))
                        line_bot_api.reply_message(event.reply_token,message)
                        break
                for text_check in questionword:
                    if mtext.find(text_check)!=-1:
                        message.append(TextSendMessage(text='？'))
                        line_bot_api.reply_message(event.reply_token,message)
                        break
                for text_check in banword:
                    if mtext.find(text_check)!=-1:
                        if mtext.find("http")==-1 or mtext.find("HTTP")==-1:
                            message.append(TextSendMessage(text='⚠由于此讯息不符合符合吴彦霖主席安全法规，已被屏蔽。'))
                            line_bot_api.reply_message(event.reply_token,message)
                            break
                for text_check in yalin_keyword:
                    if mtext.find(text_check)!=-1:
                        message.append(TextSendMessage(text='請支持1號候選人–吳彥霖。資管要贏，票投彥霖！'))
                        line_bot_api.reply_message(event.reply_token,message)
                        break
                if User_Info.objects.filter(uid=uid).exists()==False:
                    User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext)
                    message.append(TextSendMessage(text='你的個資已被資管彥霖會長掌握，請謹言慎行'))
                    line_bot_api.reply_message(event.reply_token,message)
                # elif User_Info.objects.filter(uid=uid).exists()==True:
                    # message.append(TextSendMessage(text='已經有建立會員資料囉'))
                    # user_info = User_Info.objects.filter(uid=uid)
                    # for user in user_info:
                    #     info = 'UID=%s\nNAME=%s\n大頭貼=%s'%(user.uid,user.name,user.pic_url)
                    #     message.append(TextSendMessage(text=info))
                    # line_bot_api.reply_message(event.reply_token,message)

                # if event.message.type=='text':
                #     message.append(TextSendMessage(text='文字訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='image':
                #     message.append(TextSendMessage(text='圖片訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='location':
                #     message.append(TextSendMessage(text='位置訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='video':
                #     message.append(TextSendMessage(text='影片訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)


                # elif event.message.type=='sticker':
                #     message.append(TextSendMessage(text='貼圖訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='audio':
                #     message.append(TextSendMessage(text='聲音訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)

                # elif event.message.type=='file':
                #     message.append(TextSendMessage(text='檔案訊息'))
                #     line_bot_api.reply_message(event.reply_token,message)
            # elif isinstance(event, FollowEvent):
            #     print('加入好友')
            #     line_bot_api.reply_message(event.reply_token,message)
            # elif isinstance(event, UnfollowEvent):
            #     print('取消好友')
            # elif isinstance(event, JoinEvent):
            #     print('進入群組')
            #     line_bot_api.reply_message(event.reply_token,message)
            # elif isinstance(event, LeaveEvent):
            #     print('離開群組')
            #     line_bot_api.reply_message(event.reply_token,message)
            # elif isinstance(event, MemberJoinedEvent):
            #     print('有人入群')
            #     line_bot_api.reply_message(event.reply_token,message)
            # elif isinstance(event, MemberLeftEvent):
            #     print('有人退群')
            #     line_bot_api.reply_message(event.reply_token,message)
            # elif isinstance(event, PostbackEvent):
            #     print('PostbackEvent')
        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    


