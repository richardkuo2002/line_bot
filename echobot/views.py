import imp
from django.shortcuts import render
# Create your views here.
from django.conf import settings
from django.http import  HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from echobot.models import *




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
                if User_Info.objects.filter(uid=uid).exists()==False:
                    User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext)
                    message.append(TextSendMessage(text='會員資料新增完畢'))
                elif User_Info.objects.filter(uid=uid).exists()==True:
                    message.append(TextSendMessage(text='已經有建立會員資料囉'))
                    user_info = User_Info.objects.filter(uid=uid)
                    for user in user_info:
                        info = 'UID=%s\nNAME=%s\n大頭貼=%s'%(user.uid,user.name,user.pic_url)
                        message.append(TextSendMessage(text=info))
                    line_bot_api.reply_message(event.reply_token,message)
        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    


