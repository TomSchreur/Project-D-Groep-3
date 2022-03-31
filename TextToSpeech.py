from hashlib import new
from gtts import gTTS
import os
from database_manual import selectfromtable
speak = "€ 55"
language = 'en'

output= gTTS(text=speak, lang= language, slow=False)

productdetails = selectfromtable()
mp3details = []
substring= []

namestring=[]


string =""

f=0
for i in productdetails:
    namestring.append(productdetails[f][1])
    f=f+1

new_set = [x.replace('.png','').replace(')','').replace('(','') for x in namestring]

def createMp3():
    f=0
    for i in productdetails:
        string =""
        string = new_set[f] + " The price is € " + str(productdetails[f][2])
        newstring = "./static/mp3files/"+productdetails[f][1].replace('.png','.mp3')
      
        output= gTTS(text=string, lang= language, slow=False)
        output.save(newstring)
        f=f+1


#createMp3()