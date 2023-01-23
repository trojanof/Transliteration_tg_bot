import os
import logging
from string import punctuation
from aiogram import Bot, Dispatcher, executor, types


logging.basicConfig(filename='transliterate_bot.log', encoding='utf-8', level=logging.INFO)
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)

trans_dict = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l',
 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
 'щ': 'shch', 'ы': 'y', 'ъ': 'ie', 'э': 'e', 'ю': 'iu', 'я': 'ia'}

dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f"Привет, {user_name}! \nМожешь написать фамилию, имя или отчество"\
        " (или всё вместе) и я напишу тебе транслитерацию в соответствии с приказом МИД России № 2113 от 12.02.2020"
    logging.info(f"{user_name=} {user_id=} sent message: {message.text}")
    await message.reply(text)

@dp.message_handler()
async def send_translit(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    raw_text = message.text.lower().replace('ь', '')
    
    flag = 0
    for symbol in raw_text:
        if symbol in punctuation:
            raw_text = raw_text.replace(symbol,'')
    for symbol in raw_text:
        if symbol not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя ':
            return_message = 'Видимо тут не только русские буквы. Не могу транслитерировать. Повторите ввод.' 
            flag = 1
            break   
    if len(raw_text) == 0:
        return_message = 'Нечего транслитерировать. Повторите ввод.' 
        flag = 1    
    if flag == 0:   
        entered_text = raw_text.split()
        trans_list = [[] for j in range(len(entered_text))]
        for i, word in enumerate(entered_text):
            for char in word:
                trans_list[i].append(trans_dict[char])
            
        trans_list = [''.join(w).capitalize() for w in trans_list]
        return_message = ' '.join(trans_list)
    logging.info(f"{user_name=} {user_id=} sent message: {message.text}, got response: {return_message}")
    await bot.send_message(user_id, return_message)
    

if __name__ == '__main__':
    executor.start_polling(dp)