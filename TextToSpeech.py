from hashlib import new
from gtts import gTTS
import os
import glob
from database_manual import selectallProducts
speak = "€ 55"
language = 'en'

output= gTTS(text=speak, lang= language, slow=False)

productdetails = selectallProducts()
mp3details = []
substring= []

namestring=[]


string =""

f=0
for i in productdetails:
    namestring.append(productdetails[f].name)
    f=f+1

new_set = [x.replace('.png','').replace(')','').replace('(','') for x in namestring]

def createMp3():
    f=0
    for i in productdetails:
        string =""
        string = new_set[f] + " The price is € " + str(productdetails[f].getPrice())
        newstring = "./static/mp3files/"+productdetails[f].name + ".mp3"
      
        output= gTTS(text=string, lang= language, slow=False)
        output.save(newstring)
        f=f+1



def createTempProductMp3(name,price,category):
    productInf = ""
    productInf = "The product name is: " + name + ". The price is € " + str(price) + ". The category is: " + category
    mp3File = gTTS(text=productInf, lang=language, slow=False)
    mp3File.save("./static/mp3files/"+ name +'.mp3')

def cleanMp3Directory():
    path =  glob.glob('./static/mp3files/*')
    for f in path:
        os.remove(f)