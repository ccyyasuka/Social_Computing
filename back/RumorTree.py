from json.tool import main    #导入包慢使用vpn就行
import re
import json
import pandas as pd
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
from trigger_use.myuse import tree_predict


def rumor_analysis():
    res = tree_predict()
    print(res)
    return res
    # reserve useful fields
    
        

if __name__=="__main__":
    # word_count(1418620411.0,1420820486.0,135)
    rumor_analysis()  




