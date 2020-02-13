import json

# функция, позволяющая без проблем запихать словарь в json
def set_default(obj):   # нужно при записи добавлять аргумент - json.dump(data, write_file, default=set_default)
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
        # 15 - это счетчик, сколько раз я бессмысленно пырила в эту функцию в попытках понять

# функция проверки вводимых данных на правильность
def proverka_vvoda (vvod):
    if vvod == 'логин' or vvod == 'пароль':
        not_symvol = r"'@:; /|\*-+_#№$%^&?!.,[]{}()`"   # список запрещенных символов ля логина/пароля
    else:
        not_symvol = r"'@/\*+_#№$%^&[]{}`"  # список запрещенных символов для всего остального
    n = ""   # переменная, для проверки пустого поля
    k = 1   # это счетчик для цикла while, отстань от него

    # дополнительная функция, прогоняющая входщие данные через список запрещенных символов
    # и в случае совпадения, возвращает 0, иначе - 1
    # сама функция существует в связи с тем, что нельзя загнать for под elif
    def symvol_test ():
        for i in range (0, len(not_symvol)):
            if from_user.find(not_symvol[i]) == -1:
                st = 1
            else:
                st = 0
                break
        return st

    while k == 1:   # цикл, гоняющий ввод по кругу, пока пользователь не даст данные в нужном виде
        from_user = input('Введите ' + vvod + ':')
        if from_user == n:
            print ('Поле не может быть пустым')
        elif symvol_test() == 0:
            print ('Нельзя использовать символы')
        elif len(from_user) < 4:
            print ('Нельзя короче 4 символов')
        else:
            k = from_user
            if vvod == 'пароль':    # костыль, чтобы не было нелепого вывода типа "ваш картошка"
                print ('Ваш ' + vvod + ' - ' + str(k))
            elif vvod == 'имя' or vvod == 'отчество':
                print('Ваше ' + vvod + ' - ' + str(k))
            else:
                print('Ваша ' + vvod + ' - ' + str(k))
    return k

# функция создания пользователя, если при попытке залогиниться не был найден такой пользователь
def user_create(user_login):
    with open('users_parametrs.json', 'r', encoding='utf-8') as f:    # подтягиваем из json актуальные параметры пользователя
        dannye = json.load(f)
    with open("users.json", 'r', encoding='utf-8') as read_file:  # подтягиваем всех пользователей с данными в переменную
        users = json.load(read_file)
    user_info = {dannye[j]:proverka_vvoda(dannye[j])for j in range(0, len(dannye))}     # получаем у пользователя инфу по параметрам
    user_info['key'] = 'user'   # добавляем "невидимый" ключ (по умолчанию - user)
    users[user_login] = user_info   # добавляем в переменную со всеми пользователями нового + его данные
    with open("users.json", 'w', encoding='utf-8') as write_file:     # заталкиваем обратно в json всех пользователей
        json.dump(users, write_file, default=set_default, ensure_ascii=False)

# функция, изменяющая параметры пользователя, которые запрашиваются при создании (не закончена)
def parametrs_change(auth_user):     # разрешение на изменение только у админа
    if auth_user == 'admin':
        with open('users_parametrs.json', 'r', encoding='utf-8') as f:    # подтягиваем из json актуальные параметры пользователя
            dannye = json.load(f)
        print('Вы хотите добавить или удалить параметр?')
        ans = input('1 - добавить, 2 - удалить\n')
        if  ans == '1':
            parametr = input('Введите название добавляемого параметра: ')
            if dannye.count(parametr) == 0:
                dannye.append(parametr)
                with open('users.json', 'r', encoding='utf-8') as f:  # подтягиваем из json пользователей, чтобы всем добаввить новый параметр
                    users = json.load(f)                              # в котором по-умолчанию будет значение 'none'
                for key in users:
                    man = users[key]
                    man[parametr] = 'none'
                with open('users.json', 'w', encoding='utf-8') as f:
                    json.dump(users, f, default=set_default, ensure_ascii=False)
            else:
                print('Такой параметр уже существует.')
        elif ans == '2':
            parametr = input('Введите название удаляемого параметра: ')
            if dannye.count(parametr) != 0:
                print('Вы точно уверены, что хотите удалить параметр ' + str(parametr))
                ans2 = input('Да/нет: ')
                if ans2 == 'Да' or ans2 == 'да':
                    print(ans2)
                    dannye.remove(parametr)
                    print(dannye)
                else:
                    print('Выход из функции.')
            else:
                print('Такого параметра нет. Выход из функции')
        else:
            print('Вы ввели неверный вариант. Выход из функции.')
        with open('users_parametrs.json', 'w', encoding='utf-8') as f:
            json.dump(dannye, f, default=set_default, ensure_ascii=False)
    else:
        print('Доступ к управлению параметрами есть только у администратора')

# функция авторизации пользователя
def user_authorization():
    user_login = input('Введите логин: ')
    try:
        with open("users.json", 'r', encoding='utf-8') as read_file:    # пробуем открыть файл пользователей
            users = json.load(read_file)
            user_info = users[user_login]                               # а также пробуем взять оттуда данные пользователя
    except FileNotFoundError:  # нет файла users.json
        print('База пользователей не обнаружена. Будет создана новая база')
        user_login = 'admin'
        print('Создание пользователя ' + user_login)
        user_create(user_login)
    except KeyError:    # в списке пользователей отсутсвует введеный логин
        print('Такого пользователя не существует. Желаете создать?')
        check = input('Да/нет? ')
        if check == 'Да' or 'да':
            user_create(user_login)
        else:
            print('Завершение работы')
    except json.decoder.JSONDecodeError:    # JSON с пользователями пуст. Создается болванка админа (шоб было)
        print('База пользователй существует, но пуста. Будет создан пользователь админ с параметрами по-умолчанию')
        with open("users.json", 'w', encoding='utf-8') as write_file:  # заталкиваем обратно в json всех пользователей
            admin = {"пароль": 'password', "имя": 'admin', "фамилия": 'admin', "отчество": 'admin',
                     "должность": 'admin', 'key': 'admin'}
            user = {}
            user['admin'] = admin
            json.dump(user, write_file, default=set_default, ensure_ascii=False)
        user_login = 'admin'
    else:
        user_password = input('Введите пароль: ')   # все ништь, пользователь есть, ошибок нет, АВТОРИЗАЦИЯ!...
        if user_password == user_info['пароль']:
            print('Добро пожаловать, ' + user_login)
        else:
            print('Неверный пароль')    #    ...или нет :D
            user_login = ''
    return user_login

def user_action():
    def proverka_vvoda_chisla():
        k = 1
        while k == 1:  # цикл, гоняющий ввод по кругу, пока пользователь не даст данные в нужном виде
            vvod = input('Введите желаемое действие: ')
            try:
                s = int(vvod) - 1
            except:
                print('Введите число')
            else:
                k += 1
        return s

    def go_action(user_allows):
        for i in range(0, len(user_allows)):
            print(str(i + 1) + ' - ' + user_allows[i])
        choise = proverka_vvoda_chisla()
        choise = user_allows[choise]
        if

    auth_user = user_authorization()

    with open('users.json', 'r', encoding='utf-8') as f:
        user = json.load(f)
    if auth_user == '':
        print('Пожалуйста, авторизируйтесь')
    else:
        man = user[auth_user]
        with open('users_allows.json', 'r', encoding='utf-8') as f:
            allows = json.load(f)
        if man['key'] == 'admin':
            go_action(allows['admin'])
        elif man['key'] == 'moder':
            go_action(allows['moder'])
        else:
            go_action(allows['user'])