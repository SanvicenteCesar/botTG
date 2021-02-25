from flask import flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, url
from telebot.mastermind import get_response


global bot
global TOKEN 
TOKEN = bot_token
bot = telegram.bot (token = TOKEN)

#iniciar flask app

app = Flask(__name__)

@app.route('/{}' .format(TOKEN), methods=['POST'])
def respond():
    #recuperar el mensaje en JSON y luego transformarlo en el objeto de Telegram
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # obtener el chat_id para poder responder al mismo usuario
    chat_id= update.message.message_id
    # obtener la identificación del mensaje para poder responder a este mensaje específico
    msg_id = update.message.message_id

    # Telegram entiende UTF-8, así que codifique texto para compatibilidad Unicode
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    # aquí llamamos a nuestra súper IA
    response = get_response(text)

   # ahora solo envía el mensaje de vuelta
    # observe cómo especificamos el chat y el mensaje al que respondemos
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    return 'ok'

@app.route('/ setwebhook', methods = ['GET', 'POST'])
def set_webhook():
    # usamos el objeto bot para vincular el bot a nuestra aplicación que vive 
    # en el enlace provisto por URL
    s = bot.setwebhook ('{URL} {HOOK}'. format(URL = url, HOOK=TOKEN))
    # algo que nos haga saber que las cosas funcionan
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    # tenga en cuenta el argumento thereaded que permite
    # que tu aplicación tenga más de un hilo
    app.run(threaded=True)