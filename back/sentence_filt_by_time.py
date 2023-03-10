import time
import random
import pandas as pd
def sentence_filt_by_time(dt,selected_event):
    if len(dt)==10:
        dt1 = dt+" 00:00:00"
        dt2 = dt+" 23:59:59"
    else:
        dt = dt[:13]
        dt1 = dt+":00:00"
        dt2 = dt+":59:59"
    # dt = "2023-01-01 08:00:00"
    print("dtdtdtdtdtddtdtdtdtdtdtdtdtdtdt")
    print(dt1)
    # 转换成时间数组
    timeArray1 = time.strptime(dt1, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    start = time.mktime(timeArray1)
    timeArray2 = time.strptime(dt2, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    end = time.mktime(timeArray2)
    df = pd.read_csv("./temp_data/sentiment_res.csv")
    # reserve useful fields
    fields = ["mid",'event','time', 'content','$new_sentiment_pre']
    df = df[fields]
    # reset dataframe index
    df['time'].apply(float)
    df.index = df['mid']
    df.index.name = None
    print(df.shape)
    # dataset=df
    df=df.loc[(df["time"]>=start)&(df["time"]<=end)&(df["event"]==selected_event),fields]
    mid_list = df["mid"].tolist()
    content_list = df["content"].tolist()
    sentiment_list = df["$new_sentiment_pre"].tolist()
    res = []
    for i in range(len(content_list)):#这里要改，预测之后把情感极性保存在本地
      if sentiment_list[i]==0:
        res.append({"mid":mid_list[i],"content":content_list[i],"tags":["neg"]})
      else:
        res.append({"mid":mid_list[i],"content":content_list[i],"tags":["pos"]})
    return res
   
if __name__ == '__main__':
    sentence_filt_by_time("2014-12-16 08","sydneysiege")
    
    
    


