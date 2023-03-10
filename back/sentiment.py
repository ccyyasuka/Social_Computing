from json.tool import main    #导入包慢使用vpn就行
import re
import json
import pandas as pd
# import torch
# from torch.utils.data import Dataset, DataLoader
# from torch.utils.data._utils.collate import default_collate
# import pytorch_lightning as pl
# from nltk.tokenize import TweetTokenizer
# import emoji
import os



import time
# import process_imdb
from torch.utils.data import TensorDataset, DataLoader
import torch
# import torch.nn as nn
# from torch import optim
import logging
# import numpy as np
# import pickle
from transformers import BertForSequenceClassification, AdamW, BertTokenizer, BertModel
device_id = 3
MAXLEN = 512 - 2
BATCHSIZE = 256
params_dir = './model/bert_base_model_beta.pkl'
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') # 加载base模型的对应的切词器



# os.chdir("/data-14T/zhangyixing/SocialComputing/vue2_flask")
# tweet_tokenizer = TweetTokenizer()
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
# def clean_sentence(sentence):
#     '''function to clean single sentence'''
#     sentence = re.sub('[hH]ttp\S+|www\.\S+', 'HTTPURL', sentence)  # remove url        
#     sentence = re.sub('<.*?>+', '', sentence) # remove html tags
#     sentence = re.sub('@\S*', '@USER', sentence) # remove @
#     sentence = emoji.demojize(sentence) # convert emoji into text                   
#     sentence = ' '.join(tweet_tokenizer.tokenize(sentence))      
#     sentence = ' '.join([clean_word(word) for word in sentence.split()])   
#     sentence = re.sub('\s[0-9]+\s', '', sentence) # remove numbers   
#     sentence = re.sub('[\.\+\-\?\'\\,/$%&#:;^_`{|}~><“”]', '', sentence) # remove special tokens    
#     return sentence


def convert_text_to_ids(tokenizer, sentence, limit_size=MAXLEN):
    t = tokenizer.tokenize(sentence)[:limit_size]
    encoded_ids = tokenizer.encode(t)
    if len(encoded_ids) < limit_size + 2:
        tmp = [0] * (limit_size + 2 - len(encoded_ids))
        encoded_ids.extend(tmp)
    return encoded_ids
def get_att_masks(input_ids):
    atten_masks = []
    for seq in input_ids:
        seq_mask = [float(i > 0) for i in seq]
        atten_masks.append(seq_mask)
    return atten_masks
def predict(logits):
    res = torch.argmax(logits, dim=1)  # 按行取每行最大的列下标
    return res
  
def multi_predict(out_test, net, device):
    # out_test=["I hate you.", "I think it is beautiful."]
    input_ids2 = []
    for sen in out_test:
        if sen.isspace():
            sen = "good"
        input_ids2.append(convert_text_to_ids(tokenizer, sen))
    # input_ids2 = [convert_text_to_ids(tokenizer, sen) for sen in out_test]
    # input_labels2 = torch.unsqueeze(torch.tensor(process_imdb.test_labels), dim=1)
    atten_tokens_eval = get_att_masks(input_ids2)
    test_set = TensorDataset(torch.LongTensor(input_ids2), torch.LongTensor(atten_tokens_eval),
                        #  torch.LongTensor(input_labels2)
                         )
    test_loader = DataLoader(dataset=test_set,
                            batch_size=BATCHSIZE )
    
    # correct = 0
    # total = 0
    res = []
    with torch.no_grad():
        for batch_idx, (data, mask) in enumerate(test_loader):
            logging.info("test batch_id=" + str(batch_idx))

            data, mask = data.to(device), mask.to(device)
            output = net(data, token_type_ids=None, attention_mask=mask)  # 调用model模型时不传入label值。
            # output的形式为（元组类型，第0个元素是每个batch中好评和差评的概率）
            # print(output[0],label)
            cur_res = predict(output[0]).tolist()
            print(cur_res)
            res += cur_res
    return res
    




def senti_analysis(start,end,selected_event,time_span,proportion):
    print('Loading dataset...')
    print(start)
    print(end)
    torch.cuda.set_device(device_id)
    df = pd.read_csv("./temp_data/trigger.csv")
    # reserve useful fields
    fields = ['event','mid','time', 'content','content4dl']
    df = df[fields]
    # reset dataframe index
    df['time'].apply(float)
    df.index = df['mid']
    df.index.name = None
    print(df.shape)
    # dataset=df
    df = df.sample(frac=proportion)
    df=df.loc[(df["time"]>=start)&(df["time"]<=end)&(df["event"]==selected_event),fields]
    df = df.dropna(axis=0, how='all', subset=["content4dl"])
    # print('Cleaning text...')
    # clean_text_field = 'content_clean'
    # df[clean_text_field] = df['content'].apply(clean_sentence)
    t1 = time.time()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net=BertForSequenceClassification.from_pretrained("bert-base-uncased")#慢
    net.load_state_dict(torch.load(params_dir))#慢
    net.eval()#慢
    net = net.to(device)#慢
    t2 = time.time()
    print("time!!!!!!!!!!!!!!!!!")
    print(t2-t1)
    
    unpre_sen = []
    for index, row in df.iterrows():
        unpre_sen.append(row["content4dl"])
    print(len(unpre_sen))
    pre_label = multi_predict(unpre_sen, net, device)
    print("labels!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(pre_label)
    df.insert(4,column="$new_sentiment_pre",value = pre_label)
    df.to_csv("./temp_data/sentiment_res.csv")
    count_dic = {}
    counter = 0
    for index, row in df.iterrows():
        cur_time = row['time']
        loc_time = time.localtime(cur_time)
        if time_span=="hour":
            cur_day = time.strftime("%Y-%m-%d %H:%M:%S",loc_time)[:13]+":00"
        if time_span=="day":
            cur_day = time.strftime("%Y-%m-%d %H:%M:%S",loc_time)[:10]
        # content = row["content"]
        # res = multi_predict([content], net, device)[0]
        # print(res)
        if cur_day not in count_dic.keys():
            count_dic[cur_day]=[0,0]
        count_dic[cur_day][0]+=1 #总数+1
        if pre_label[counter] == 1:
            count_dic[cur_day][1]+=1
        counter+=1
    final_res = []
    for i in count_dic.keys():
        if count_dic[i][0]==0:
            continue
        final_res.append({"date":i,"pos":count_dic[i][1]/count_dic[i][0],"neg":1-count_dic[i][1]/count_dic[i][0]})
    print(final_res) 
    return final_res   
        
        # event = row['event']
        # content = row[clean_text_field]
        # cur_words = content.split(" ")
        # for i in cur_words:
        #     if i!="":
        #         cur_word = event+"/"+i
        #         if cur_word not in count_dic.keys():
        #             count_dic[cur_word]=1
        #         else:
        #             count_dic[cur_word]+=1
    # res = []
    # for i in count_dic.keys():
    #     value = count_dic[i]
    #     res.append({"name":i,"value":value})
        
    # res = sorted(res,key=lambda x:x["value"],reverse=True)
    # print(res[:topk])
    # return res[:topk]
        

if __name__=="__main__":
    # word_count(1418620411.0,1420820486.0,135)
    senti_analysis(1415088354.772,1435305954.772,"sydneysiege","hour",0.5)  




