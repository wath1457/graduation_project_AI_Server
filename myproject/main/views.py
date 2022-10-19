from tkinter.tix import MAX
from django.shortcuts import render, HttpResponse, redirect
from main.apps import MainConfig

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
    # stopwords, depression_tokenizer, model, max_len = dm_init()
    print('우울증 분석 모델 로드 완료')
    START_TOKEN, END_TOKEN, MAX_LENGTH, chatbot_tokenizer, C_model = cm_init()
    print('챗봇 모델 로드 완료')
    setting_completed = True
else:
    pass

def index(request):
    return render(request, "main/index.html")

def depression(request):
    return HttpResponse(testhtml())

def chatbot(request):
    predicted_reply = predict_reply('오늘 뭐하지?',START_TOKEN, END_TOKEN, MAX_LENGTH, chatbot_tokenizer, C_model)
    return HttpResponse(testhtml2())

def testhtml():
        page = f'''
        <h2>{depression_predict('너무 행복하다', stopwords, depression_tokenizer, model, max_len)}</h2>
        '''
        return page
def testhtml2():
        page = f'''
        <h2>결과 : {predict_reply('오늘 뭐하지?', START_TOKEN, END_TOKEN, MAX_LENGTH, chatbot_tokenizer, C_model)}</h2>
        '''
        return page


# def chat():
#     score = 0
#     params = request.get_json()
#     reply = predict_reply(params['user_chat'])
#     score = predict_emotion(params['user_chat'])
#     email = params['user_email']

#     headers = {'Content-Type' : 'application/json; charset=utf-8'}
#     data = {'email' : email, 'score' : score}
    
#     # requests.post(url, data=json.dumps(data), headers=headers)
#     if score == 1:
#         print("점수 상승(긍정)")
#         requests.put(emo_url + 'plus/' + email, data=json.dumps(data), headers = headers)
#     elif score == -1:
#         print("점수 하락(부정)")
#         requests.put(emo_url + 'minus/' + email, data=json.dumps(data), headers = headers)
        
#     return jsonify({"reply" : reply})