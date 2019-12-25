def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import warnings 
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from lxml import html
from json import dump,loads
from requests import get
import json
import csv
from re import sub
from dateutil import parser as dateparser
from time import sleep
from django.http import HttpResponse
from django.shortcuts import render
import os
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("darkgrid", {"axes.facecolor": ".3"})
from youtube_transcript_api import YouTubeTranscriptApi

def home(request):
    return render(request,'home.html')

def result(request):
    nm=request.GET['url']
    csvfilename=nm+".csv"

    imgname=nm+'.png'
    img="/"+imgname
    location="static/"+imgname
    loc="/static/"+imgname
    location1="static/"+"em"+imgname
    loc1="/static/"+"em"+imgname
    location2="static/"+"ha"+imgname
    loc2="/static/"+"ha"+imgname
    location3="static/"+"of"+imgname
    loc3="/static/"+"of"+imgname
    location4="static/"+"wc"+imgname
    loc4="/static/"+"wc"+imgname
    print (loc)
    l=f'\"{loc}"'
    print (l)
    print (location)

    #if os.path.exists("static\\cloud_amazon3.png"):
    #    os.remove("static\\cloud_amazon3.png")
    #else:
    #    print("The file does not exist")
    #nm="amazonextraction/" + nm
    
    import re
    data=YouTubeTranscriptApi.get_transcript(nm,languages=['en'])
    csvfilename=nm+".csv"
    for i in range(len(data)):
        with open (csvfilename,'a',encoding="utf-8") as res:        
            writer=csv.writer(res)           
            s="{},{},{},{}\n".format(data[i]['duration'],data[i]['start'],data[i]['start']+data[i]['duration'], re.sub(r'\s+', ' ',re.sub(r'\W', ' ',data[i]['text'],flags=re.I)))
            res.write(s)
            print (s)

    df=pd.read_csv(csvfilename)
    df.columns=['duration','start','end','text']
    X=df['text']
        
    from sklearn.externals import joblib

    emotion=[]
    loaded_model = joblib.load('emotion_model.sav')
    for i in X:
        emotion.append(loaded_model.predict([i])[0])
    df['emotion']=emotion
    
    dict={0:"hate_speech",1:"offensive_speech",2:"neither"}
    nature=[]
    loaded_model = joblib.load('offense_hate_modelv1.sav')
    for i in X:
        nature.append(dict[loaded_model.predict([i])[0]])
    df['nature']=nature

    b=df.groupby('nature')['text'].count()

    x=[]
    y=[]
    for i in range(len(b)):
        x.append(b.index[i])
        y.append(b[i])       

    import seaborn as sns
    import matplotlib.pyplot as plt

    label=x
    freq=y




    fig, ax = plt.subplots(figsize=(15,7))
    plt.bar(label,freq,width=0.4 ,edgecolor = 'black', linewidth=3,color=['red','yellow','orange'])


    ax.set_xlabel('Labels',fontsize=20)
    ax.set_ylabel('Frequency of occurence',fontsize=20)
    ax.set_title("Labels and their frequency",fontsize=20)
    plt.xticks(label,rotation=30)
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = 15)  
    fig.savefig(location, bbox_inches='tight')

    c=df.groupby('emotion')['text'].count()

    x1=[]
    y1=[]
    for i in range(len(c)):
        x1.append(c.index[i])
        y1.append(c[i])   

    import seaborn as sns
    import matplotlib.pyplot as plt

    label=x1
    freq=y1

    fig, ax = plt.subplots(figsize=(15,7))
    plt.bar(label,freq,width=0.4 ,edgecolor = 'black', linewidth=3,color=['red','yellow','orange'])

    ax.set_xlabel('Labels',fontsize=20)
    ax.set_ylabel('Frequency of occurence',fontsize=20)
    ax.set_title("Labels and their frequency",fontsize=20)
    plt.xticks(label,rotation=30)
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = 15)       
    fig.savefig(location1, bbox_inches='tight')

    off=df[df['nature']=="offensive_speech"]
    off.to_csv("tempoff.csv")
    dfoff=pd.read_csv("tempoff.csv")
    X=dfoff['text']

    import re  

    processed_tweets=[]

    for tweet in range(1, len(X)):  
        processed_tweet = re.sub(r'\W', ' ', str(X[tweet]))

                
        # Remove all the special characters
        
        processed_tweet = re.sub(r'http\S+', ' ', processed_tweet)
        
        #processed_tweet = re.sub(r'https?:\/\/+', ' ', processed_tweet)
        
        #processed_tweet=re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ',processed_tweet)
        
        processed_tweet=re.sub(r'www\S+', ' ', processed_tweet)
        
        processed_tweet=re.sub(r'co \S+', ' ', processed_tweet)
        # remove all single characters
        processed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_tweet)
    
        # Remove single characters from the start
        processed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_tweet) 
    
        # Substituting multiple spaces with single space
        processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
    
        # Removing prefixed 'b'
        processed_tweet = re.sub(r'^b\s+', ' ', processed_tweet)
        
        processed_tweet = re.sub(r'\d','',processed_tweet)
        
        processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)

    
        # Converting to Lowercase
        processed_tweet = processed_tweet.lower()
        
        processed_tweets.append(processed_tweet)
        
    print (processed_tweets)    

    with open('u_off_corpus.txt', 'w',encoding='utf-8') as f:
        for item in processed_tweets:
            f.write("%s\n" % item)

    sample = open("u_off_corpus.txt", "r",encoding='utf-8') 
    s = sample.read() 

    # Replaces escape character with space 
    f = s.replace("\n", " ") 

    from os import path
    from PIL import Image
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    import matplotlib.pyplot as plt
    #% matplotlib inline
    stopwords= set(STOPWORDS)
    stopwords.update([" ",'','re'])
    listtowrite=[]
    for i in f.split(((' '))):
        if i not in stopwords:
            listtowrite.append(i)
    print (listtowrite)

    with open('u_off_ref_corpus.txt', 'w',encoding='utf-8') as f:
        for item in listtowrite:
            f.write("%s\n" % item)

    sample = open("u_off_ref_corpus.txt", "r",encoding='utf-8') 
    s = sample.read() 

    # Replaces escape character with space 
    f = s.replace("\n", " ") 
    import collections
    words = re.findall(r'\w+', open("u_off_ref_corpus.txt").read().lower())
    s=collections.Counter(words).most_common(50)

    x2=[]
    y2=[]
    for i in range(len(s)):
        x2.append(s[i][0])
        y2.append(s[i][1])
    print (x2)
    print (y2)

    
    fig, ax = plt.subplots(figsize=(15,7))
    plt.bar(x2, y2, edgecolor = 'black', linewidth=2,color="red")
    #barlist[0].set_color('r')
    ax.set_xlabel('Words',fontsize=20)
    ax.set_ylabel('Frequency of words',fontsize=20)
    ax.set_title("Most used words in 'offensive' reviews",fontsize=20)
    plt.xticks(rotation=90)
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = 15)    
    fig.savefig(location2, bbox_inches='tight')

    sample = open("u_off_ref_corpus.txt", "r",encoding='utf-8') 
    s = sample.read() 

    # Replaces escape character with space 
    f = s.replace("\n", " ") 
    from os import path
    from PIL import Image
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    import matplotlib.pyplot as plt
    #% matplotlib inline
    stopwords= set(STOPWORDS)

    #stopwords.update(["status","still","must","support","",'pretty','mmine','loud','amazon','stays','anything','mine','month','proper','listen','written','box' ,"public","last","read","johnson","didn","ve","put","needs","save","help","deal","tories","years","articles","need","back","government","pm","back","life","care","everyone","give","day","country","new","look","mps","everything","really","need","hard","believe","even","still","re","eu","pic","dlidington", "philiphammonduk","jeremy_hunt","may","theresa_may","alanduncanmp","watson","work",'don', "anna_soubry","voted","heidi","constituents","heidiallen","claiming","yasmin","george_osborne","ayeshahazarika","tom","conservatives","griffith","hear","tory", "twitter","amberrudduk","love","take","real","friend","good","conservative","election","right","tell","vote","sure","parliament",'people',"justinegreening","tom_watson","labour","time","party","think","going","set","lines","nickymorgan","amberruddhr","will","one","brexit","say","mp","said","want","come","well","no","see","now","know","borisjohnson","stephentwigg","please","happy","share","remember","thank","much","constituent","spaces","job","action","got","jbl",'sound','product','speaker','rha','gya','high','hai',"today",'ho','go','ll','amazes','working','thing','laptop','gaya','raha','purchase','bluetooth','speakers','amazing','compactness','connect'])

    wordcloud = WordCloud(
                            background_color='black',
                            stopwords=stopwords,
                            max_words=200,
                            max_font_size=150, width=1000, height=450,
                            random_state=42
                            ).generate(f)
    print(wordcloud)
    plt.figure(figsize = (10, 10), facecolor = None) 
    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.tight_layout(pad=0)
    ax.set_title("WordCloud of offensive content",fontsize=20)
    plt.axis('off')
    plt.show()
    fig.savefig(location3, bbox_inches='tight')

    #plt.savefig('cloud_amazon.png', facecolor='k', bbox_inches='tight')

    ohate=df[df['nature']=="hate_speech"]
    ohate.to_csv("temphate.csv")
    dfhate=pd.read_csv("temphate.csv")
    X=dfhate['text']
    len((dfhate))

    import re  

    processed_tweets=[]

    for tweet in range(1, len(X)):  
        processed_tweet = re.sub(r'\W', ' ', str(X[tweet]))

                
        # Remove all the special characters
        
        processed_tweet = re.sub(r'http\S+', ' ', processed_tweet)
        
        #processed_tweet = re.sub(r'https?:\/\/+', ' ', processed_tweet)
        
        #processed_tweet=re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ',processed_tweet)
        
        processed_tweet=re.sub(r'www\S+', ' ', processed_tweet)
        
        processed_tweet=re.sub(r'co \S+', ' ', processed_tweet)
        # remove all single characters
        processed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_tweet)
    
        # Remove single characters from the start
        processed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_tweet) 
    
        # Substituting multiple spaces with single space
        processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
    
        # Removing prefixed 'b'
        processed_tweet = re.sub(r'^b\s+', ' ', processed_tweet)
        
        processed_tweet = re.sub(r'\d','',processed_tweet)
        
        processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)

    
        # Converting to Lowercase
        processed_tweet = processed_tweet.lower()
        
        processed_tweets.append(processed_tweet)
        
    print (processed_tweets)    

    with open('u_hate_corpus.txt', 'w',encoding='utf-8') as f:
        for item in processed_tweets:
            f.write("%s\n" % item)

    sample = open("u_hate_corpus.txt", "r",encoding='utf-8') 
    s = sample.read() 

    # Replaces escape character with space 
    f = s.replace("\n", " ") 

    from os import path
    from PIL import Image
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    import matplotlib.pyplot as plt
    #% matplotlib inline
    stopwords= set(STOPWORDS)
    stopwords.update([" ",'','re'])
    listtowrite=[]
    for i in f.split(((' '))):
        if i not in stopwords:
            listtowrite.append(i)
    print (listtowrite)
  

    with open('u_hate_ref_corpus.txt', 'w',encoding='utf-8') as f:
        for item in listtowrite:
            f.write("%s\n" % item)

    sample = open("u_hate_ref_corpus.txt", "r",encoding='utf-8') 
    s = sample.read() 

    # Replaces escape character with space 
    f = s.replace("\n", " ") 

    import collections
    words = re.findall(r'\w+', open("u_hate_ref_corpus.txt").read().lower())
    s=collections.Counter(words).most_common(50)

    x4=[]
    y4=[]
    for i in range(len(s)):
        x4.append(s[i][0])
        y4.append(s[i][1])
    print (x4)
    print (y4)

    
    fig, ax = plt.subplots(figsize=(15,7))
    plt.bar(x4, y4, edgecolor = 'black', linewidth=2,color="blue")
    #barlist[0].set_color('r')
    ax.set_xlabel('Words',fontsize=20)
    ax.set_ylabel('Frequency of words',fontsize=20)
    ax.set_title("Labels an their frequency",fontsize=20)
    plt.xticks(rotation=90)
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = 15)    

       
    fig.savefig(location4, bbox_inches='tight')
    




    #return render(request,'result.html',{'result':'Real-time analysis successfull','url':nm,'filename':loc,'f2':imgname})
    return render(request,'result.html',{'result':'Real-time analysis successfull','f2':loc,'f3':loc1,'f4':loc2,'f5':loc3,'f6':loc4})

def about(request):
    return render(request,'about.html')    