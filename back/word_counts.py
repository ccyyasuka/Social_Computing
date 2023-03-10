from json.tool import main
import re
import json
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from torch.utils.data._utils.collate import default_collate
# import pytorch_lightning as pl
from nltk.tokenize import TweetTokenizer
import emoji
import os
os.chdir("/data-14T/zhangyixing/SocialComputing/Social_Computing/back")
tweet_tokenizer = TweetTokenizer()
with open("./datas/abbreviation.json", "r", encoding="utf-8") as f:
    abbre_dict = dict(json.load(f))
with open("./datas/stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = f.readlines()
    for i in range(len(stopwords)):
        stopwords[i]=stopwords[i][:-1]
    
        
def clean_word(word):
    if word=="the":
        print()
    word = word.lower()
    if word and word[0] != "@":
        # split with capitalized letter
        word = re.sub(r'([a-z]+|\d+)([A-Z])', r'\1 \2', word)
        
    ## extend the abbreviated words
    word = " ".join([abbre_dict.get(sub_word, 0) if abbre_dict.get(sub_word, 0) else sub_word for sub_word in word.split(" ")])
    if word in stopwords:
        
        return ""
    return word
def clean_sentence(sentence):
    '''function to clean single sentence'''
    sentence = re.sub('[hH]ttp\S+|www\.\S+', 'HTTPURL', sentence)  # remove url        
    sentence = re.sub('<.*?>+', '', sentence) # remove html tags
    sentence = re.sub('@\S*', '@USER', sentence) # remove @
    sentence = emoji.demojize(sentence) # convert emoji into text                   
    sentence = ' '.join(tweet_tokenizer.tokenize(sentence))      
    sentence = ' '.join([clean_word(word) for word in sentence.split()])   
    sentence = re.sub('\s[0-9]+\s', '', sentence) # remove numbers   
    sentence = re.sub('[\.\+\-\?\'\\,/$%&#:;^_`{|}~><“”]', '', sentence) # remove special tokens    
    return sentence

def word_count(start,end,topk):
    print('Loading dataset...')
    print(start)
    print(end)
    print(topk)
    df = pd.read_csv("./temp_data/trigger.csv")
    # reserve useful fields
    fields = ['event','mid','time', 'content4wordcount']
    df = df[fields]
    # reset dataframe index
    df['time'].apply(float)
    df.index = df['mid']
    df.index.name = None
    print(df.shape)
    # dataset=df
    df=df.loc[(df["time"]>=start)&(df["time"]<=end),fields]
    df = df.dropna(axis=0, how='all', subset=["content4wordcount"])
    # print('Cleaning text...')
    # clean_text_field = 'content_clean'
    # df[clean_text_field] = df['content'].apply(clean_sentence)
    count_dic = {}
    for index, row in df.iterrows():
        event = row['event']
        content = row["content4wordcount"]
        # if str(content)!="nan":
        cur_words = content.split(" ")
        for i in cur_words:
            if i!="":
                cur_word = event+"/"+i
                if cur_word not in count_dic.keys():
                    count_dic[cur_word]=1
                else:
                    count_dic[cur_word]+=1
    res = []
    for i in count_dic.keys():
        value = count_dic[i]
        res.append({"name":i,"value":value})
        
    res = sorted(res,key=lambda x:x["value"],reverse=True)
    print("word_count_res")
    print(res[:topk])
    return res[:topk]
        

if __name__=="__main__":
    # word_count(1418620411.0,1420820486.0,135)
    word_count(1415088354.772,1435305954.772,55)  




