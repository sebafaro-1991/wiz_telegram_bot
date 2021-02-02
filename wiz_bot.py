import telepot
from telepot.loop import MessageLoop
from pywizlight import wizlight, PilotBuilder, discovery
import asyncio
import speech_recognition as sr
from requests import get
from json import loads
from os import path, mkdir, chmod
import os
import wavio
import sys
from pydub import AudioSegment

bot_token = <token_bot>
light_ip = <wiz light ip>
#main function where we receive the msg from the end user
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    usermsg = bot.getUpdates(allowed_updates='message')
    command='test'
    
    if content_type == 'voice':
        #voice=msg['voice']
        command=get_file(usermsg,chat_id)
        print (command)
    else:
        command = msg['text'] 
        print ('Got command: %s' % command)
        
    
    #Generate loop for the async function
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    
    if command != None:
        loop.run_until_complete(lightState(command, chat_id))


bot = telepot.Bot(bot_token)

MessageLoop(bot, handle).run_as_thread()
print ('I am listening ...')

#Function to tranlsate the audio to text using google speech
def speech(audio):
    
    r = sr.Recognizer()
    file=sr.AudioFile(audio)    
    with file as source:
        audio = r.record(source)    
    type(audio)
    
    try:
        recog = r.recognize_google(audio, language = 'en-US')
        #print("You said: " + recog)
        return recog
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

#To get the URL path of the telegram audio that we sent
def get_file_path(token, file_id):
    get_path = get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(token, file_id))
    json_doc = loads(get_path.text)
    try:
        file_path = json_doc['result']['file_path']
    except Exception as e:  # Happens when the file size is bigger than the API condition
        print('Cannot download a file because the size is more than 20MB')
        return None

    return 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)

#To download the file from Telegram
def get_file(msg_list, chat_id):
    
    #print ('Got voice: %s' % voice)
    audios_dir='audios_dir'
    
    for msg in msg_list:
        try:
            voiceFileId = msg['message']['voice']['file_id']
        except KeyError:
            continue

       
        # Get file download path
        download_url = get_file_path(bot_token, voiceFileId)
        voiceFile = get(download_url)
        if download_url is None:
            continue

        if not path.exists(audios_dir):
            mkdir(audios_dir)
        
        try:
            with open('{}/{}'.format(audios_dir, voiceFileId), 'wb') as f:
        
                f.write(voiceFile.content)
                f.close()
                os.chmod(f.name , 0o777)
                dest_audio=f.name
                #convert to WAV
                audio = AudioSegment.from_ogg(f.name)
                audio.export(dest_audio, format="wav")
    
                recog=speech(dest_audio)
                
                return recog
        except FileNotFoundError:  
            bot.sendMessage(chat_id, 'Error')
            
#Excute commands on the wiz lights            
async def lightState (command,chat_id):
    light = wizlight(light_ip)
    
    if command == '/on' or command == 'on': 
        await light.turn_on(PilotBuilder())
        bot.sendMessage(chat_id, "Light on")

    elif command == '/off' or command == 'off':
        await light.turn_off()
        bot.sendMessage(chat_id, "Light off")