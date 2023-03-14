from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import time
import datetime
import wikipedia as wiki
import os
import asyncio
from colorama import Fore
import openai
import datetime
#
# (Variavéis importantes para o código)
__ = str(datetime.datetime.now())
data =f'{__[8:10]}/{__[5:7]}/{__[0:4]}'
hora =f'{__[11:16]}'
bot = AsyncTeleBot("TOKEN",colorful_logs=True)
openai.api_key = "APIKEY OPENAI"
links = "youtu.be", "youtube.com", "music.youtube", "m.youtube", "instagram.com", "soundcloud.com"
wiki.set_lang(prefix="pt")

#
#



# (0) - Comando /start => Dá instruções.
@bot.message_handler(commands=['start'])
async def start(message):
 await bot.send_message(message.chat.id,  f'Formato: \n@vid NOMEMUSICA = Baixa áudio ou vídeo do youtube.')



# (1) - Comando /ia 'DAVINCI-003' => Responde a mensagem como "ChatGPT".
@bot.message_handler(commands=['ia'])
async def openai_ia(message):
 if message.text == "/ia":
        ''
 else:
     
  #contador+=1
  id_msg2 = message.message_id
  url2 = str(message.text).replace('/ia ', '')
  print(f'[{hora}] - {Fore.YELLOW}[ACIONADO : OpenAI]{Fore.BLUE}\nNome : {Fore.RESET}({message.from_user.first_name}){Fore.BLUE}\nUser: {Fore.RESET}({message.from_user.username})')
 try: 
  response = openai.Completion.create(
        engine="text-davinci-003",
        prompt='"""\n{}\n"""'.format(str(url2)),
        temperature=0.7,
        max_tokens=1200,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        stop=['"""'])
  await bot.send_message(message.chat.id,text=f'{response["choices"][0]["text"]}\n Mantenha o bot vivo! acesse @archonyoubot',parse_mode="HTML", reply_to_message_id=id_msg2)
  print(f"{Fore.GREEN}⤷ Enviado sem erros{Fore.RESET}\n")
 except Exception as e:
     print(f"{Fore.RED}⤷ ERRO DESCONHECIDO: ( ' {Fore.RESET}{e.args}{Fore.RED} ' ){Fore.RESET}\n")

# ENGINE 'CODEX'
@bot.message_handler(commands=['codex'])
async def openai_ia(message):
 if message.text == "/codex":
        ''
 else:
     
  #contador+=1
  id_msg2 = message.message_id
  url2 = str(message.text).replace('/codex ', '')
  print(f'[{hora}] - {Fore.YELLOW}[ACIONADO : OpenAI -  CODEX]{Fore.BLUE}\nNome : {Fore.RESET}({message.from_user.first_name}){Fore.BLUE}\nUser: {Fore.RESET}({message.from_user.username})')
 try: 
  response = openai.Completion.create(
        engine="code-davinci-002",
        prompt='"""\n{}\n"""'.format(str(url2)),
        temperature=0.7,
        max_tokens=1200,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        stop=['"""'])
  await bot.send_message(message.chat.id,text=f'{response["choices"][0]["text"]}\n Mantenha o bot vivo! acesse @archonyoubot',parse_mode="HTML", reply_to_message_id=id_msg2)
  print(f"{Fore.GREEN}⤷ Enviado sem erros{Fore.RESET}\n")
 except Exception as e:
     print(f"{Fore.RED}⤷ ERRO DESCONHECIDO: ( ' {Fore.RESET}{e.args}{Fore.RED} ' ){Fore.RESET}\n")
     
     
     

# (2) - Comando /wiki => Caso exista resultado, retorna o mesmo, do contrário printa e avisa no Telegram que não foi encontrado. 
@bot.message_handler(commands=['wiki'])
async def wiki_wiki(message):
 id_msg = message.message_id
 user_id = message.from_user.id
 url2 = str(message.text).replace('/wiki ', '')
 print(f'[{hora}] - {Fore.YELLOW}[ACIONADO : Wikipedia]{Fore.BLUE}\nNome : {Fore.RESET}({message.from_user.first_name}){Fore.BLUE}\nUser: {Fore.RESET}({message.from_user.username})')
 try:
  result_wiki = str(wiki.summary(url2))
  if 'does not match any pages.' not in result_wiki:
   try:
    await bot.send_message(chat_id=user_id, text=result_wiki[:4096])
    print(f"{Fore.GREEN}⤷ Enviado sem erros :{Fore.RESET} {url2}\n")
   except Exception as e:
    if 'Error code: 403. Description: Forbidden: bot was blocked by the user' or "Error code: 403. Description: Forbidden: bot can't initiate conversation with a user" in str(e.args):
     await bot.send_message(message.chat.id, text='Dê um "/start" no meu pv e refaça a consulta.', reply_to_message_id=id_msg, parse_mode="HTML")
     print(f"{Fore.RED}⤷ ERRO:{Fore.RESET} Usuário não interagiu com o bot anteriormente.\n")
    else:
       print(f'{Fore.RED}⤷ ERRO DESCONHECIDO: {Fore.RESET}{e.args}\n')
 except Exception as e:
     if f"('{url2}',)" or f'("{url2}",)' in str(e.args):
      await bot.send_message(message.chat.id, text='Não encontrei resultados na Wikipedia.', reply_to_message_id=id_msg)
      print(f"{Fore.RED}⤷ ERRO:{Fore.RESET} Não foi encontrado resultado para ({Fore.BLACK}{url2[:10]}{Fore.RESET}[...]).\n")
     else: 
      await bot.send_message(message.chat.id, text='Não encontrei resultados na Wikipedia.', reply_to_message_id=id_msg)
      print(f"{Fore.RED}⤷ ERRO DESCONHECIDO: ( ' {Fore.RESET}{e.args}{Fore.RED} ' ){Fore.RESET}\n")



# (3) - @vid => com opção de escolher vídeo ou audio em InlineKeyboard
@bot.message_handler(func=lambda message: True if links else False)
async def vid_msg_handler(message):
 if "'via_bot': {'id': 90832338" in str(message):
  for link in links:
   if link in str(message.text):
    global messagechatid
    global messagesent
    global messageid
    global messageufirstname
    global messageusername
    global messagetext
    messagetext = message.text
    messagechatid = message.chat.id
    messageid = message.message_id
    messageufirstname = message.from_user.first_name
    messageusername = message.from_user.username
    messagesent = await bot.send_message(message.chat.id, "Escolha o tipo a ser enviado :", reply_to_message_id=message.message_id,reply_markup=await vid_gen_markup())
    
async def vid_gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Vídeo", callback_data="video_"),
                               InlineKeyboardButton("Áudio", callback_data="audio_"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
async def vid_callback_query(call):
    
    contador=0      
    if call.data == "video_":
       try:
          await bot.answer_callback_query(call.id, "Baixando Vídeo... @uncomputerized")
          await bot.delete_message(chat_id=messagechatid, message_id=messagesent.id)
          id_msg2 = messageid
          url2 = str(messagetext)
          print(f'[{hora}] - {Fore.YELLOW}[ACIONADO : Vídeo]{Fore.BLUE}\nNome : {Fore.RESET}({messageufirstname}){Fore.BLUE}\nUser: {Fore.RESET}({messageusername})')
     
     
          video_info = yt_dlp.YoutubeDL(params={
          'noplaylist':True,
          'cachedir':False,
          'max_filesize': 50331648,
          'keepvideo':False,
          'format':'best',
          'quiet': True
           }).extract_info(
           url = url2, download=False
           )
          global video_title
          video_title = video_info.get('title', None)
           
          with yt_dlp.YoutubeDL() as ydl:
           video_title = video_info.get('title', None)
           filenamev =video_title
          filenamev ="".join([c for c in filenamev if c.isalpha() or c.isdigit() or c==' ' or c==' ']).rstrip().replace(' ', '_')
          filenamev =f'{filenamev}.mp4'
          options={
           'format':'best',
           'noplaylist':True,    
           'keepvideo':False,
           'cachedir':False,
           'max_filesize': 50331648,
           'outtmpl':filenamev,
           'quiet': True
             }
          
          with yt_dlp.YoutubeDL(options) as ydl:
             ydl.download([video_info['webpage_url']])

          try:
            await bot.send_video(messagechatid, reply_to_message_id=id_msg2, video=open((filenamev), 'rb'), supports_streaming=True)
            print(f"{Fore.GREEN}⤷ Enviado sem erros :{Fore.RESET} {video_title}\n")
            time.sleep(5)
            os.remove(filenamev)
          except Exception as e:
            await bot.send_message(messagechatid, "O vídeo não pode ser enviado, pois excede 50MB", reply_to_message_id=id_msg2)
            if 'O sistema não pode ' or 'No such file or directory' in e.args:
                  print(f"{Fore.RED}⤷ ERRO: Arquivo maior que 48 megabytes.{Fore.RESET}\n")
                  pass
            else:
                  print(f"{Fore.RED}⤷ ERRO:{Fore.RESET}{e.args}.\n")
            time.sleep(5)
            os.remove(filenamev)
       except Exception as e:
             if ' is not defined' in str(e.args):
                  await bot.answer_callback_query(call.id, "ERRO: Comandos antigos não serão processados novamente, tente enviar denovo")
             elif 'O sistema não pode ' or 'No such file or directory' in e.args:
                  's'
             else:
              print(f"{Fore.RED}⤷ ERRO:{Fore.RESET}{e.args}.\n")   
              
              
    elif call.data == "audio_":
      try:
               await bot.answer_callback_query(call.id, "Baixando Áudio... @uncomputerized")
               await bot.delete_message(chat_id=messagechatid, message_id=messagesent.id)
               print(f'[{hora}] - {Fore.YELLOW}[ACIONADO : Áudio]{Fore.BLUE}\nNome : {Fore.RESET}({messageufirstname}){Fore.BLUE}\nUser: {Fore.RESET}({messageusername})')
               id_msg2 = messageid
               url2 = str(messagetext)
     
     
               video_info = yt_dlp.YoutubeDL(params={
                'noplaylist':True,
                'cachedir':False,
                'max_filesize': 50331648,
                'keepvideo':False,
                'format':'bestaudio',
                'quiet': True
                 }).extract_info(
                 url = url2, download=False
                 )
               video_title = video_info.get('title', None)
           
               with yt_dlp.YoutubeDL() as ydl:
                 video_title = video_info.get('title', None)
                 filenamev = video_title
               filenamev = "".join([c for c in filenamev if c.isalpha() or c.isdigit() or c==' ' or c==' ']).rstrip().replace(' ', '_')
               filenamev=f'{filenamev}.mp3'
               options={
               'format':'bestaudio',
               'noplaylist':True,
               'max_filesize': 50331648,    
               'keepvideo':False,
               'cachedir':False,
               'outtmpl':filenamev,
               'quiet': True
                }
  
         
          
               with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])


                await bot.send_audio(messagechatid, reply_to_message_id=id_msg2, audio=open((filenamev), 'rb'))
                print(f"{Fore.GREEN}⤷ Enviado sem erros :{Fore.RESET} {video_title}\n")
                time.sleep(5)
                os.remove(filenamev)
              
      except Exception as e:
             if ' is not defined' in str(e.args):
              await bot.answer_callback_query(call.id, "ERRO: Comandos antigos não serão processados novamente, tente enviar denovo")
             elif 'O sistema não pode ' or 'No such file or directory' in e.args:
              print(f"{Fore.RED}⤷ ERRO: Arquivo maior que 48 megabytes.{Fore.RESET}\n")
              await bot.send_message(messagechatid, "O áudio não pode ser enviado, pois excede 50MB", reply_to_message_id=id_msg2)
              time.sleep(5)
              os.remove(filenamev)
             else:
              print(f"{Fore.RED}⤷ ERRO:{Fore.RESET}{e.args}.\n")



# (4) - ________



##########################
asyncio.run(bot.polling())
