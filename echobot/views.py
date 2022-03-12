from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


# Create your views here.

line_bot_api = LineBotApi('8q9MjJrPlCYTK9c/tVoaHfLkZMMhjsfihsw1f4s03ZE4erq1i7N/nponVQJ+c+zVPtBQ1X35q/wUSN0WFODYdmyitlZn9fF1SDoCSkHV+4RS5gKcS8uN9OeyV1R3lSazWtWdod1SrLs2o8lHU7sjQAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fc08e253935409bac40d3a6b8846b71b')


@csrf_exempt
def callback(request: HttpRequest) -> HttpResponse:
    
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessage)
def message_text(event: MessageEvent):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )