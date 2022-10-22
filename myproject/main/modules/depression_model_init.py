from django.conf import settings
from keras_preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from konlpy.tag import Mecab
from keras.preprocessing.text import Tokenizer
from keras.models import load_model


def dm_init():
    total_data = pd.read_csv(str(settings.BASE_DIR) + '/dataset/tweets_dataset_18.csv', encoding='cp949')
    total_data = total_data.drop(['Datetime', 'Unnamed: 0'], axis = 1)
    total_data.drop_duplicates(subset=['Text'], inplace=True)
    train_data, test_data = train_test_split(total_data, test_size = 0.2, random_state = 42)


    train_data['Text'] = train_data['Text'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)
    train_data['Text'].replace('', np.nan, inplace=True)

    stopwords = []
    file = open(str(settings.BASE_DIR) + '/stopword.txt', "r", encoding="utf-8")
    while True:
        line = file.readline()
        if line == '':
            break
        stopwords.append(line.strip('\n'))
    file.close()

    mecab = Mecab() 

    train_data['tokenized'] = train_data['Text'].apply(mecab.morphs)
    train_data['tokenized'] = train_data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])


    X_train = train_data['tokenized'].values


    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)

    threshold = 2
    total_cnt = len(tokenizer.word_index) # 단어의 수
    rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트

    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        if(value < threshold):
            rare_cnt = rare_cnt + 1
    vocab_size = total_cnt - rare_cnt + 2
    tokenizer = Tokenizer(vocab_size, oov_token = 'OOV')
    tokenizer.fit_on_texts(X_train)

    model = load_model(str(settings.BASE_DIR) + '/model/BiLSTM_model_18')
    max_len = 55
    return stopwords, tokenizer, model, max_len