# -*- coding: utf-8 -*-
"""
Created on Tue May 15 03:29:45 2018

@author: User
"""
from Document_PreProcessing import *
import re
import math

#menghitung CosSim
str1 = input("Welcome to Gulu! Please Enter Your Query : ")   
str1 = re.split('[^a-zA-Z]',str1)
str2 = []
query = {}
    
    #for loop ini berfungsi sebagai pemrosesan prepocessing lebih lanjut
    #untuk setiap kata
for x in str1:
        achar = x.lower() #casefolding
        if achar != '' and achar not in stopwords and achar in corpus:
            #pembuangan component bernilai null dan tidak tergolong sebagai stopwords
            str2.append(stemmer.stem(achar))
            
#penghitungan frekuensi munculnya setiap kata pada sebuah dokumen            
for x in str2:
    count = 0
    if(x not in query.keys()):
        for y in str2:
            if(y == x):
                count+=1
        query[x] = count
        
#pemrosesan wtf query        
input_wtf_weight = {}
weight = 0       
for x in corpus:
    for y in query.keys():
        if (x not in list(query.keys())):
            weight = 0
            break
        elif (x == y):
            weight = round(1+(math.log(query[y],10)),4)
            break
    input_wtf_weight[str(x)] = weight   


#pemrosesan wtf.idf query    
input_wtfidf = {}           
for x in input_wtf_weight.keys():
    wtf = 0
    for y in idf_weight.keys():
        if(x == y):
            wtf = round(input_wtf_weight[x]*idf_weight[y],4)
    input_wtfidf[str(x)] = wtf        
      
#normalisasi nilai wtf.idf query
input_wtfidf_norm = {}
sumWSquared = 0
    
temp1 = input_wtfidf.values()
for val in temp1:
    sumWSquared += val**2       
for y in input_wtfidf.keys():
    temp2 = round((input_wtfidf[y]/sumWSquared),4)
    input_wtfidf_norm[y] = temp2 
    
    
#menghitung CosSim
results ={}
input_norm_wtfidf_list = list(input_wtfidf_norm.values())

for x in wtfidf_norm.keys():
    current_doc = wtfidf_norm[x]
    total = 0
    for y in range(len(current_doc)):
        total += round(current_doc[y]*input_norm_wtfidf_list[y],4)
    results[str(x)] = total    


#menyortir urutan dokumen dan menampilkan top 5
top_results = []    
for x in results.keys():
    info=[]
    info.append(x)
    info.append(results[x])
    top_results.append(info)
top_results = sorted(top_results,key=lambda x: x[1], reverse=True)




#nilai dalam range sesuaikan dengan jumlah top file
print('=================================================')
print('Here are your search results based on similarity:')
for x in range(5):
    print(str(top_results[x][0])+' with a CosSim of '+str(round(top_results[x][1],4)))
    