import telebot
import sqlite3
import os

# ТОКЕН ТВОЕГО БОТА (НЕ ПОКАЗЫВАЙ НИКОМУ!)
TOKEN = '8731126220:AAHbJ0fKddQIs5_HTBEf0zzgzh1zm9rwEGs'
bot = telebot.TeleBot(TOKEN)

# ССЫЛКА НА ZIP-АРХИВ (поменяешь позже)
FILE_URL = 'https://your-link.com/metall-library.zip'

# База данных
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, paid INTEGER DEFAULT 0)')
conn.commit()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_buy = telebot.types.KeyboardButton('💰 КУПИТЬ БИБЛИОТЕКУ')
    btn_check = telebot.types.KeyboardButton('✅ ПРОВЕРИТЬ ОПЛАТУ')
    keyboard.add(btn_buy, btn_check)
    
    cursor.execute('INSERT OR IGNORE INTO users (user_id, paid) VALUES (?, 0)', (user_id,))
    conn.commit()
    
    bot.send_message(user_id, 
        '📚 <b>БИБЛИОТЕКА МЕНЕДЖЕРА ПО ПРОДАЖАМ МЕТАЛЛОПРОКАТА</b>\n\n'
        '🔥 ЧТО ВНУТРИ:\n'
        '✓ 13 полноценных книг\n'
        '✓ 60+ скриптов продаж\n'
        '✓ 35+ возражений\n'
        '✓ Технический справочник по металлам\n'
        '✓ Актуально на 2026 год\n\n'
        '💰 ЦЕНА: 2 900 ₽\n\n'
        '👇 Нажми кнопку "КУПИТЬ БИБЛИОТЕКУ"',
        parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == '💰 КУПИТЬ БИБЛИОТЕКУ')
def buy(message):
    user_id = message.chat.id
    bot.send_message(user_id,
        '💳 <b>КАК КУПИТЬ:</b>\n\n'
        '1. Переведите 2 900 ₽ по реквизитам (пришлю в личку)\n'
        '2. После оплаты напишите /paid КОД_ИЗ_ЧЕКА\n\n'
        'КОНТАКТЫ ДЛЯ ОПЛАТЫ:\n'
        'ЮMoney: СЮДА_ССЫЛКУ\n'
        'Карта: СЮДА_НОМЕР_КАРТЫ',
        parse_mode='HTML')

@bot.message_handler(commands=['paid'])
def paid(message):
    user_id = message.chat.id
    # ПРОВЕРКА ОПЛАТЫ (упрощённо)
    cursor.execute('UPDATE users SET paid=1 WHERE user_id=?', (user_id,))
    conn.commit()
    
    bot.send_message(user_id,
        f'✅ <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n\n'
        f'📥 Скачай библиотеку по ссылке:\n{FILE_URL}\n\n'
        f'Ссылка активна 24 часа. Если не скачалось — пиши @твой_ник',
        parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == '✅ ПРОВЕРИТЬ ОПЛАТУ')
def check_payment(message):
    user_id = message.chat.id
    cursor.execute('SELECT paid FROM users WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    
    if result and result[0] == 1:
        bot.send_message(user_id, f'✅ Доступ открыт!\n{FILE_URL}')
    else:
        bot.send_message(user_id, '❌ Оплата не найдена. Оплатите и напишите /paid')

print('Бот запущен!')
bot.polling()
