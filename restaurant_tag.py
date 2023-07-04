import pandas as pd
from zhon.hanzi import punctuation
from zhon.hanzi import non_stops
from zhon.hanzi import stops
from hanziconv import HanziConv
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

def remove_stopwords(text, stopwords):
    # 移除停用詞
    words = text.split(' ')
    filtered_words = [word for word in words if word not in stopwords]
    processed_text = " ".join(filtered_words)
    return processed_text

def preprocess_text(text):
    # 移除標點符號
    text = re.sub(r'[^\w\s]', '', text)

    # 移除數字
    text = re.sub(r'\d+', '', text)

    # 移除特殊字元（例如網址連結）
    text = re.sub(r'http\S+', '', text)

    # 去除多餘的空格
    text = re.sub(r'\s+', ' ', text)

    return text

def data_processing(dfr):

    with open("models/stopwords_zh-tw.txt", encoding="utf-8") as fin:
        stopwords = fin.read().split("\n")[1:]
    tokenized=[]
    for i in range(len(dfr['text'])):
        s_to= HanziConv.toSimplified(dfr['text'][i])
        cuts = "/".join(jieba.cut(s_to))
        sen=cuts.split('/')
        sen_tot =[HanziConv.toTraditional(i) for i in sen]
        tokenized.append(' '.join(sen_tot))
    dfr['tokenized']=tokenized

    filter = []
    for text in dfr['tokenized']:
        text1 = remove_stopwords(text, stopwords)
        filter.append(preprocess_text(text1))
    dfr['filtered']=filter

    # tfidf_model = pd.read_pickle('models/tdidf1.pkl')
    vectorizer = pickle.load(open("models/tfidf1.pkl", "rb"))
    x = vectorizer.transform(dfr['filtered'])

    return x

def run_classification(raw, name):
    df = pd.DataFrame.from_dict(raw)
    df = df[['text']]
    df['text'] = df['text'] + name
    x = data_processing(df)
    loaded_model = joblib.load('models/tag_svc_model')
    result = loaded_model.predict(x)
    tag_dict = { 0:"中式料理", 1:"其他料理", 2:"台式料理", 3:"日式料理", 4:"法式料理", 5:"泰式料理", 6:"美式料理", 7:"義式料理", 8:"韓式料理"}
    tag = []
    for i in result:
        if tag_dict[i] in tag:
            continue
        tag.append(tag_dict[i])

    return tag

