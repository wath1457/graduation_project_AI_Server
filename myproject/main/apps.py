from django.apps import AppConfig
import os
import pandas as pd
from django.conf import settings

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    def ready(self):
        if not os.environ.get('APP'):
            os.environ['APP'] = 'True'
            total_data = pd.read_csv(str(settings.BASE_DIR) + '/dataset/tweets_dataset_18.csv', encoding='cp949')
            print('hello')