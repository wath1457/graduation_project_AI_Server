from django.shortcuts import render, HttpResponse, redirect
from main.apps import MainConfig
from django.http import JsonResponse
from django.http import Http404
import traceback
import json
from django.core import serializers

from .modules.depression_model_init import dm_init
from .modules.depression_predict import depression_predict
from .modules.chatbot_model_init import cm_init
from .modules.chatbot_reply import predict_reply

setting_completed = False


# 우울증 분석 변수
stopwords = None
depression_tokenizer = None
model = None
max_len = None

# 챗봇 변수
START_TOKEN = None
END_TOKEN = None
MAX_LENGTH = None
chatbot_tokenizer = None
C_model = None

if setting_completed != True:
    print('우울증 분석 모델 로드 시작')
    stopwords, depression_tokenizer, model, max_len = dm_init()
    print('우울증 분석 모델 로드 완료')
    print('챗봇 모델 로드 시작')
    START_TOKEN, END_TOKEN, MAX_LENGTH, chatbot_tokenizer, C_model = cm_init()
    print('챗봇 모델 로드 완료')
    setting_completed = True
else:
    pass

def index(request):
    return render(request, "main/index.html")

def depression(request):
    if request.method == 'POST':
        try:
            # jsonData = request.POST.getlist('user_sns')
            body = json.loads(request.body.decode('utf-8'))
            total_score = 0
            count = 0
            for sentence in body['user_sns']:
                depression_score = depression_predict(sentence, stopwords, depression_tokenizer, model, max_len)
                if depression_score >= 91:
                    count += 1
            result = round(count / len(body['user_sns']))
            return JsonResponse({'score': result})
        except:
            err = traceback.format_exc()
            raise Http404(str(err))

def chatbot(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user_chat = body['chat']
            predicted_reply = predict_reply(user_chat, START_TOKEN, END_TOKEN, MAX_LENGTH, chatbot_tokenizer, C_model)
            return JsonResponse({'reply': predicted_reply})
        except:
            err = traceback.format_exc()
            raise Http404(str(err))
