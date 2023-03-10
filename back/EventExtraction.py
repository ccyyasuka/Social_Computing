from openie import StanfordOpenIE
import spacy
import neuralcoref
import os
import time
import re

nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)

properties = {
    'openie.affinity_probability_cap': 2 / 3,
}

def openie2triple(text):
    text = nlp(text)._.coref_resolved
    
    print(text)
    with StanfordOpenIE(properties=properties) as client:
        triples = []
        cur_res = client.annotate(text)
        # for triple in cur_res:
        #     triples.append(triple)
        # subject = []
        # relation = []
        # new_triples = {}
        # for triple in triples:
        #     if [triple['subject'], triple['relation']] in subject:
        #         if len(triple['object']) > len(new_triples[(triple['subject'], triple['relation'])]):
        #             new_triples[(triple['subject'], triple['relation'])] = triple['object']
        #     else:
        #         new_triples[(triple['subject'], triple['relation'])] = triple['object']
        #         subject.append([triple['subject'], triple['relation']])
    print(cur_res)
    fin_res = triple2json(cur_res)
    print(fin_res)
    return fin_res

def triple2json(data):
    
    # res = {"name":"sentence","children":[]}
    children = []
    flag1 = 0
    flag2 = 0
    flag3 = 0
    for i in range(len(data)):
        cur_triple = data[i]
        #先遍历主语
        for j in range(len(children)):
            if children[j]["name"]==cur_triple["subject"]:
                flag1 = 1
                for k in range(len(children[j]["children"])):
                    if children[j]["children"][k]["name"]==cur_triple["relation"]:
                        flag2=1
                        for l in range(len(children[j]["children"][k]["children"])):
                            if children[j]["children"][k]["children"][l]["name"]==cur_triple["object"]:
                                flag3 = 1
                                children[j]["children"][k]["children"][l]["size"]+=1
                            
                        if flag3==0:
                            children[j]["children"][k]["children"].append(
                                {"name":cur_triple["object"],
                                 "size":1}
                                )
                        flag3=0
                if flag2==0:
                    children[j]["children"].append(
                        {"name":cur_triple["relation"],
                         "children":[
                          {"name":cur_triple["object"],
                           "size":1}
                          ]
                        })
                flag2 = 0
        if flag1==0:
            children.append(
                {"name":cur_triple["subject"],
                 "children":[
                     {"name":cur_triple["relation"],
                      "children":[
                          {"name":cur_triple["object"],
                           "size":1}
                          ]
                      }
                     ]
                 })
        flag1 = 0
    # first_rem = {"sentence":[]}
    # second_rem = {}
    # third_rem = {}
    # for i in range(len(data)):
    #     cur_triple = data[i]
    #     if cur_triple["subject"] not in first_rem["sentence"]:
    #         children.append(
    #             {"name":cur_triple["subject"],
    #              "children":[
    #                  {"name":cur_triple["relation"],
    #                   "children":[
    #                       {"name":cur_triple["object"],
    #                        "size":1}
    #                       ]
    #                   }
    #                  ]
    #              })
    #         first_rem['sentence'].append(cur_triple["subject"])
            
    #     else:
    #         for j in range(len(children)):
    #             if children[j]["name"]==cur_triple["subject"]
    #         if cur_triple["relation"] not in second_rem[cur_triple["subject"]]:
                
    res = {"name":"sentence","children":children}               
    return res
    




if __name__ == '__main__':


    data = 'Steve Jobs attended Reed College in 1972 before withdrawing that same year. In 1974, he traveled through India seeking enlightenment before later studying Zen Buddhism.'
    # print(nlp(data)._.coref_resolved)
    t1 = time.time()
    res = openie2triple(data)
    print(res)
    
    # for i in range(1000):
    #     print(i)
    #     print()
    t2 = time.time()
    print(t2-t1)
    