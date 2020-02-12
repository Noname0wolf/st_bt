# -*- coding: utf-8 -*-
import cnf
import telebot
import urllib.request
import os
import re
import pickle

def save_dict(dict,name):
    with open('C:\\Users\\And\\Music\\st_bt\\data\\'+name + '.pkl', "wb") as file:
        pickle.dump(dict,file)
        file.close()
    print('OK!')

def load_dict(name):
    with open('C:\\Users\\And\\Music\\st_bt\\data\\'+name+'.pkl', "rb") as file:
        data = pickle.load(file)
        print(data)
        file.close()
    return data


def search_values_in_dict(dict, values):
    temp = 0
    values = values.lower()
    for i in dict.values():
        if values == i[0].lower():
            # print(i)
            temp += 1
    if temp:
        return True
    else:
        return False

folder='ФБ-63'
list_of_types=('application/vnd.openxmlformats-officedocument.wordprocessingml.document','text/plain','application/pdf','application/msword')
list_of_practise=('пр1','пр2','пр3','пр4','пр5','пр6',)
dict_of_users=load_dict('dict_of_users')

bot = telebot.TeleBot(cnf.token)

@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    document_id = message.document.file_id
    file_info   = bot.get_file(document_id)
    first_name  = message.from_user.first_name
    id          = message.from_user.id
    file_name   = message.document.file_name




    if message.document.mime_type in list_of_types:
        result = re.split(' ', file_name)
        if len(result) == 2 and result[1].split('.')[0] in list_of_practise:
            if dict_of_users.keys() == None or (first_name, id) not in dict_of_users.keys() :
                dict_of_users[(first_name, id)] = [re.split(' ', file_name)[0],0]
                print("Novaya zapisy",(first_name, id))

            if re.split(' ', file_name)[0].lower()==dict_of_users[(first_name, id)][0].lower() and search_values_in_dict(dict_of_users,re.split(' ', file_name)[0]):
                dict_of_users[(first_name, id)][1]+=1

                if result[1].split('.')[0] not in os.listdir():
                    os.mkdir(str(result[1].split('.')[0]))
                    print(str(result[1].split('.')[0])+'  papka sozdana')
                    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{cnf.token}/{file_info.file_path}',
                                               str(result[1].split('.')[0])+'\\'+file_name)
                    bot.send_message(message.chat.id, 'Файл принят👌😋\nОн записан по пути: '+str(result[1].split('.')[0])+'\\'+file_name)
                    print((first_name, id),"file is save\n")
                else:
                    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{cnf.token}/{file_info.file_path}',
                                               str(result[1].split('.')[0])+'\\'+file_name)
                    bot.send_message(message.chat.id, 'Файл принят👌😋\nОн записан по пути: '+str(result[1].split('.')[0])+'\\'+file_name)
                    print((first_name, id),"file is save\n")







            else:
                bot.send_message(message.chat.id,
                                 'Имя файла не соответствует закрепленному за вами имени или вы не тот за кого себя выдаете😐\nПереименуйте пожалуйста😊\n\nПример имени файла:\n"Пронченко пр1"\n"Пронченко пр6"')
                print((first_name, id),'Имя файла не соответствует вашему имени')
        else:
            bot.send_message(message.chat.id,
                'Имя файла не подходит под формат обработки😐\nПереименуйте пожалуйста😊\n\nПример имени файла:\n"Пронченко пр1"\n"Пронченко пр6"')
            print((first_name, id),'Имя файла не подходит под формат')

    else:
        bot.send_message(message.chat.id,
                         message.from_user.first_name + ', Вы отправили файл  расширением которое не поддерживаеться😐\nПопробуй еще раз с другим расширением😊')
        print((first_name, id),'Вы отправили файл  расширением которое не поддерживаеться')

# Тут работаем с командой start
@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.send_message(message.chat.id, 'Привет, '+message.from_user.first_name+'\nБот создан, чтобы облегчить жизнь.\nСюда нужно скидывать файли с практиками АМКБ(Юдин).\nПоддерживаемые расширения файлов: pdf, doc, docx, txt.\nЕсли нужно добавить какое-либо расширения, напишите ему: @fury_wolf\nСоблюдайте формат имени файла, иначе бот не пустит😉\nЕсли вы отправите файл с одинаковым именем, то он перезапишет себя же.\n\nПример имени файла:\n"Пронченко пр1"\n"Пронченко пр6"\n\nБот, возможно, будет отвечать не сразу, так как код работает не всегда.\nПриятного пользования))')

# Тут работаем с командой help
@bot.message_handler(commands=['help'])
def welcome_help(message):
    bot.send_message(message.chat.id, 'Ни чем не могу тебе помочь...😝😝😝')

















if __name__ == '__main__':
    try:
        if folder not in os.listdir():
            print('папки '+folder+ ' нет')
            os.mkdir(folder)
            print(folder + 'папка создана')
            os.chdir('./' + folder)
        else:
            os.chdir('./' + folder)
        print(os.listdir(),'\n\n')
        bot.infinity_polling()
    finally:
        save_dict(dict_of_users, 'dict_of_users')