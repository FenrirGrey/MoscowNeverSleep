import json

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


def user_create(user_login):
    dannye = ['пароль', 'имя', 'фамилия', 'отчество', 'должность']
    user_info = {dannye[j]:proverka_vvoda(dannye[j])for j in range(0, len(dannye))}
    users = {user_login:user_info}

    print(user_info)
