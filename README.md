# wiz_telegram_bot

This little python program allows you to control your wiz light trough a telegram bot, using text or voice commands.
Is just a sample to put together differnts libraries and to do some POC.

It runs with Python3 and in my case I'm runing it on a RaspberryPi 4

The libraries used are:  
https://pypi.org/project/pywizlight/ -->Handle wiz lights  
https://telepot.readthedocs.io/en/latest/ -->To use telegram bot  
https://pypi.org/project/SpeechRecognition/ --> Speach recognitiom  
https://pypi.org/project/wavio/ --> convert the audio to WAV for speach recognition  
https://pypi.org/project/pydub/ --> convert the audio to WAV for speach recognition  


You can send the commands (/on, on, /off, off) to turn on/off the indicated light  
If you send a text it will do it directly trough pywizlight, if you send an audio it will first retrieve it from Telegram server, then save it locally and convert it to WAV, and last it will be send to google speach recognition API to transalate it to text.
