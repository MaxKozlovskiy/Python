import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	stick = open('stickers/Hello.tgs' , 'rb')
	bot.send_sticker(message.chat.id, stick)

	#keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("🎁 Рандомное число")
	item2 = types.KeyboardButton("ツ Как дела ?")

	markup.add(item1, item2)

	bot.send_message(message.chat.id, 'Приветствую ,{0.first_name} \n Я - <b>{1.first_name}</b> ,бот созданный для вас'.format(message.from_user, bot.get_me()) ,
		parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == '🎁 Рандомное число':
			bot.send_message(message.chat.id, str(random.randint(0,100)))
		elif message.text == 'ツ Как дела ?':

			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton('Хорошо',callback_data='good')
			item2 = types.InlineKeyboardButton('Плохо',callback_data='bad')

			markup.add(item1, item2)

			bot.send_message(message.chat.id, 'Всё очень даже неплохо, ведь мной пользуешься ты! :)', reply_markup=markup)

		else:
			bot.send_message(message.chat.id, 'Я не знаю что ответить! :(')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                reply_markup=None)
 
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
 
    except Exception as e:
        print(repr(e))

#RUN
bot.polling(none_stop=True)