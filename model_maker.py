#!/usr/bin/env python
# coding: utf-8

# In[11]:


# coding: utf-8
import nltk
import os
import codecs
import argparse
import numpy as np

lcode = 'ko'
vector_size = 100
window_size = 5
vocab_size = 1000
num_negative = 5


# In[12]:


def get_min_count(sents):
    global vocab_size
    from itertools import chain
     
    fdist = nltk.FreqDist(chain.from_iterable(sents))
    min_count = fdist.most_common(vocab_size)[-1][1] #find most min count in the tokens
    
    return min_count


# In[13]:


def make_wordvectors():
    global lcode
    import gensim
     
    sents = []
    with codecs.open('{}.txt'.format(lcode), 'r', 'utf-8') as fin:
        while True:
            line = fin.readline()
            if not line: break
             
            words = line.split()
            sents.append(words)
 
    min_count = get_min_count(sents)
    model = gensim.models.Word2Vec(sents, size=vector_size, min_count=min_count,
                                   negative=num_negative, 
                                   window=window_size) #create model
    
    model.save('{}.bin'.format(lcode))


# In[14]:


if __name__ == "__main__":
    make_wordvectors()


# In[ ]:




