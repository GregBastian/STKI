# -*- coding: utf-8 -*-
"""
Created on Fri May 11 16:08:39 2018

@author: User
"""

# import Sastrawi module
import re
import math
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# create stopword remover
factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()
# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
dic_doc = {}
corpus = []
total_files = 10 #diisi dengan jumlah file .txt yang ingin diproses

#iterator range menyesuaikan dengan jumlah file .txt
for filename in range(total_files):
    print('Processing Doc',filename+1,'...')
    str1=''
    str2=[]
    dic_tf={}
    fn = str(filename+1)
    file = open(fn+'.txt',"r")
  
    #for loop ini berfungsi sebagai pembaca seluruh isi file
    #kemudian membaginya berdasarkan delimiter dibawah
    for line in file:
        str1 += line
        
    str1 = re.split('[^a-zA-Z]',str1)
    
    #for loop ini berfungsi sebagai pemrosesan prepocessing lebih lanjut
    #untuk setiap kata
    for x in str1:
        achar = x.lower() #casefolding
        if achar != '' and achar not in stopwords:
            #pembuangan component bernilai null dan tidak tergolong sebagai stopwords
            str2.append(stemmer.stem(achar))
            
#penghitungan frekuensi munculnya setiap kata pada sebuah dokumen            
    for x in str2:
        count = 0
        if(x not in dic_tf.keys()):
            for y in str2:
                if(y == x):
                    count+=1
            dic_tf[x] = count
                    
    dic_doc['dok'+str(filename+1)] = dic_tf
    print('Finished processing Doc',filename+1)
    
   
#untuk memproses corpus. Dari setiap dokumen dimasukkan kata yang unik    
for x in dic_doc.keys():
    current_doc = dic_doc[x]
    for y in current_doc.keys():
        if (y not in corpus):
            corpus.append(y)
            
            
corpus.sort() #menyortir corpus secara lexicon
          
#menghitung  tf weight setiap dokumen tetapi isi seurut dengan corpus
wtf_weight = {}          
for x in dic_doc.keys():
    tfw = []
    current_doc = dic_doc[x]
    for y in corpus:
        for z in current_doc.keys():
            if (y not in list(current_doc.keys())):
                tfw.append(0)
                break
            elif (z == y):
                tfw.append(round(1+(math.log(current_doc[z],10)),4))  
                break
    wtf_weight[str(x)] = tfw
                
#menghitung nilai idf setiap kata dalam korpus
idf_weight = {}
for x in corpus:
    count = 0
    for y in dic_doc.keys():
        current_doc = dic_doc[y]
        for z in current_doc.keys():
            if (x not in list(current_doc.keys())):
                break
            elif(x == z): 
                count+=1
                break
    count = round(math.log((total_files/count),10),4)
    idf_weight[str(x)] = count
    
#menghitung nilai wtf.idf    
wtfidf = {}   
#LMAOOOO 
for x in wtf_weight.keys():
    count = 0
    wtf =[]
    wtf_list = wtf_weight[x]
    for y in idf_weight.values():
        wtf.append(round(wtf_list[count]*y,4))
        count+=1   
    wtfidf[str(x)] = wtf   
    
#normalisasi nilai wtf.idf
wtfidf_norm = {}
sumWSquared = 0
for x in wtfidf.keys():
    temp1 = wtfidf[x]
    temp2 = []
    for val in temp1:
        sumWSquared += val**2
    for val in range(len(temp1)):
        temp2.append (round((temp1[val]/sumWSquared),4))
    wtfidf_norm[x] = temp2
    
    
    
'''
DOKUMENTASI JANGAN DIHAPUS
# stem
sentence = 'Perekonomian Indonesia sedang dalam pertumbuhan yang menghebohkan'
output   = stemmer.stem(sentence)
print(output)
# ekonomi indonesia sedang dalam tumbuh yang bangga

#stem from a list
indo_str = ['perjalanan', 'masa', 'pertumbuhan']
indo_str_modified =[]
for indo_word in indo_str:
    indo_str_modified.append(stemmer.stem(indo_word))

print(indo_str_modified)


print(stemmer.stem('Mereka meniru-nirukannya'))
# mereka tiru
'''