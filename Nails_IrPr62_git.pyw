import telebot
import ast
from datetime import date as d
import requests
from urllib.parse import urljoin

##########################################################

# подключение к API телеграмма

token = ''
bot  = telebot.TeleBot (token)




# подключение к API pythoneAnywhere

username = ""
api_token = ""
pythonanywhere_host = "www.pythonanywhere.com"

api_base = "https://{pythonanywhere_host}/api/v0/user/{username}/".format(
    pythonanywhere_host=pythonanywhere_host,
    username=username,
)

########################################################

god_users = [0,1] 

########################################################

# ВРЕМЯ ЗАПИСИ

time = ['10.00','12.00','14.00','16.00','18.00']

########################################################
def dt_now():
    x = d.today()
    return x

def year(month_input):
    month_now = str(dt_now())
    month_now = int(month_now[5:7])
    year_now = str(dt_now())
    year_now = int(year_now[0:4])
    month_input = int(month_input)
    if month_input < month_now :
        year = year_now + 1
    else:
        year = year_now
    return year

def year_today():
    x = str(dt_now())
    x = x[0:4]
    return x

def f_open_read():
    try:
        resp = requests.get(
        urljoin(api_base, "files/path/home/{username}/nails_IrPr62_2022/zapis.txt".format(username=username)),
        headers={"Authorization": "Token {api_token}".format(api_token=api_token)}
    )
        tasks_str = resp.content
        tasks_str = tasks_str.decode('UTF-8')
    #print (tasks_str)
        tasks = ast.literal_eval(tasks_str)
        return tasks

    except:
        bot.send_message(god_users[0], 'ошибка открытия файла для чтения')


def f_open_write(tasks):
    tasks = str(tasks)

    resp = requests.post(
    urljoin(api_base, "files/path/home/{username}/nails_IrPr62_2022/zapis.txt".format(username=username)),
    files={"content": tasks},
    headers={"Authorization": "Token {api_token}".format(api_token=api_token)}
)
    #print(resp.status_code)

def zapis_time_limit (date_input):
    #dt_now = date.today()
    try:
        date_curent = date_input
        day_in_date_curent = date_curent[0:2]
        day_in_date_curent = int(day_in_date_curent)
        month_in_date_current = date_curent[3:5]
        month_in_date_current = int(month_in_date_current)
        year_now = year (month_in_date_current)
        date_1 = d (year_now, month_in_date_current, day_in_date_curent)
        dt__now = dt_now()
        x = date_1 - dt__now
        x = str(x)
        x = x.split()
        x = x[0]
        x = int(x)
    except:
        x = 'ne ok'
        return (x)
    else:
        if x <= 14 and x > 0:
            x ='ok'
            return (x)

def date_zapis_clear ():
    tasks = f_open_read()

    date_now = str(dt_now())
    key_for_delete =[]
    for task in tasks:
        if int(task[0][0:4]) <= int(date_now[0:4]):
            if int(task[0][5:7]) < int(date_now[5:7]):
                key_for_delete.append(task)
    for key in key_for_delete:
        del tasks[key]

    f_open_write (tasks)


@bot.message_handler(commands = ['help'])
def help(message):
    HELP = """
/help  - помощь

/start - просмотреть свою запись, записаться

/dell xx.xx xx.xx - удалить запись, где хх.хх - дата и время

/change xx.xx xx.xx Имя - изменить запись

/weekend xx.xx - записать выходной

/show хх.хх - показать запись на дату

/show_all - показать все записи
    """
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands = ['start'])
def start (message):
    global user_id
    user_id = message.from_user.id
    global user_nick_name
    user_nick_name = message.chat.username

    if user_nick_name == None:
        user_nick_name = message.chat.first_name
    if user_nick_name == None:
        user_nick_name = message.chat.last_name
    if user_nick_name == None:
        user_nick_name == 'Таинственная Незнакомка'

    try:
        tasks = f_open_read()

        if user_id in god_users:
            bot.send_message(message.chat.id, f"Привет, {user_nick_name}!\nдобавляем/корректируем /change\nудаляем /dell\n/help  - помощь")
        else:
            all_users_id = []
            for key in tasks:
                x = tasks[key][1]
                if x != '':
                    x = int (x)
                    if x == user_id:
                        all_users_id.append(user_id)
                        break

            if user_id in all_users_id:
                day_from_key = key[0][8:10]
                month_from_key = key[0][5:7]
                time_from_key = key[1]
                bot.send_message(message.chat.id, f"Привет, {user_nick_name}! твоя запись: {day_from_key}.{month_from_key} в {time_from_key}")
                bot.send_message(message.chat.id, f'отменить запись - отправь')
                bot.send_message(message.chat.id, f'/dell {day_from_key}.{month_from_key} {time_from_key}')
            else:
                bot.send_message(message.chat.id, f"Привет, {user_nick_name}! Давай запишемся")
                bot.send_message(message.chat.id, 'введи дату в формате хх.хх')
                bot.register_next_step_handler(message, add_date)
    except:
        bot.send_message(message.chat.id, 'чет не так пошло. давай ещё раз /start')

def add_date(message):
    try:
        global date_input
        date_input = message.text
        x = zapis_time_limit (date_input)
        if x != 'ok':
            bot.send_message (message.chat.id, 'записаться можно только на 2 недели вперед. пришли новую дату')
            bot.register_next_step_handler(message, add_date)
        else:
            tasks = f_open_read()
            if date_input[2] == '.' and (len(date_input[0:2]) == 2) and (len(date_input[3:5]) == 2):
                time_free = ''
                for i in time:
                    year_now = str(dt_now())
                    year_now = year_now[0:4]
                    date_input_full = year_now + '-' + date_input[3:5] + '-' + date_input[0:2]
                    date_time = (date_input_full, i)
                    if date_time not in tasks:
                        tasks[date_time] = ['free','','','']
                    x = tasks[date_time]
                    if x[0] == 'free':
                        time_free = time_free + i + ' '
                if time_free == '':
                    bot.send_message (message.chat.id, 'на эту дату всё занято ( выбери другую дату')
                    bot.register_next_step_handler(message, add_date)
                else:
                    bot.send_message(message.chat.id, f'Выбери время\nДоступное время:\n{time_free}\nесли нужна другая дата - отправь 0')
                    bot.register_next_step_handler(message, add_time)
            else:
                bot.send_message(message.chat.id, 'неверная дата, давай еще раз, в формате хх.хх')
                bot.register_next_step_handler(message, add_date)
    except:
        bot.send_message(message.chat.id, 'чет не так пошло. давай ещё раз. введи дату')
        bot.register_next_step_handler(message, add_date)

def add_time(message):
    time_current = message.text
    try:
        if time_current == '0':
            bot.send_message(message.chat.id, f'пришли новую дату')
            bot.register_next_step_handler(message, add_date)
        else:
            global key
            key = (date_input, time_current)
            tasks = f_open_read()
    except:
        bot.send_message(message.chat.id, 'чет не так пошло. давай ещё раз')
        bot.register_next_step_handler(message, add_time)
    else:
        if time_current in time:
            year_now = year_today()
            date_input_full = year_now + '-' + date_input[3:5] + '-' + date_input[0:2]
            key = (date_input_full, time_current)
            if key not in tasks:
                tasks[key] = ['free','','','']
            x = tasks[key]
            if x[0] == 'busy':
                bot.send_message(message.chat.id, 'увы, время занято. введите другое')
                bot.register_next_step_handler(message, add_time)
            else:
                bot.send_message(message.chat.id, f'{key[0][8:10]}.{key[0][5:7]} {key[1]}, записываемся?')
                bot.register_next_step_handler(message, choise)

def choise(message):
    choise = message.text
    choise = choise.lower()
    try:
        if choise == 'да' or choise == '+':
            tasks = f_open_read()

            tasks[key] = ['busy', user_id, user_nick_name, ''] 

            f_open_write(tasks)
            bot.send_message(message.chat.id, 'запись сделана. для проверки отправь /start')

            chat_id_Pr = int(god_users[1])
            bot.send_message(chat_id_Pr, f'новая запись {key[0]}  {key[1]}  {user_nick_name}')
        else:
            bot.send_message(message.chat.id, 'ок.запишемся в другой раз. для записи нажми /start')
    except:
        bot.send_message(message.chat.id, 'чет не так пошло. давай ещё раз /start')

@bot.message_handler(commands = ['change'])
def change(message):
    user_id = message.from_user.id
    text = message.text
    if user_id in god_users:
        try:
            text_soup = text.split()
            month_input = text_soup[1][3:5]
            year_now = year(month_input)
            date_time_curent = ((str(year_now) + '-' + text_soup[1][3:5] + '-' + text_soup[1][0:2]), text_soup[2])  # из сообщения берем [1]: дату (дд.мм) и [2]: время (чч.мм)
            x_1 = len (text_soup[1])
            x_2 = len (text_soup[2])
            user_name = text_soup [3]
            if x_1 != 5:
                bot.send_message(message.chat.id, f"неправильнный ввод даты. надо / change xx.xx xx.xx Имя")
            elif x_2 != 5:
                bot.send_message(message.chat.id, f"неправильнный ввод времени. надо / change xx.xx xx.xx Имя")
            else:
                tasks = f_open_read()
                tasks[date_time_curent] = ['busy', user_id, user_name, '']
                f_open_write(tasks)
        except:
            bot.send_message(message.chat.id, f"что-то пошло не так, попробуй еще раз /change xx.xx xx.xx Имя")
        else:
            bot.send_message(message.chat.id, f"запись изменена")

@bot.message_handler(commands = ['dell'])
def dell (message):
    user_id = message.from_user.id
    text = message.text
    try:
        if text == "/dell":
            bot.send_message(message.chat.id, f"неправильнный ввод. введи /dell хх.хх хх.хх")
            bot.send_message(message.chat.id, f"где первые хх.хх - дата, вторые хх.хх - время")
        text_soup = text.split()
        key_curent = text_soup[1:]
        day_from_key_curent = key_curent[0][0:2]
        month_from_key_curent = key_curent[0][3:5]
        year_now = year(int(month_from_key_curent))
        time_from_key_curent = key_curent [1]
        key_curent = ((str(year_now) + '-' + month_from_key_curent + '-' + day_from_key_curent), time_from_key_curent)
        tasks = f_open_read()
        x = tasks[key_curent][1]
    except:
        bot.send_message(message.chat.id, f"неправильнный ввод. введи /dell хх.хх хх.хх")
        bot.send_message(message.chat.id, f"где первые хх.хх - дата, вторые хх.хх - время")
    else:
        if  (x == user_id) or (user_id in god_users):
            tasks[key_curent]=['free','','','']
            f_open_write(tasks)
            bot.send_message(message.chat.id, f"ок, запись удалена")
            bot.send_message(message.chat.id, f"для новой записи нажми /start")

@bot.message_handler(commands = ['show'])
def show(message):
    user_id = message.from_user.id
    if user_id in god_users:
        command = message.text
        try:
            command = message.text.split(maxsplit=1)
            date = command[1]
            year_curent = year(date[3:5])
            date = str(year_curent) + '-' + date[3:5] + '-' + date[0:2]
            text = ''
            tasks = f_open_read()
            for t in time:
                date_time_curent = (date, t)
                if date_time_curent in tasks:
                    x = tasks[date_time_curent][0]
                    if x == 'busy':
                        if user_id != god_users[0]:
                            y = tasks[date_time_curent][2]
                            text = text + t + ' ' + y + '\n'
            if text == '':
                text = "записи нет"
            text_all = date[8:10] + '.' + date[5:7] + '\n' + text
        except:
            if message.text == '/show':
                bot.send_message(message.chat.id, "неправильный ввод. введи /show хх.хх")
                bot.send_message(message.chat.id, "где хх.хх - дата")
            else:
                bot.send_message(message.chat.id, "что-то пошло не так")
        else:
            bot.send_message(message.chat.id, text_all)

@bot.message_handler(commands = ['show_all'])
def show(message):
    user_id = message.from_user.id
    if user_id in god_users:
        try:
            date_zapis_clear()
            tasks = f_open_read ()
            text = ''
            text_final = ''
            for task in tasks:
                x = tasks[task][0] # free or busy
                y = tasks[task][2] # ник пользователя
                z = task[0] # дата визита
                z = z[8:10] + '.' + z[5:7] # пересобираю дату в формат дд.мм
                t = task[1] # время визита
                if x == 'busy':
                    if user_id != god_users[0]:
                        text = text + z + '  ' + t + '  ' + y + '\n'
            text_final = text_final  + ' ' + text
            if text_final == ' ':
                text_final = 'нет записей'
        except:
            bot.send_message(message.chat.id, 'что-то пошло не так. попробуй еще раз')
        else:
            bot.send_message(message.chat.id, text_final)

@bot.message_handler(commands = ['weekend']) #занять весь день
def weekend (message):
    user_id = message.from_user.id
    text = message.text
    try:
        if user_id in god_users:
            text_soup = text.split()
            key_curent = text_soup[1:]
            day_from_key_curent = key_curent[0][0:2]
            month_from_key_curent = key_curent[0][3:5]
            year_now = year(int(month_from_key_curent))
            tasks = f_open_read()

            for t in time:
                key_curent = ((str(year_now) + '-' + month_from_key_curent + '-' + day_from_key_curent), t)
                if key_curent not in tasks:
                    tasks[key_curent] = ['free', '', '', '']
                if tasks[key_curent][0] == 'busy':
                    bot.send_message(message.chat.id, f"на эту дату есть запись! незанятое время помечено, как выходной")
                else:
                    tasks[key_curent] = ['busy', user_id, 'Выходной', '']
            f_open_write (tasks)
            bot.send_message(message.chat.id, f"{day_from_key_curent}.{month_from_key_curent} - выходной")
    except:
        bot.send_message(message.chat.id, f"неправильнный ввод. введи /weekend xx.xx")
        bot.send_message(message.chat.id, f"где хх.хх - дата")

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            
            