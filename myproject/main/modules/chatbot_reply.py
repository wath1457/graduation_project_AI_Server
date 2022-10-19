import tensorflow as tf
import re

def preprocess_sentence(sentence):
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = sentence.strip()
    return sentence

def evaluate(sentence, START_TOKEN, END_TOKEN, MAX_LENGTH, tokenizer, C_model):
    sentence = preprocess_sentence(sentence)

    sentence = tf.expand_dims(
        START_TOKEN + tokenizer.encode(sentence) + END_TOKEN, axis=0)

    output = tf.expand_dims(START_TOKEN, 0)

    # 디코더의 예측 시작
    for i in range(MAX_LENGTH):
      predictions = C_model(inputs=[sentence, output], training=False)

      # 현재(마지막) 시점의 예측 단어를 받아온다.
      predictions = predictions[:, -1:, :]
      predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

      # 만약 마지막 시점의 예측 단어가 종료 토큰이라면 예측을 중단
      if tf.equal(predicted_id, END_TOKEN[0]):
        break

      # 마지막 시점의 예측 단어를 출력에 연결한다.
      # 이는 for문을 통해서 디코더의 입력으로 사용될 예정이다.
      output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0)

def predict_reply(sentence, START_TOKEN, END_TOKEN, MAX_LENGTH, tokenizer, C_model):
    prediction = evaluate(sentence, START_TOKEN, END_TOKEN, MAX_LENGTH, tokenizer, C_model)

    predicted_sentence = tokenizer.decode(
        [i for i in prediction if i < tokenizer.vocab_size])

    print('Input: {}'.format(sentence))
    print('Output: {}'.format(predicted_sentence))

    return predicted_sentence