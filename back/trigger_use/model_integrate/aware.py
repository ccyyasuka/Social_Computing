﻿import torch
from torch import nn
from torch.nn import functional as F

class Integrate(nn.Module):
    def __init__(self, args, input_size=None):
        super().__init__()

    @staticmethod
    def _transform_mes_into_cas(message, structure):#把节点数量补齐 比如batch里有2个cas 一个有12个节点 1个有27个节点 那就都变成27个的序列 返回54*600和54*4的矩阵
        cids, mids, pids, time = structure
        # split according to pid=='None'
        source_index = [i for i in range(len(pids)) if pids[i] == 'None']
        temp = source_index + [len(pids)]
        cas_index = [list(range(temp[i], temp[i+1]))
                    for i in range(len(source_index))]
        cas_size = [len(index) for index in cas_index]
        max_cas_size = max(cas_size)
        cas_batch = [message[index] for index in cas_index]
        # padding into the same length
        cas_batch = [F.pad(item, (0, 0, 0, max_cas_size-item.size(0)),
                        'constant', 0) for item in cas_batch]
        # stack to form uniform tensor
        cas_all = torch.stack(tuple(cas_batch), dim=0)
        cas_mask = torch.Tensor([[1]*item+[0]*(max_cas_size-item)
                                for item in cas_size]).long().to(message.device)#记录哪些节点是真实节点 哪些是额外加的补齐的节点
        return cas_all, cas_mask, source_index

    def aware_pooling(self, x, x_mask, weights):
        """
        x: (bsz, seq_len, input_size)5 56 600 所有节点的表示（里面会有补齐的）
        x_mask: (bsz, seq_len)5 56
        weights: (bsz, seq_len, 1)5 56 4 每个节点预测对应属性的概率
        => s: (bsz, input_size)-pooling output, u: (bsz, seq_len)-pooling weights
        """
        mm_tensor = torch.Tensor([0,1,1,1]).to(weights.device)
        weight_score = torch.matmul(weights, mm_tensor)  # (bsz, seq_len)
        u = weight_score.masked_fill_(x_mask==0, -1e9)        
        u = F.softmax(u, dim=-1)#(bsz,len) 粗浅理解为各个节点属于后三类节点的概率
        u_ = u.unsqueeze(-1).expand(-1, -1, x.size(-1))#u_是权重u复制了600次 (bsz,len,600)
        s = torch.sum(x*u_, dim=1) #x*u_代表把各个节点加权求和
        return s, u

    def forward(self, mes_update, yv, structure, *args, **kargs):
        '''ingerate mesences to form cas-level representation
        mes_update(torch.Tensor): updated message representation, shape: (batch_mes, hidden)
        '''
        yt_pred = kargs.pop('yt_pred', None)
        cas_all, cas_mask, source_index = self._transform_mes_into_cas(
            mes_update, structure)  # (batch_cas, max_cas_size, hidden), (batch_cas, max_cas_size)
        yt_pred, cas_mask, source_index = self._transform_mes_into_cas(yt_pred, structure)
        cas, weights = self.aware_pooling(cas_all, cas_mask, yt_pred) # (batch_cas, hidden)
        yv_cas = yv[source_index]#weight可以可视化一下
        return cas, yv_cas