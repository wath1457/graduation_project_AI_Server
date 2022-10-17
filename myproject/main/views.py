from django.shortcuts import render, HttpResponse, redirect
from main.apps import MainConfig

from .modules.depression_model_init import dm_init
from .modules.depression_predict import depression_predict

setting_completed = False
stopwords = None
tokenizer = None
model = None
max_len = None


if setting_completed != True:
    stopwords, tokenizer, model, max_len = dm_init()
    setting_completed = True
else:
    pass

def index(request):
    return render(request, "main/index.html")

def depression(request):
    return HttpResponse(testhtml())

def testhtml():
        page = f'''
        <h2>{depression_predict('너무 행복하다', stopwords, tokenizer, model, max_len)}</h2>
        '''
        return page