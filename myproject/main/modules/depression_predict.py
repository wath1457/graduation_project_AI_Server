from eunjeon import Mecab
from keras_preprocessing.sequence import pad_sequences
import re

def depression_predict(new_sentence, stopwords, tokenizer, model, max_len):
    mecab = Mecab()
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    new_sentence = mecab.morphs(new_sentence) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(model.predict(pad_new)) # 예측
    if(score > 0.5):
        return("{:.2f}% 확률로 우울증 트윗입니다.".format(score * 100))
    else:
        return("{:.2f}% 확률로 보통 트윗입니다.".format((1 - score) * 100))