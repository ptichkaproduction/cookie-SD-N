import os
import json
import time
from datetime import datetime, timedelta
import telebot # type: ignore
import random
import sqlite3

global USERS_BALANCE
COOKIE_NUMBER = 0 # цена печеньки
USERS_BALANCE = {} # баланс пользователей (user_id: [balance, last_time_cookies])
BUFFER = 0
ANSWER = 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_NAME = 'data.json'
DB_PATH = os.path.join(BASE_DIR, BASE_NAME)
print("")
print(" -----------------------")
print(" Bot version: 0.7 beta \n Made by Ptichka Production (Laboratories)\n Have a nice day ^^")
print(" -----------------------")
print("\nDebug logs:\n")

# если базы данных нет, то создаем новую

if not os.path.exists('data.json'):
    db = {'token': 'None'}
    js = json.dumps(db, indent=2)
    with open('data.json', 'w') as outfile:
        outfile.write(js)

    print('Input token in "None" (data.json)')
    exit()

# загружаем базу данных
with open(DB_PATH, 'r') as f:
    USERS_BALANCE = json.load(f)

#Загружаем токен из базы
bot = telebot.TeleBot(USERS_BALANCE['token'])
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    if not user_id in USERS_BALANCE:
        USERS_BALANCE[user_id] = [0, '']

    bot.reply_to(message, f'Привет, {user_name}, я - Серийный номер N и я люблю готовить печеньки и угощать ими других! \n' 
                                      'Чтобы съесть печенье напиши слово: <blockquote>Кукисы</blockquote> или команду: <blockquote>/cookies</blockquote>'
                                      'Для проверки количества печенек напиши это: <blockquote>/bal</blockquote>'
                                      'Для получения справки напиши это: <blockquote>/help</blockquote>'
                                      'Разработчик сие бота: @PerryTheBalloon (Перри Балун)\n'
                                      'Исходники кода предоставлены мистером @aswer_user (Дядя Эйден)', parse_mode='HTML')

@bot.message_handler(commands=['help'])
def help_message(message):
    user_name = message.from_user.first_name
    print('------\n User', user_name , 'used "help" in', datetime.now())
    bot.reply_to(message, 'Для того чтобы съесть печенье напиши слово: <blockquote>Кукисы</blockquote> Или команду: <blockquote>/cookies</blockquote> Для проверки коливества печенек напиши команду: <blockquote>/bal</blockquote> Если ты в группе используешь этого бота, то для проверки баланса лучше использовать это: <blockquote>/bal@skickman_bot</blockquote> А для получения справки используй <blockquote>/help</blockquote> или <blockquote>/help@skickman_bot</blockquote>'
                 'Разработчик сие бота: @PerryTheBalloon (Перри Балун)\n'
                 'Исходники кода предоставлены мистером @aswer_user (Дядя Эйден)', parse_mode='HTML')

# ура, печеньки!

# по команде

@bot.message_handler(commands=['cookies']) 
def cookie_message(message):
    global USERS_BALANCE
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    if not user_id in USERS_BALANCE:
        USERS_BALANCE[user_id] = [0, '']

    # проверяем, можно ли съесть печенье
    BUFFER = float(random.randint(0, 50))
    ANSWER = float(random.randint(1, 11)) # <- ANSWER = float(random.randint(1, 5))
    #BUFFER = 5
    COOKIE_NUMBER = round(BUFFER)
    try:
        last_cookie_time = datetime.strptime(USERS_BALANCE[user_id][1], '%Y-%m-%d %H:%M:%S')        
        time_delta = datetime.now() - last_cookie_time
        if time_delta.seconds < 900:
            bot.reply_to(message, f'{user_name}, ты уже ел печенье {time_delta.seconds//60} минут назад. \n'
                                              f'Новые печеньки будут готовы через {(15 - time_delta.seconds//60)} минут :3')
            return
    except:
        pass

    # обновляем баланс пользователя
    balance = USERS_BALANCE[user_id]
    print('------\n Username:', user_name , '\n User ID:', user_id , '\n Old user balance:', balance)
    #if (COOKIE_NUMBER >= 1):
    balance[0] += COOKIE_NUMBER
    balance[1] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    USERS_BALANCE[user_id] = balance
    print(' Updated user balance:', balance)
    if not user_id in USERS_BALANCE:
        USERS_BALANCE[user_id] = [0, '']
    with open(DB_PATH, 'w') as f:
        json.dump(USERS_BALANCE, f) # записываем изменения в базу данных
    if (COOKIE_NUMBER == 0):
        bot.reply_to(message, " Блин, прости...случайно передержал твои печеньки в духовке...")
    if (COOKIE_NUMBER == 50):
        if (ANSWER == 1):
            bot.reply_to(message, f"Капец...." + str(COOKIE_NUMBER) + f" печенюшек....{user_name}, тебе плохо не станет, а?")
    if (COOKIE_NUMBER >= 25):
        if (ANSWER == 1): # <- if (ANSWER == 1):
            bot.reply_to(message, f"{user_name}, неужели так вкусно? Ты же знаешь, что ты съел " + str(COOKIE_NUMBER) + " печенек или больше? .-.")
        if (ANSWER == 6): # <- if (ANSWER == 1):
            bot.reply_to(message, f"{user_name}, неужели так вкусно? Ты же знаешь, что ты съел " + str(COOKIE_NUMBER) + " печенек или больше? .-.")
        if (ANSWER == 2): # <- elif (ANSWER == 2):
            bot.reply_to(message, f"{user_name}, вкусное? А то ты ... " + str(COOKIE_NUMBER) + " печенек съел")
        if (ANSWER == 7): # <- elif (ANSWER == 2):
            bot.reply_to(message, f"{user_name}, вкусное? А то ты ... " + str(COOKIE_NUMBER) + " печенек съел")
        if (ANSWER == 3): # <- elif (ANSWER == 3):
            bot.reply_to(message, f"{user_name}, Тебе плохо не станет от " + str(COOKIE_NUMBER) + " печенек не станет, а?")
        if (ANSWER == 8): # <- elif (ANSWER == 3):
            bot.reply_to(message, f"{user_name}, Тебе плохо не станет от " + str(COOKIE_NUMBER) + " печенек не станет, а?")
        if (ANSWER == 9): # <- elif (ANSWER == 4):
            bot.reply_to(message, f"{user_name}, Тебе плохо не станет от такого количесва? Может хватит? Я конечно понимаю что они вкусные, но как бы " + str(COOKIE_NUMBER) + " печенек...")
        if (ANSWER == 4): # <- elif (ANSWER == 4):
            bot.reply_to(message, f"{user_name}, Тебе плохо не станет от такого количесва? Может хватит? Я конечно понимаю что они вкусные, но как бы " + str(COOKIE_NUMBER) + " печенек...")
        if (ANSWER == 10): # <- elif (ANSWER == 5):
            bot.reply_to(message, f"Надо же, " + str(COOKIE_NUMBER) + f" печенек... {user_name}, неужели правда настолько вкусно?")        
        if (ANSWER == 5): # <- elif (ANSWER == 5):
            bot.reply_to(message, f"Надо же, " + str(COOKIE_NUMBER) + f" печенек... {user_name}, неужели правда настолько вкусно?")
        if (ANSWER == 11): # NEW STRING
            bot.reply_to(message, f"omagad, <tg-spoiler>SECRET COOKIE!!!!!!!!!!!!</tg-spoiler>", parse_mode='HTML') # NEW STRING
    if (COOKIE_NUMBER  >=1):
        if (COOKIE_NUMBER  <=24):
            if (ANSWER == 1):
                bot.reply_to(message, f'{user_name}, ты съел ' + str(COOKIE_NUMBER) + ' овсяных печенек. \nСделал как любишь, присладил немного ^^')
            if (ANSWER == 2):
                bot.reply_to(message, f'Привет, {user_name}! Рад видеть тебя, вот твои печенюшечки, наслаждайся ^^\nТы съел ' + str(COOKIE_NUMBER) + ' печенек ')
            if (ANSWER == 3):
                bot.reply_to(message, f'{user_name}, ты съел ' + str(COOKIE_NUMBER) + ' печенек. \nНадеюсь вкусно? ^^')
            if (ANSWER == 4):
                bot.reply_to(message, f'{user_name}, вот тебе ' + str(COOKIE_NUMBER) + ' печенья с топленым молоком =3 \nНадеюсь вкусно? ^^')
            if (ANSWER == 5):
                bot.reply_to(message, f'Вкусное печенье с шоколадом в количестве ' + str(COOKIE_NUMBER) + f' печенек. \nТолько для тебя, {user_name} ^^')

def get_cookies_stats():
    user_balance = {}
    user_balance = round(USERS_BALANCE[user_id][0])
    for user_id, user_data in user_balance.items():
        for balance in user_data["balance"]:
            user_balance[user_id] = balance
    return USERS_BALANCE


@bot.message_handler(commands=['top'])
def handle_top_cookie(message):
    user_balance = get_cookies_stats()
    # Сортируем пользователей по количеству сообщений
    sorted_stats = sorted(user_balance.items(), key=lambda x: x[1], reverse=True)

    # Формируем ответ
    text = "TOP 10 COOKIE_USERS:\n"
    for i, (user_id, count) in enumerate(sorted_stats[:10]):
        text += f"{i+1}. USER {user_id}: {count} COOKIESS\n"

    bot.send_message(message.chat.id, text)

    #balance                
@bot.message_handler(commands=['bal'])
def balance_message(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    print('------\n User', user_name , 'used "bal" in', datetime.now())
    # проверяем баланс пользователя
    user_balance = round(USERS_BALANCE[user_id][0])
    last_cookie_time = datetime.strptime(USERS_BALANCE[user_id][1], '%Y-%m-%d %H:%M:%S')        
    time_delta = datetime.now() - last_cookie_time
    if time_delta.seconds < 1800:
        bot.reply_to(message, f'{user_name}, ты съел {user_balance} печенек\n'
                    f'Новые печеньки будут готовы через {(30 - time_delta.seconds//60)} минут')
    if time_delta.seconds >= 1800:
        bot.reply_to(message, f'{user_name}, ты съел {user_balance} печенек\n'
                    f'Если хочешь, то можешь как раз еще поесть, просто введи: <blockquote>/cookies</blockquote> ^^', parse_mode='HTML')
                

@bot.message_handler(func=lambda message: True)
def cookie_message(message):
    
    if message.text.upper() == 'КУКИСЫ':
            global USERS_BALANCE
            user_id = str(message.from_user.id)
            user_name = message.from_user.first_name
            if not user_id in USERS_BALANCE:
                USERS_BALANCE[user_id] = [0, '']

            # проверяем, можно ли съесть печенье
            BUFFER = float(random.randint(1, 50))
            ANSWER = float(random.randint(1, 11)) # <- ANSWER = float(random.randint(1, 5))
            #BUFFER = 5
            COOKIE_NUMBER = round(BUFFER)
            try:
                last_cookie_time = datetime.strptime(USERS_BALANCE[user_id][1], '%Y-%m-%d %H:%M:%S')        
                time_delta = datetime.now() - last_cookie_time
                if time_delta.seconds < 1800:
                    bot.reply_to(message, f'{user_name}, ты уже ел печенье {time_delta.seconds//60} минут назад. \n'
                                                    f'Новые печеньки будут готовы через {(30 - time_delta.seconds//60)} минут <3') #Ня.
                    return
            except:
                pass

            # обновляем баланс пользователя
            balance = USERS_BALANCE[user_id]
            print('------\n Username:', user_name , '\n User ID:', user_id , '\n Old user balance:', balance)
            #if (COOKIE_NUMBER >= 1):
            balance[0] += COOKIE_NUMBER
            balance[1] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            USERS_BALANCE[user_id] = balance
            print(' Updated user balance:', balance)

            with open(DB_PATH, 'w') as f:
                json.dump(USERS_BALANCE, f) # записываем изменения в базу данных
            if (COOKIE_NUMBER == 0):
                bot.reply_to(message, " Блин, прости...случайно передержал твои печеньки в духовке...")
            if (COOKIE_NUMBER == 50):
                if (ANSWER == 1):
                    bot.reply_to(message, f"Капец...." + str(COOKIE_NUMBER) + f" печенюшек....{user_name}, тебе плохо не станет, а?")
            if (COOKIE_NUMBER >= 25):
                if (ANSWER == 1): # <- if (ANSWER == 1):
                    bot.reply_to(message, f"{user_name}, неужели так вкусно? Ты же знаешь, что ты съел " + str(COOKIE_NUMBER) + " печенек или больше? .-.")
                if (ANSWER == 6): # <- if (ANSWER == 1):
                    bot.reply_to(message, f"{user_name}, неужели так вкусно? Ты же знаешь, что ты съел " + str(COOKIE_NUMBER) + " печенек или больше? .-.")
                if (ANSWER == 2): # <- elif (ANSWER == 2):
                    bot.reply_to(message, f"{user_name}, вкусное? А то ты ... " + str(COOKIE_NUMBER) + " печенек съел")
                if (ANSWER == 7): # <- elif (ANSWER == 2):
                    bot.reply_to(message, f"{user_name}, вкусное? А то ты ... " + str(COOKIE_NUMBER) + " печенек съел")
                if (ANSWER == 3): # <- elif (ANSWER == 3):
                    bot.reply_to(message, f"{user_name}, Тебе плохо не станет от " + str(COOKIE_NUMBER) + " печенек не станет, а?")
                if (ANSWER == 8): # <- elif (ANSWER == 3):
                    bot.reply_to(message, f"{user_name}, Тебе плохо не станет от " + str(COOKIE_NUMBER) + " печенек не станет, а?")
                if (ANSWER == 9): # <- elif (ANSWER == 4):
                    bot.reply_to(message, f"{user_name}, Тебе плохо не станет от такого количесва? Может хватит? Я конечно понимаю что они вкусные, но как бы " + str(COOKIE_NUMBER) + " печенек...")
                if (ANSWER == 4): # <- elif (ANSWER == 4):
                    bot.reply_to(message, f"{user_name}, Тебе плохо не станет от такого количесва? Может хватит? Я конечно понимаю что они вкусные, но как бы " + str(COOKIE_NUMBER) + " печенек...")
                if (ANSWER == 10): # <- elif (ANSWER == 5):
                    bot.reply_to(message, f"Надо же, " + str(COOKIE_NUMBER) + f" печенек... {user_name}, неужели правда настолько вкусно?")        
                if (ANSWER == 5): # <- elif (ANSWER == 5):
                    bot.reply_to(message, f"Надо же, " + str(COOKIE_NUMBER) + f" печенек... {user_name}, неужели правда настолько вкусно?")
                if (ANSWER == 11): # NEW STRING
                    bot.reply_to(message, f"omagad, <tg-spoiler>SECRET COOKIE!!!!!!!!!!!!</tg-spoiler>", parse_mode='HTML') # NEW STRING
            if (COOKIE_NUMBER  >=1):
                if (COOKIE_NUMBER  <=24):
                    if (ANSWER == 1):
                        bot.reply_to(message, f'{user_name}, ты съел ' + str(COOKIE_NUMBER) + ' овсяных печенек. \nСделал как любишь, присладил немного ^^')
                    if (ANSWER == 2):
                        bot.reply_to(message, f'Привет, {user_name}! Рад видеть тебя, вот твои печенюшечки, наслаждайся ^^\nТы съел ' + str(COOKIE_NUMBER) + ' печенек ')
                    if (ANSWER == 3):
                        bot.reply_to(message, f'{user_name}, ты съел ' + str(COOKIE_NUMBER) + ' печенек. \nНадеюсь вкусно? ^^')
                    if (ANSWER == 4):
                        bot.reply_to(message, f'{user_name}, вот тебе ' + str(COOKIE_NUMBER) + ' печенья с топленым молоком =3 \nНадеюсь вкусно? ^^')
                    if (ANSWER == 5):
                        bot.reply_to(message, f'Вкусное печенье с шоколадом в количестве ' + str(COOKIE_NUMBER) + f' печенек. \nТолько для тебя, {user_name} ^^')

def new_chat_member(update):
    for member in update.message.new_chat_members:
        if member.id == '7159499048':
            update.message.reply_text('TEXT_FIRST_MESSAGE')
bot.polling(none_stop=True)
print("\nShutting Down...")