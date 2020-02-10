from functions import user_create

filename = open('users.txt', 'r')
users = filename.read()
filename.close()
user_login = input('Введите логин: ')
try:
    users[user_login]
except KeyError:
    print('Такого пользователя не существует. Желаете создать?')
    check = input('Да/нет? ')
    if check == 'Да' or 'да':
        user_create(user_login)
    else:
        print ('Завершение работы')
else:
    print ('Добро пожаловать, ' + user_login)
    print ('Ваши даные')








