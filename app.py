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
    # get the chat_id to be able to respond to the same user
    chat_id= update.message.message_id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    # here we call our super AI
    response = get_response(text)

    # now just send the message back
    # notice how we specify the chat and the msg we reply to
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

return 'ok'

@app.route('/ setwebhook', methods = ['GET', 'POST'])
def set_webhook():
    # usamos el objeto bot para vincular el bot a nuestra aplicación que vive 
    # en el enlace provisto por URL
    s = bot.setwebhook ('{URL} {HOOK}'. format(URL = url, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    # note the thereaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)