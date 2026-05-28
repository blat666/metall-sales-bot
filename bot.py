import telebot
import sqlite3

TOKEN = '8731126220:AAHbJ0fKddQIs5_HTBEf0zzgzh1zm9rwEGs'
bot = telebot.TeleBot(TOKEN)

FILE_URL = 'https://your-link.com/metall-library.zip'

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, paid INTEGER DEFAULT 0)')
conn.commit()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_buy = telebot.types.KeyboardButton('КУПИТЬ БИБЛИОТЕКУ')
    btn_check = telebot.types.KeyboardButton('ПРОВЕРИТЬ ОПЛАТУ')
    keyboard.add(btn_buy, btn_check)
    
    cursor.execute('INSERT OR IGNORE INTO users (user_id, paid) VALUES (?, 0)', (user_id,))
    conn.commit()
    
    bot.send_message(user_id, 
        'БИБЛИОТЕКА МЕНЕДЖЕРА ПО ПРОДАЖАМ МЕТАЛЛОПРОКАТА\n\n'
        'Внутри:\n'
        '- 13 книг\n'
        '- 60+ скриптов\n'
        '- 35+ возражений\n'
        '- Технический справочник\n\n'
        'Цена: 2900 руб\n\n'
        'Нажми кнопку',
        reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'КУПИТЬ БИБЛИОТЕКУ')
def buy(message):
    bot.send_message(message.chat.id,
        'ОПЛАТА:\n\n'
        'ЮMoney: СЮДА_ССЫЛКУ\n'
        'Карта: СЮДА_НОМЕР\n\n'
        'После оплаты отправь /paid КОД')

@bot.message_handler(func=lambda message: message.text == 'ПРОВЕРИТЬ ОПЛАТУ')
def check_payment(message):
    user_id = message.chat.id
    cursor.execute('SELECT paid FROM users WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    
    if result and result[0] == 1:
        bot.send_message(user_id, f'Доступ есть\nСкачай: {FILE_URL}')
    else:
        bot.send_message(user_id, 'Оплаты нет')

@bot.message_handler(commands=['paid'])
def paid(message):
    user_id = message.chat.id
    cursor.execute('UPDATE users SET paid=1 WHERE user_id=?', (user_id,))
    conn.commit()
    bot.send_message(user_id, f'Оплата подтверждена\nСкачай: {FILE_URL}')

@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, 'Нажми /start')

if __name__ == '__main__':
    print('Bot started')
    bot.polling()
