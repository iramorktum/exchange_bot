import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from mysql.connector import connect
from random import shuffle
import re

con = connect(host = 'localhost', user = 'root', password = '', database = 'exchange')
curs = con.cursor()

token = 'b83635630d163e2158ea594aa8ad5e8adbb9cec660f238ec279adf5d5f565830dc3ddd24a67c9997cc198'
bh = vk_api.VkApi(token=token)
give = bh.get_api()
longpoll = VkLongPoll(bh)

cols = ['id', 'my', 'wish', 'ign', 'igntwo', 'time', 'place', 'links', 'ready', 'recip', 'hide']
eq = [['Грозовое племя', 'Гроза'],
          ['Племя Теней', 'Сумрачное племя', 'Тени', 'Сумрак'],
          ['Племя Ветра', 'Ветер'],
          ['Речное племя', 'Река'],
          ['Изгнанники ОВ'],
          ['Клан Падающей Воды', 'КПВ'],
          ['Северный клан', 'Север', 'СК'],
          ['Одиночки ОВ', 'ОВП'],
          ['Домашние'],
          ['Звёздное племя', 'Звездное племя', 'ЗП'],
          ['Сумрачный лес', 'СЛ'],
          ['Душевая', 'Бесплеменные', 'Душ'],
          ['Морское племя', 'Море'],
          ['Племя Луны', 'Луна'],
          ['племя солнца', 'Солнце'],
          ['Одиночки МВ', 'Деревня'],
          ['Изгнанники МВ'],
          ['Вселенная Творцов', 'ВТ']]


def params(x, num = 1):
    if x == 1:
        keyb = VkKeyboard(inline=True)
        keyb.add_button(label='Интересует — №' + str(num), color='secondary')
    elif x == 2:
        keyb = VkKeyboard()
        keyb.add_button(label='Обмен, продажа и покупка', color='primary')
        keyb.add_line()
        keyb.add_button(label='Ищу посредника', color='secondary')
        keyb.add_button(label='Стану посредником', color='secondary')
    elif x == 3:
        keyb = VkKeyboard()
        keyb.add_button(label='Создать анкету', color='primary')
    elif x == 4:
        keyb = VkKeyboard()
        keyb.add_button(label='Вернуться в меню', color='primary')
        keyb.add_line()
        keyb.add_button(label='Изменить анкету', color='secondary')
        keyb.add_button(label='Показать объявления', color='primary')
    elif x == 5:
        keyb = VkKeyboard()
        keyb.add_button(label='Вернуться', color='primary')
        keyb.add_line()
        keyb.add_button(label='Настройки', color='secondary')
        keyb.add_line()
        keyb.add_button(label='Заполнить сначала', color='secondary')
        keyb.add_button(label='Изменить пункт', color='secondary')
    elif x == 6:
        keyb = VkKeyboard()
        keyb.add_button(label='Добавить категорию', color='secondary')
        keyb.add_button(label='Добавить предмет', color='secondary')
        keyb.add_line()
        keyb.add_button(label='Удалить категорию', color='secondary')
        keyb.add_button(label='Удалить предмет', color='secondary')
    elif x == 7:
        keyb = VkKeyboard()
        keyb.add_button(label='А', color='secondary')
        keyb.add_button(label='Б', color='secondary')
    elif x == 8:
        keyb = VkKeyboard()
        keyb.add_button(label='Вернуться', color='primary')
        keyb.add_line()
        keyb.add_button(label='Тип предложений', color='secondary')
        keyb.add_button(label='Режим невидимки', color='secondary')
    keyb = keyb.get_keyboard()
    return keyb


def fix(ar):
    out = []
    for i in range(len(ar)):
        out.append(ar[i])
    return out


def cut(x, y):
    for i in range(len(my[x])):
        for j in range(len(my[y])):
            if my[y].count(my[x][i]) != 0:
                del (my[y][my[y].index(my[x][i])])


def wish(my):
    for i in range(len(my)):
        if i not in (0, 5, 7, 8, 9, 10):
            my[i] = my[i].lower().split(',')
            for j in range(len(my[i])):
                if my[i][j][0] == ' ':
                    my[i][j] = my[i][j][1:]
                if my[i][j][-1] == ' ':
                    my[i][j] = my[i][j][:-1]
    for u in (2, 3, 4):
        for i in range(len(my[u])):
            curs.execute('SELECT * FROM category WHERE name = "' + my[u][i] + '";')
            pos = curs.fetchall()
            if len(pos) > 0:
                try:
                    pos = pos[0]
                    curs.execute('SELECT * FROM category')
                    all = curs.fetchall()
                    num = all.index((pos)) + 1
                    curs.execute('SELECT * FROM items' + str(num) + ';')
                    del (my[u][i])
                    itm = curs.fetchall()
                    for j in range(len(itm)):
                        my[u].append(itm[j][0])
                except IndexError:
                    break
    cut(4, 3)
    cut(3, 2)


def send(id, text):
    bh.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


def send_key(id, text, x, num = 1):
    bh.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': params(x, num)})

def equ(ar):
    fixed = len(ar)
    for i in range(fixed):
        end = False
        for j in range(len(eq)):
            for k in range(len(eq[j])):
                if eq[j][k].lower() == ar[i]:
                    for l in range(len(eq[j])):
                        if eq[j][l] != ar[i]:
                            ar.append(eq[j][l].lower())
            if end:
                break
    return ar


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.text.lower()
            id = event.user_id
            curs.execute("SELECT * FROM ads" + ';')
            ads = curs.fetchall()
            msg = bh.method('messages.getHistory', {'user_id': id, 'count': 2})
            if message == 'начать':
                send_key(id, 'Добро пожаловать! Что вас интересует?', 2)
            elif message == 'вернуться в меню':
                send_key(id, 'Что вас интересует?', 2)
            elif message == 'вернуться':
                curs.execute('SELECT * FROM ads WHERE id = ' + str(id) + ';')
                fetch = curs.fetchall()
                if len(fetch) > 0:
                    send_key(id, 'Ваша анкета уже заполнена. Показать объявления?', 4)
                else:
                    send_key(id, 'Что вас интересует?', 2)
            elif message == 'обмен, продажа и покупка':
                curs.execute('SELECT * FROM ads WHERE id = ' + str(id) + ';')
                fetch = curs.fetchall()
                if len(fetch) == 0:
                    send_key(id, 'Для просмотра объявлений вы должны создать свою анкету.', 3)
                elif fetch[0][-3] == 1:
                    send_key(id, 'Ваша анкета уже заполнена. Показать объявления?', 4)
                curs.execute('SELECT * FROM buy_type WHERE id = ' + str(id) + ';')
                fetch = curs.fetchall()
                if len(fetch) == 0:
                    curs.execute('INSERT INTO buy_type VALUES(' + str(id) + ', "обмен")')
                else:
                    curs.execute('UPDATE buy_type SET type = "обмен" WHERE id = ' + str(id) + ';')
                con.commit()
            elif message == 'создать анкету' or message == 'заполнить сначала':
                if message == 'заполнить сначала':
                    curs.execute('DELETE FROM ads WHERE id = ' + str(id) + ';')
                    con.commit()
                send(id,
                     '1) Вам нужно будет ответить на несколько вопросов, связанных с вашими интересами. Введите через запятую с пробелом свои предметы, которые вы бы хотели обменять или продать.')
            elif message == 'настройки':
                send_key(id, 'Что вы хотите изменить?', 8)
            elif message == 'тип предложений':
                send_key(id, 'Показывать анкеты пользователей только со взаимными интересами (А) или с односторонними в том числе (Б)?', 7)
            elif message == 'режим невидимки':
                send_key(id, 'Показывать пользователям мою анкету (А) или нет (Б)?', 7)
            elif 'Показывать анкеты' in msg['items'][1]['text'] and '8)' not in msg['items'][1]['text']:
                c = 0
                if message == 'а':
                    c = 1
                curs.execute("UPDATE ads SET recip = " + str(c) + " WHERE id = " + str(id) + ";")
                con.commit()
                send_key(id, 'Вы успешно сменили тип предложений. Хотите настроить что-нибудь ещё?', 8)
            elif 'Показывать пользователям' in msg['items'][1]['text'] and '9)' not in msg['items'][1]['text']:
                c = 0
                if message == 'а':
                    c = 1
                curs.execute("UPDATE ads SET hide = " + str(c) + " WHERE id = " + str(id) + ";")
                con.commit()
                send_key(id, 'Вы успешно изменили параметр режима невидимки. Хотите настроить что-нибудь ещё?', 8)
            elif message == 'изменить анкету':
                curs.execute('SELECT * FROM ads WHERE id = ' + str(id))
                try:
                    fetch = curs.fetchall()[0]
                    ad = "Ваша анкета выглядит вот так:\n\n"
                    for i in range(len(fetch) - 4):
                        ad += str(i + 1) + ') ' + fetch[i + 1] + "\n"
                    send_key(id, ad, 5)
                except IndexError:
                    send_key(id, 'У вас нет анкеты.', 3)
            elif message == 'изменить пункт':
                curs.execute('SELECT * FROM ads WHERE id = ' + str(id))
                fetch = curs.fetchall()
                if len(fetch) == 1:
                    send(id, 'Какой пункт вы хотите изменить?')
                else:
                    send_key(id, 'У вас нет анкеты.', 3)
            elif message == 'показать объявления':
                try:
                    curs.execute('SELECT * FROM ads WHERE id = ' + str(id))
                    myp = curs.fetchall()[0]
                    my = fix(myp)
                    wish(my)
                    my_it = my[1]
                    my_wish = my[2]
                    my_place = equ(my[6])
                    curs.execute('SELECT * FROM ads')
                    their = curs.fetchall()
                    shuffle(their)
                    ads = 0
                    for i in range(len(their)):
                        if their[i][0] != id and their[i][-3] and their[i][-1]:
                            th_ = their[i]
                            th = fix(th_)
                            wish(th)
                            good = False
                            for j in range(len(my_place)):
                                if th[6].count(my_place[j]) != 0:
                                    good = True
                            if good:
                                th_it = th[1]
                                th_wish = th[2]
                                c = 0
                                b = 0
                                yes = False
                                for j in range(len(my_wish)):
                                    if th_it.count(my_wish[j]) != 0:
                                        c += 1
                                for j in range(len(th_wish)):
                                    if my_it.count(th_wish[j]) != 0:
                                        b += 1
                                if their[i][-1] == 1 or myp[-1] == 1:
                                    if c > 0 and b > 0:
                                        yes = True
                                elif their[i][-1] == 0 and myp[-1] == 0:
                                    if c > 0 or b > 0:
                                        yes = True
                                if yes:
                                    ads += 1
                                    ad = 'Анкета №' + str(ads) + ':\n'
                                    for j in range(len(th_) - 4):
                                        ad += str(j + 1) + ') ' + str(th_[j + 1]) + "\n"
                                    send_key(id, ad, 1, ads)
                    if not ads:
                        send(id, 'Подходящих объявлений нет.')
                except IndexError:
                    send_key(id, 'У вас нет анкеты.', 3)
            elif 'интересует' in message:
                num = ''
                for i in range(14, len(message)):
                    num += message[i]
                curs.execute("SELECT * FROM ads WHERE id = " + str(id) + ";")
                _anc = curs.fetchall()[0]
                all = bh.method('messages.getHistory', {'user_id': id, 'count': 100})
                for i in range(len(all['items'])):
                    anc = all['items'][i]['text']
                    if 'анкета №' + num in anc.lower():
                        my_anc = ''
                        for j in range(anc.index('1) ') + 3, len(anc)):
                            if anc[j] != '\n':
                                my_anc += anc[j]
                            else:
                                break
                        wish_anc = ''
                        for j in range(anc.index('2) ') + 3, len(anc)):
                            if anc[j] != '\n':
                                wish_anc += anc[j]
                            else:
                                break
                        time_anc = ''
                        for j in range(anc.index('5) ') + 3, len(anc)):
                            if anc[j] != '\n':
                                time_anc += anc[j]
                            else:
                                break
                        curs.execute("SELECT * FROM ads WHERE my = '" + my_anc + "' AND wish = '" + wish_anc + "' AND time = '" + time_anc + "';")
                        anc_own = curs.fetchall()
                        curs.execute('SELECT * FROM likes WHERE id = ' + str(id))
                        likes = curs.fetchall()[0]
                        second_like = False
                        if not isinstance(likes[1], str):
                            curs.execute('UPDATE likes SET liked = "' + str(anc_own[0][0]) + '" WHERE id = ' + str(id))
                            con.commit()
                        else:
                            likes = likes[1].split(', ')
                            for k in likes:
                                if k == str(anc_own[0][0]):
                                    second_like = True
                                    break
                            if not second_like:
                                if '' in likes:
                                    del likes[likes.index('')]
                                likes.append(str(anc_own[0][0]))
                                likes = ', '.join(likes)
                                curs.execute('UPDATE likes SET liked = "' + str(likes) + '" WHERE id = ' + str(id))
                                con.commit()
                        if not second_like:
                            send(id, 'Ваша анкета отправлена этому пользователю!')
                            ad = 'Вами заинтересовался пользователь с этой анкетой:\n'
                            for j in range(1, len(_anc) - 3):
                                ad += str(j) + ') ' + str(_anc[j]) + "\n"
                            send(anc_own[0][0], ad)
                        else:
                            send(id, 'Вы не можете повторно отправить свою анкету этому пользователю.')
                        break
            elif id == 428883129 or id == 516077635:
                msg = bh.method('messages.getHistory', {'user_id': id, 'count': 4})
                if message == 'админ-панель':
                    send_key(id, 'Что вы хотите сделать?', 6)
                elif message == 'добавить категорию':
                    send(id, 'Как будет называться новая категория?')
                elif message == 'удалить предмет':
                    send(id, 'Введите название предмета, который нужно удалить.')
                elif msg['items'][1]['text'] == 'Введите название предмета, который нужно удалить.':
                    curs.execute('SELECT * FROM category;')
                    cat_count = len(curs.fetchall())
                    for i in range(cat_count):
                        curs.execute('DELETE FROM items' + str(i + 1) + ' WHERE name = "' + message + '";')
                        con.commit()
                    send(id, 'Предмет был удалён.')
                elif message == 'удалить категорию':
                    send(id, 'Введите название категории, которую нужно удалить.')
                elif msg['items'][1]['text'] == 'Введите название категории, которую нужно удалить.':
                    curs.execute('SELECT * FROM category;')
                    с = curs.fetchall()
                    for i in range(len(с)):
                        if с[i][0] == message:
                            cat_num = i + 1
                    cat_count = len(с)
                    curs.execute('DROP TABLE items' + str(cat_num) + ';')
                    con.commit()
                    curs.execute('DELETE FROM category WHERE name = "' + message + '";')
                    con.commit()
                    for i in range(cat_num + 1, cat_count + 1):
                        curs.execute('ALTER TABLE items' + str(i) + ' RENAME TO items' + str(i - 1))
                        con.commit()
                    send(id, 'Категория была удалена.')
                elif msg['items'][1]['text'] == 'Как будет называться новая категория?':
                    curs.execute('SELECT * FROM category;')
                    num = len(curs.fetchall()) + 1
                    curs.execute('CREATE TABLE items' + str(num) + '(name varchar(100));')
                    con.commit()
                    curs.execute("INSERT INTO category VALUES ('" + message + "');")
                    con.commit()
                    send(id, 'Категория добавлена!')
                elif message == 'добавить предмет':
                    send(id, 'Как называется предмет?')
                elif msg['items'][1]['text'] == 'Как называется предмет?':
                    send(id, 'Введите через запятую с пробелом имена всех категорий.')
                elif msg['items'][3]['text'] == 'Как называется предмет?':
                    curs.execute('SELECT * FROM category')
                    cats = curs.fetchall()
                    nums = msg['items'][0]['text'].lower().split(', ')
                    name = msg['items'][2]['text'].lower()
                    out = [nums]
                    for j in range(len(out[i])):
                        curs.execute("SELECT * FROM category WHERE name = '" + out[i][j] + "';")
                        next = curs.fetchall()[0]
                        curs.execute('SELECT * FROM items' + str(cats.index(next) + 1))
                        already_in = curs.fetchall()
                        append_item = True
                        for k in already_in:
                            if name == k[0]:
                                append_item = False
                        if append_item:
                            curs.execute("INSERT INTO items" + str(cats.index(next) + 1) + " VALUES ('" + name + "');")
                            con.commit()
                    send(id, 'Предмет добавлен!')
            msg = bh.method('messages.getHistory', {'user_id': id, 'count': 2})
            if msg['items'][1]['text'][1] == ')':
                if msg['items'][1]['text'][0] == '1':
                    curs.execute(
                        "INSERT INTO ads (id, my) VALUES (" + str(id) + ", '" + msg['items'][0]['text'] + "');")
                    con.commit()
                    send(id, '2) Что вы хотели бы получить взамен?')
                else:
                    curs.execute('SELECT * FROM ads WHERE id = ' + str(id) + ';')
                    fetch = curs.fetchall()
                    for i in range(len(fetch[0])):
                        if fetch[0][i] is None:
                            inp = cols[i]
                            break
                    if inp != 'recip' and inp != 'hide':
                        curs.execute("UPDATE ads SET " + inp + " = '" + event.text + "' WHERE id = " + str(id) + ";")
                        con.commit()
                    else:
                        c = 0
                        if event.text.lower() == 'а':
                            c = 1
                        curs.execute("UPDATE ads SET " + inp + " = " + str(c) + " WHERE id = " + str(id) + ";")
                        con.commit()
                    if inp == 'wish':
                        send(id, '3) Введите названия предметов или категорий, которые вас не интересуют.')
                    elif inp == 'ign':
                        send(id,
                             '4) Есть ли предметы-исключения, которые вы бы не отказались видеть, несмотря на игнорируемые категории?')
                    elif inp == 'igntwo':
                        send(id, '5) В какие сроки вы хотели бы уложиться?')
                    elif inp == 'time':
                        send(id, '6) Назовите фракции и места, к которым у вас есть доступ.')
                    elif inp == 'place':
                        send(id, '7) Оставьте данные для обратной связи с потенциально заинтересованными.')
                    elif inp == 'links':
                        curs.execute('UPDATE ads SET ready = 1 WHERE id = ' + str(id) + ';')
                        con.commit()
                        curs.execute('DELETE FROM likes WHERE id = ' + str(id) + ';')
                        curs.execute('INSERT INTO likes (id) VALUES (' + str(id) + ')')
                        con.commit()
                        curs.execute('SELECT * FROM likes')
                        likes_all = curs.fetchall()
                        for i in likes_all:
                            if i[0] != id and i[1] != '[]' and isinstance(i[1], str):
                                a = i[1].split(', ')
                                try:
                                    del a[a.index(str(id))]
                                except ValueError:
                                    pass
                                ', '.join(a)
                                if not a:
                                    a = ''
                                curs.execute('UPDATE likes SET liked = "' + str(a) + '" WHERE id = ' + str(i[0]) + ';')
                                con.commit()
                        send_key(id, '8) Показывать анкеты пользователей только со взаимными интересами (А) или с односторонними в том числе (Б)?', 7)
                    elif inp == 'recip':
                        send_key(id, '9) Показывать пользователям мою анкету (А) или нет (Б)?', 7)
                    else:
                        send_key(id, 'Анкета готова. Показать объявления?', 4)
                        curs.execute('SELECT * FROM ads WHERE id = ' + str(id))
                        myp = curs.fetchall()[0]
                        my = fix(myp)
                        wish(my)
                        my_it = my[1]
                        my_wish = my[2]
                        my_place = equ(my[6])
                        curs.execute('SELECT * FROM ads')
                        their = curs.fetchall()
                        shuffle(their)
                        ads = 0
                        for i in range(len(their)):
                            if their[i][0] != id and their[i][-3] and their[i][-1]:
                                th_ = their[i]
                                th = fix(th_)
                                wish(th)
                                good = False
                                for j in range(len(my_place)):
                                    if th[6].count(my_place[j]) != 0:
                                        good = True
                                if good:
                                    th_it = th[1]
                                    th_wish = th[2]
                                    c = 0
                                    b = 0
                                    yes = False
                                    for j in range(len(my_wish)):
                                        if th_it.count(my_wish[j]) != 0:
                                            c += 1
                                    for j in range(len(th_wish)):
                                        if my_it.count(th_wish[j]) != 0:
                                            b += 1
                                    if their[i][-1] == 1 or myp[-1] == 1:
                                        if c > 0 and b > 0:
                                            yes = True
                                    elif their[i][-1] == 0 and myp[-1] == 0:
                                        if c > 0 or b > 0:
                                            yes = True
                                    if yes:
                                        msg = bh.method('messages.getHistory', {'user_id': th[0], 'count': 30})
                                        for j in range(len(msg['items'])):
                                            if 'анкета №' in msg['items'][j]['text'].lower():
                                                ads = int(re.findall('[\d]{1,3}', msg['items'][j]['text'])[0])
                                                break
                                        ad = 'Появилась новая анкета №' + str(ads + 1) + ':\n'
                                        for j in range(len(myp) - 4):
                                            ad += str(j + 1) + ') ' + str(myp[j + 1]) + "\n"
                                        send_key(th[0], ad, 1, ads + 1)
            elif msg['items'][1]['text'] == 'Какой пункт вы хотите изменить?':
                send(id, 'Введите новое значение этого пункта.')
            msg = bh.method('messages.getHistory', {'user_id': id, 'count': 4})
            if msg['items'][3]['text'] == 'Какой пункт вы хотите изменить?':
                inp = cols[int(msg['items'][2]['text'])]
                curs.execute("UPDATE ads SET " + inp + " = '" + event.text + "' WHERE id = " + str(id) + ";")
                con.commit()
                curs.execute('DELETE FROM likes WHERE id = ' + str(id))
                con.commit()
                curs.execute('INSERT INTO likes (id) VALUES (' + str(id) + ')')
                con.commit()
                curs.execute('SELECT * FROM likes')
                likes_all = curs.fetchall()
                for i in likes_all:
                    if i[0] != id and isinstance(i[1], str):
                        a = i[1].split(', ')
                        try:
                            del a[a.index(str(id))]
                        except ValueError:
                            pass
                        a = ', '.join(a)
                        if not a:
                            a = ''
                        curs.execute('UPDATE likes SET liked = "' + str(a) + '" WHERE id = ' + str(i[0]))
                        con.commit()
                send_key(id, 'Вы успешно изменили анкету!', 5)
