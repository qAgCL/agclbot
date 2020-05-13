import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
import json
import re
import datetime
from bs4 import BeautifulSoup as BS
def get_wheather(city):
    appid = 'ab2ede76dd714722a2183f3c570b2618'
    week = requests.get('http://api.openweathermap.org/data/2.5/weather',
                        params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    weather = json.loads(week.text)
    print(week.text)
    wher = ''
    try:
        wher = 'Страна: ' + weather["sys"]["country"] + '\nГород: ' + weather["name"] + '\nПогода: ' + \
               weather["weather"][0]["description"] + '\n🌡️ Температура: ' + str(
            weather["main"]["temp"]) + ' °C, ощущается как ' + str(
            weather["main"]["feels_like"]) + " °C" + "\n 💧 Влажность: " + str(
            weather['main']['humidity']) + "%\n 💨 Скорость ветра: " + str(
            weather['wind']['speed']) + '\n ☀ Рассвет: ' + datetime.datetime.fromtimestamp(
            weather["sys"]["sunrise"]).strftime('%H:%M:%S') + '\n 🌑 Закат: ' + datetime.datetime.fromtimestamp(
            weather["sys"]["sunset"]).strftime('%H:%M:%S')
    except:
        wher = 'Нет такого города'
    return wher
def group_schedule_exam(group_num):
    url = 'https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=' + group_num
    string = ''
    try:
        r = requests.get(url)
        all_shedule = json.loads(r.text)
        for exam in all_shedule['examSchedules']:
            days=exam['weekDay'].split('.')
            times=exam['schedule'][0]['startLessonTime'].split(':')
            start=datetime.datetime(int(days[2]), int(days[1]),int(days[0]), int(times[0]), int(times[0]))
            now=datetime.datetime.now()
            delay=start-now
            lessday=datetime.timedelta(seconds=delay.seconds)
            string+=exam['weekDay']+' c '+exam['schedule'][0]['startLessonTime']+' по '+exam['schedule'][0]['endLessonTime']+'\n'+exam['schedule'][0]['lessonType']+' по '+exam['schedule'][0]['subject']+' в аудитории '+exam['schedule'][0]['auditory'][0]+'\n Преподаватель: '+exam['schedule'][0]['employee'][0]['fio']+\
                    '\n'+'Осталось: '+str(delay.days)+' дн. '+str(datetime.timedelta(seconds=delay.seconds))+'\n\n'
        if string=='':
            string='Расписание еще не добавлено'
    except Exception as e:
        print(e)
        string = 'Такой группы не существует'
    finally:
        return string
def group_schedule(group_num):
    url = 'https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=' + group_num
    string = ''
    try:
        r = requests.get(url)
        url = 'http://journal.bsuir.by/api/v1/week'
        week = requests.get(url)
        print(week.text)
        tasd = json.loads(r.text)
        for day in tasd['schedules']:
            string += day['weekDay'] + ':\n\r'
            for key in day['schedule']:
                for weekN in key['weekNumber']:
                    if weekN == int(week.text):
                        if len(key['auditory']) == 0:
                            key['auditory'].append('')
                        group = {
                            0: 'Вся группа',
                            1: 'Первая подгруппа',
                            2: 'Вторая подгруппа'
                        }
                        string += key['subject'] + ' ' + group[key['numSubgroup']] + ' ' + key['lessonType'] + ' ' + \
                                  key[
                                      'lessonTime'] + ' ' + key['auditory'][0] + '\n\r'
            string += '\n\r'
    except:
        string = 'Такой группы не существует'
    finally:
        return string
def schedule_day(x, group_num):
    url = 'https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=' + group_num
    try:
        r = requests.get(url)
        url = 'http://journal.bsuir.by/api/v1/week'
        week = requests.get(url)
        tasd = json.loads(r.text)
        week_days = {
            0: 'Понедельник',
            1: 'Вторник',
            2: 'Среда',
            3: 'Четверг',
            4: 'Пятница',
            5: 'Суббота',
            6: 'Воскресенье'
        }
        week_day = week_days[(datetime.datetime.now().weekday() + x) % 7]
        string = ''
        if (week_day != 'Воскресенье'):
            for day in tasd['schedules']:
                if (day['weekDay'] == week_day):
                    string += day['weekDay'] + ':\n\r'
                    for key in day['schedule']:
                        for weekN in key['weekNumber']:
                            if weekN == int(week.text):
                                if len(key['auditory']) == 0:
                                    key['auditory'].append('')
                                group = {
                                    0: 'Вся группа',
                                    1: 'Первая подгруппа',
                                    2: 'Вторая подгруппа'
                                }
                                string += key['subject'] + ' ' + group[key['numSubgroup']] + ' ' + key['lessonType'] + ' ' + \
                                          key[
                                              'lessonTime'] + ' ' + key['auditory'][0] + '\n\r'
            return string
        else:
            string='Выходной 😎'
    except:
        string = 'Такой группы не существует'
    finally:
        return string
def schedule(group_num):
    url = 'https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=' + group_num
    try:
        r = requests.get(url)
        url = 'http://journal.bsuir.by/api/v1/week'
        week = requests.get(url)
        print(week.text)
        tasd = json.loads(r.text)
        string = ''
        for day in tasd['schedules']:
            string += day['weekDay'] + ':\n\r'
            for key in day['schedule']:
                for weekN in key['weekNumber']:
                    if weekN == int(week.text):
                        if len(key['auditory']) == 0:
                            key['auditory'].append('')
                        group = {
                            0: 'Вся группа',
                            1: 'Первая подгруппа',
                            2: 'Вторая подгруппа'
                        }
                        string += key['subject'] + ' ' + group[key['numSubgroup']] + ' ' + key['lessonType'] + ' ' + key[
                            'lessonTime'] + ' ' + key['auditory'][0] + '\n\r'
            string += '\n\r'
        return string
    except:
        string = 'Такой группы не существует'
    finally:
        return string
def schedule_curday(day_name, group_num):
    url = 'https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=' + group_num
    try:
        r = requests.get(url)
        url = 'http://journal.bsuir.by/api/v1/week'
        week = requests.get(url)
        tasd = json.loads(r.text)
        string = ''
        day_name = day_name[0:-1]
        if (day_name != 'воскресень'):
            for day in tasd['schedules']:
                if (day['weekDay'][0:-1].lower() == day_name):
                    string += day['weekDay'] + ':\n\r'
                    for key in day['schedule']:
                        for weekN in key['weekNumber']:
                            if weekN == int(week.text):
                                if len(key['auditory']) == 0:
                                    key['auditory'].append('')
                                group = {
                                    0: 'Вся группа',
                                    1: 'Первая подгруппа',
                                    2: 'Вторая подгруппа'
                                }
                                string += key['subject'] + ' ' + group[key['numSubgroup']] + ' ' + key['lessonType'] + ' ' + \
                                          key[
                                              'lessonTime'] + ' ' + key['auditory'][0] + '\n\r'
                    break
            if (string == ''):
                string='Нет такого дня недели'
        else:
            string='Выходной 😎'
    except:
        string = 'Такой группы не существует'
    finally:
        return string
def send_schedule(den):
    mess = "Ошибочка"
    if den[0][0] == '':
        group_num = "851002"
    else:
        group_num = den[0][0]
    if (den[0][1] == 'завтра'):
        mess = schedule_day(1, group_num)
    elif (den[0][1] == 'сегодня'):
        mess = schedule_day(0, group_num)
    elif (den[0][1] == 'неделю'):
        mess = schedule(group_num)
    else:
        mess = schedule_curday(den[0][1], group_num)
    return mess
def main():
    bot_session = vk_api.VkApi(
        token="7e7f19b864480ef7eaaba0ad822b5f661cebbc4ce9bd43c64aa65610392d54f0eef71f1f628bde8a4ef31")
    bot_api = bot_session.get_api()
    longpoll = VkBotLongPoll(bot_session, 192798565)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение')
            print(event.message.from_id)
            print(event.message.peer_id)
            print(event.message.text)
            print(event.message.attachments)
            message_text = re.sub(r"\[club192798565\|[@\w\s]+\]",'',event.obj.message['text']).strip()
            print(message_text)
            rofl=str(message_text[-2:])
            if rofl.lower()=='да':
                bot_api.messages.send(
                    random_id=random.random(),
                    peer_id=event.obj.message['peer_id'],
                    message='Пизда'
                )
            ras_day = re.findall(r"экзамены ([0-9]*)", message_text.lower())
            if len(ras_day):
                bot_api.messages.send(random_id=random.random(), peer_id=event.message.peer_id, message=group_schedule_exam(ras_day[0]))
            ras_day = re.findall(r"расписание ([0-9]*)[\s]*на ([а-я]+)", message_text.lower())
            if len(ras_day):
                bot_api.messages.send(random_id=random.random(), peer_id=event.message.peer_id, message=send_schedule(ras_day))
            if message_text.lower() == 'вставай':
                bot_api.messages.send(
                    random_id=random.random(),
                    peer_id=event.obj.message['peer_id'],
                    sticker_id='8916'
                )
            ras_day = re.findall(r"погода ([\w\- ]+)", message_text.lower())
            if len(ras_day):
                    bot_api.messages.send(
                        random_id=random.random(),
                        peer_id=event.obj.message['peer_id'],
                        message=get_wheather(ras_day[0])
                    )
            if message_text.lower() == 'коронавирус':
                url = 'https://www.worldometers.info/coronavirus'
                r = requests.get(url)
                html = BS(r.text, 'html.parser')
                znach = html.findAll("div", id="maincounter-wrap")
                cases = re.search(r"[0-9]+(,[0-9]+)+", str(znach[0]))
                deaths = re.search(r"[0-9]+(,[0-9]+)+", str(znach[1]))
                recovered = re.search(r"[0-9]+(,[0-9]+)+", str(znach[2]))
                bot_api.messages.send(
                    random_id=random.random(),
                    peer_id=event.obj.message['peer_id'],
                    message='Cases: ' + cases[0] + '\n\rDeaths: ' + deaths[0] + '\n\rRecovered ' + recovered[0],
                )
            country = re.findall(r"[кК]оронавирус в ([A-z]+)", message_text)
            if len(country):
                print(country)
                url = 'https://www.worldometers.info/coronavirus'
                r = requests.get(url)
                html = BS(r.text, 'html.parser')
                total_cases = "None"
                total_deaths = "None"
                total_recovered = "None"
                new_cases = "None"
                new_deaths = "None"
                recovered = "None"
                znach = html.findAll("tr")
                flag = False
                for i in znach:
                    match = re.search(r">(" + country[0] + ")<", str(i))
                    if match:
                        znach2 = re.findall(r"(>(\+*[\s]*([0-9]+(,[0-9]+)*))[\s]*<)|(></td>)", str(i))
                        flag = True
                        if znach2[1][1] != "":
                            total_cases = znach2[1][1]
                        if znach2[2][1] != "":
                            new_cases = znach2[2][1]
                        if znach2[3][1] != "":
                            total_deaths = znach2[3][1]
                        if znach2[4][1] != "":
                            new_deaths = znach2[4][1]
                        if znach2[5][1] != "":
                            recovered = znach2[5][1]
                        bot_api.messages.send(
                            random_id=random.random(),
                            peer_id=event.obj.message['peer_id'],
                            message='Country:' + country[
                                0] + '\n\r🤒Total cases: ' + total_cases + '\n\rNew cases: ' + new_cases + '\n\r☠Total deaths: ' + total_deaths + '\n\rNew deaths: ' + new_deaths + '\n\r😁Recovered: ' + recovered,
                        )
                        break
                if not flag:
                    bot_api.messages.send(
                        random_id=random.random(),
                        peer_id=event.obj.message['peer_id'],
                        message='Нет такой страны',
                    )
            horoscope = re.findall(r"[Г|г]ороскоп ([А-я]+) на ([А-я]+)", message_text)
            if len(horoscope):
                day=horoscope[0][1].lower()
                sign=horoscope[0][0].lower()
                if sign=='пидарас':
                    bot_api.messages.send(
                        random_id=random.random(),
                        peer_id=event.obj.message['peer_id'],
                        message='Сам ты пидарас'
                    )
                link = {
                    'рыбы': 'https://1001goroskop.ru/?znak=pisces',
                    'овен': 'https://1001goroskop.ru/?znak=aries',
                    'телец': 'https://1001goroskop.ru/?znak=taurus',
                    'близнецы': 'https://1001goroskop.ru/?znak=gemini',
                    'рак': 'https://1001goroskop.ru/?znak=cancer',
                    'лев': 'https://1001goroskop.ru/?znak=leo',
                    'дева': 'https://1001goroskop.ru/?znak=virgo',
                    'весы': 'https://1001goroskop.ru/?znak=libra',
                    'скорпион': 'https://1001goroskop.ru/?znak=scorpio',
                    'стрелец': 'https://1001goroskop.ru/?znak=sagittarius',
                    'козерог': 'https://1001goroskop.ru/?znak=capricorn',
                    'водолей': 'https://1001goroskop.ru/?znak=aquarius',
                }
                try:
                    url=link[sign]
                    if (day=='неделю'):
                        url += '&kn=week'
                        r = requests.get(url)
                        html = BS(r.text, 'html.parser')
                        znach = html.findAll("i")
                        prognoz = str(znach[0])
                        prognoz = prognoz.replace('<i>', '')
                        prognoz = prognoz.replace('</i>', '')
                        prognoz += '\n'
                        znach1 = html.findAll(attrs={'class':re.compile("date")})
                        znach2 = html.findAll("p")
                        print(znach1)
                        print(znach2)
                        for i in range(7):
                            print(znach1[i+1])
                            prognoz += str(znach1[i+1])
                            prognoz = prognoz.replace('<div class="date">', '')
                            prognoz = prognoz.replace('</div>', '')
                            prognoz += '\n'
                            prognoz += str(znach2[i])
                            prognoz = prognoz.replace('<p>', '')
                            prognoz = prognoz.replace('</p>', '')
                            prognoz += '\n'
                        bot_api.messages.send(
                            random_id=random.random(),
                            peer_id=event.obj.message['peer_id'],
                            message=prognoz
                        )
                    else:
                        if (day=='завтра'):
                            url+='&kn=tomorrow'
                        r = requests.get(url)
                        html = BS(r.text, 'html.parser')
                        znach = html.findAll("i")
                        prognoz = str(znach[0])
                        prognoz = prognoz.replace('<i>', '')
                        prognoz = prognoz.replace('</i>', '')
                        znach = html.findAll("p")
                        prognoz+="\n"+str(znach[0])
                        prognoz = prognoz.replace('<p>', '')
                        prognoz = prognoz.replace('</p>', '')
                        bot_api.messages.send(
                            random_id=random.random(),
                            peer_id=event.obj.message['peer_id'],
                            message=prognoz
                        )
                except KeyError:
                    bot_api.messages.send(
                        random_id=random.random(),
                        peer_id=event.obj.message['peer_id'],
                        message='Такого знака не существует'
                    )
            if message_text.lower() == 'кто пидор':
                hahaha = bot_api.messages.getConversationMembers(
                    peer_id=event.message.peer_id
                )
                print(hahaha)
                pidr = random.randint(0, len(hahaha['profiles']) - 1)
                print(pidr)
                bot_api.messages.send(
                    random_id=random.random(),
                    peer_id=event.obj.message['peer_id'],
                    message='[id' + str(hahaha['profiles'][pidr]['id']) + '|Пидор]'
                )
            if message_text.lower()=='сделай очередь':
                prof_info = bot_api.messages.getConversationMembers(
                    peer_id=event.message.peer_id
                )
                print(prof_info)
                chil_numb = list(range(0, len(prof_info['profiles'])))
                random.shuffle(chil_numb)
                queue='Очередь\n'
                j=0
                for i in chil_numb:
                    j+=1
                    queue+=str(j)+'.[id'+str(prof_info['profiles'][i]['id'])+'|'+prof_info['profiles'][i]['first_name']+' '+prof_info['profiles'][i]['last_name']+']\n'
                bot_api.messages.send(
                    random_id=random.random(),
                    peer_id=event.obj.message['peer_id'],
                    message=queue
                )
if __name__ == '__main__':
    main()