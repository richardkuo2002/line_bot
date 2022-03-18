from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *


# Create your views here.

line_bot_api = LineBotApi('8q9MjJrPlCYTK9c/tVoaHfLkZMMhjsfihsw1f4s03ZE4erq1i7N/nponVQJ+c+zVPtBQ1X35q/wUSN0WFODYdmyitlZn9fF1SDoCSkHV+4RS5gKcS8uN9OeyV1R3lSazWtWdod1SrLs2o8lHU7sjQAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fc08e253935409bac40d3a6b8846b71b')

def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = WebhookParser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                mtext=event.message.text
                message=[]
                message.append(TextSendMessage(text=mtext))
                line_bot_api.reply_message(event.reply_token,message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()