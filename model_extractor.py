#!/usr/bin/env python
# coding: utf-8

# In[25]:


# coding: utf-8
import argparse
import codecs
import lxml.etree as ET
import os
import regex


from konlpy.tag import Kkma 
kkma = Kkma()
    
max_corpus_size = 1000000000
fname = "{}wiki-20190120-pages-articles-multistream.xml".format('ko')    


# In[26]:


def clean_text(text):

    
    text = regex.sub("(?s)<ref>.+?</ref>", "", text) # remove reference links
    text = regex.sub("(?s)<[^>]+>", "", text) # remove html tags
    text = regex.sub("&[a-z]+;", "", text) # remove html entities
    text = regex.sub("(?s){{.+?}}", "", text) # remove markup tags
    text = regex.sub("(?s){.+?}", "", text) # remove markup tags
    text = regex.sub("(?s)\[\[([^]]+\|)", "", text) # remove link target strings
    text = regex.sub("(?s)\[\[([^]]+\:.+?]])", "", text) # remove media links  
    text = regex.sub("[']{5}", "", text) # remove italic+bold symbols
    text = regex.sub("[']{3}", "", text) # remove bold symbols
    text = regex.sub("[']{2}", "", text) # remove italic symbols
    

    text = regex.sub(u"[^ \r\n\p{Hangul}.?!]", " ", text) 
    text = regex.sub("[ ]{2,}", " ", text) # Squeeze spaces.
    return text


# In[27]:


def sentence_segment(text):

    sents = regex.split("([.?!])?[\n]+|[.?!] ", text)
    return sents
        
def word_segment(sent):
    words = [word for word, _ in kkma.pos(sent)]  
    
    return words


# In[28]:


def build_corpus():
    global max_corpus_size, fname
    with codecs.open("{}.txt".format('ko'), 'w', 'utf-8') as fout:
        i = 1
        j = 1
        ns = "{http://www.mediawiki.org/xml/export-0.10/}" # namespace
        for _, elem in ET.iterparse("{}".format(fname), tag=ns+"text"):
            running_text = elem.text
            try:
                running_text = clean_text(running_text)
                sents = sentence_segment(running_text)
                for sent in sents:
                    if sent is not None:
                        words = word_segment(sent)
                        if len(words) > 10:
                            fout.write(" ".join(words) + "\n")
                                
            except:
                continue 
            elem.clear() 
            if i % 1000 == 0: 
                print(i)  #show progress
                fsize = os.path.getsize("{}.txt".format('ko'))
                if fsize > max_corpus_size:
                    break
            i += 1


# In[ ]:


if __name__ == "__main__":
    build_corpus()
    
    print("Done")


# In[ ]:




