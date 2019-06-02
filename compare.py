#!/usr/bin/env python
# coding: utf-8

# In[69]:


# -*- coding: utf-8 -*-
import sys
import json
import gensim
import os
from konlpy.tag import Okt

okt = Okt()
model = gensim.models.Word2Vec.load("./../model/ko.bin")


# In[57]:


def extract_sentence(keywords, sens):
    
    exts = {}
    
    for v in range(len(keywords)):
        scores = []
      
        for i in range(len(sens)):
            comparee = okt.nouns(sens[i])
            total_score=0
            excepts = 0
            for t in range(len(comparee)):
                try:
                    score=model.wv.n_similarity(comparee[t],keywords[v])
                    total_score+=score         
                except KeyError :
                    excepts+1
            if len(comparee)>excepts and total_score/(len(comparee)-excepts)>0.30:
                scores.append(total_score)
            else :
                scores.append(-10)
                
        exts[keywords[v]] = sens[scores.index(max(scores))]
        
    return exts


# In[3]:


# def remove_duplicates(list):
#     temp = []
#     for item in list:
#         if item not in temp:
#             temp.append(item)
#     return temp


# In[58]:


def init():
    path = sys.argv[1]
    
    import ast
    
    with open(path,'r') as inf:
        sens =ast.literal_eval(inf.read())
    
    keywords = []
    for i in range(2,len(sys.argv)):
        keywords.append(str(sys.argv[i]))
        
    exts=extract_sentence(keywords, sens)
    os.remove(path)
    
    path=path[0:len(path)-4]+".json"
    fp = open(path,'w')
    
    json.dump(exts,fp,ensure_ascii=False)
    fp.close()
    
#     return exts


# In[5]:


if __name__ is "__main__":
    init()


# In[70]:


# if __name__ is "__main__":
#     path = './nonmun.txt'
#     import ast
    
#     with open(path,'r') as inf:
#         sens =ast.literal_eval(inf.read())
        
#     keywords = []
#     for i in range(0,3):
#         keywords.append(input())

        
#     exts=extract_sentence(keywords, sens)
#     os.remove(path)
    
#     path=path[0:len(path)-4]+".json"
#     fp = open(path,'w')
    
#     json.dump(exts,fp,ensure_ascii=False)
#     fp.close()
    

        

