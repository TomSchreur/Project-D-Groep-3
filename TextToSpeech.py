from hashlib import new
from gtts import gTTS
import os
from database_manual import selectallFromTable

def createTempProductMp3(prodDescription,name):
    language = 'en'
    mp3File = gTTS(text=prodDescription, lang=language, slow=False)
    mp3File.save("./static/mp3files/" + name + '.mp3')