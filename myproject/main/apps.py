from lib2to3.pgen2 import token
from django.apps import AppConfig
import os

model = None
tokenizer = None
stopwords = None
max_len = None

a = 123
b = 456

def first_init():
    global a
    global b
    return a, b


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'    
    
    # def ready(self):
    #     if not os.environ.get('APP'):
    #         os.environ['APP'] = 'True'
            