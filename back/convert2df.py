import pandas as pd
from json.tool import main
import re
import json
import time
import pandas as pd
# import pytorch_lightning as pl
from nltk.tokenize import TweetTokenizer
import emoji
abbre_dict = None
stopwords = None
with open("./datas/abbreviation.json", "r", encoding="utf-8") as f:
    abbre_dict = dict(json.load(f))
with open("./datas/stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = f.readlines()
    for i in range(len(stopwords)):
        stopwords[i]=stopwords[i][:-1]
tweet_tokenizer = TweetTokenizer()  


def list2df(ini_list):
    df = pd.DataFrame(ini_list[1:], columns=ini_list[0], dtype=str)
    try:
        static_info = df[['event','mid','time', 'content']].describe()
    except:
        return [{"data_count":"don't enough keys"}]
    print(static_info)
    df = df[ini_list[0]]
    print(df.head)
    df = preprocess(df)
    df.to_csv("./temp_data/trigger.csv")
    time_list = df['time'].tolist()
    earlist = float(min(time_list))
    latest = float(max(time_list))
    time_earlist = time.localtime(earlist )
    time_earlist = time.strftime("%Y-%m-%d %H:%M:%S", time_earlist)
    time_latest = time.localtime(latest)
    time_latest = time.strftime("%Y-%m-%d %H:%M:%S", time_latest)
    res = [{"data_count":int(static_info.iat[0,0]),"top_event":str(static_info.iat[2,0]),"freq":int(static_info.iat[3,0]),"earlist":time_earlist,"latest":time_latest}]
    # print("static_res")
    # print(res)
    return res
def clean_word(word):
    word = word.lower()
    if word and word[0] != "@":
        # split with capitalized letter
        word = re.sub(r'([a-z]+|\d+)([A-Z])', r'\1 \2', word)
        
    ## extend the abbreviated words
    word = " ".join([abbre_dict.get(sub_word, 0) if abbre_dict.get(sub_word, 0) else sub_word for sub_word in word.split(" ")])
    if word in stopwords:
        return ""
    return word
def sentence4dl(sentence):
    '''function to clean single sentence'''
    sentence = re.sub('[hH]ttp\S+|www\.\S+', 'HTTPURL', sentence)  # remove url        
    sentence = re.sub('<.*?>+', '', sentence) # remove html tags
    sentence = re.sub('@\S*', '@USER', sentence) # remove @
    sentence = emoji.demojize(sentence) # convert emoji into text                   
    sentence = re.sub('\s[0-9]+\s', '', sentence) # remove numbers   
    sentence4dl = re.sub('[\.\+\-\?\'\\,/$%&#:;^_`{|}~><“”]', '', sentence) # remove special tokens 
    
    return sentence4dl

def sentence4wordcount(sentence):
    sentence = ' '.join(tweet_tokenizer.tokenize(sentence))   
    sentence4wordcount = ' '.join([clean_word(word) for word in sentence.split()])  
    return sentence4wordcount

def preprocess(df):
    df['time'].apply(float)
    print(df.shape)
    # dataset=df
    print('Cleaning text...')
    # clean_text_field = 'content4dl'
    df['content4dl'] = df['content'].apply(sentence4dl)
    df['content4wordcount'] = df['content4dl'].apply(sentence4wordcount)
    return df



if __name__=="__main__":
    ini_list = [
      [
    "event",
    "cid",
    "mid",
    "pid",
    "time",
    "date",
    "content",
    "detect",
    "verify",
    "stance",
    "stance_",
    "trigger",
    "trigger_binary"
],
      [
    "sydneysiege",
    "544359578612559872",
    "544359578612559872",
    "None",
    "1418620411.0",
    "2014-12-15 05:13:31",
    "UPDATE: Police confirm they have made contact with the gunman. There are no reported injuries. #9News http://t.co/nZWY5ZyWBe",
    "1",
    "1",
    "-1",
    "3",
    "1",
    "1"
],
     [
    "sydneysiege",
    "544359578612559872",
    "544360321234640896",
    "544359578612559872",
    "1418620588.0",
    "2014-12-15 05:16:28",
    "@RT_com: #Ferguson cops beat innocent man, then charged him with bleeding on their uniforms http://t.co/r5mdmi0Eqv http://t.co/4aroIyKt6m",
    "1",
    "1",
    "-1",
    "0",
    "0",
    "0"
]
    ]
#     ini_list = [
#       [
#     "event",
#     "cid",
    
# ],
#       [
#     "sydneysiege",
#     "544359578612559872",
    
# ],
#      [
#     "sydneysiege",
#     "544359578612559872",
    
# ]
#     ]
    list2df(ini_list)
