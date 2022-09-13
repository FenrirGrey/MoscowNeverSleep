import json  # загружаем список необходимых колонок

cols = {}
cols_eng = {}
columns = []
columns_eng = []
service = {}
doctype = {}

cols ={"ФИО": ["ФИО полностью", "Сотрудники", "ФИО сотрудника", "ФИО (полное)","фио"],
        "Дата рождения": ["дата рождения"],
        "Пол": ["пол", "ПОЛ"],
        "Тип документа": ["тип документа", "Тип Документа", "Тип"],
        "Серия документа": ["Серия паспорта", "Серия", "Серия Паспорта", "серия паспорта","Серияпаспорта"],
        "Номер документа": ["Номер", "номер паспорта", "Номерпаспорта"],
        "Дата выдачи документа": ["Дата выдачи", "Дата выдачи документа", "Когда Выдан", "Дата Выдачи Паспорта", "дата выдачи паспорта"],
        "Кем выдан": ["Кем  ", "Место выдачи документа", "Удостоверение.Кем выдан", "кем выдан"],
        "Адрес фактического проживания": ["Адрес проживания", "Фактический адрес", "Адрес места проживания","адрес фактического проживания"],
        "Место работы": ["место работы"],
        "ЛПУ": ["лпу"],
        "Телефон": ["Телефон мобильный", "Физическое лицо.Мобильный телефон", "телефон"],
        "СМС": ["смс", "SMS"],
        "Почта": ["Эл.почта", "Электронная почта", "почта", "E-Mail", "ПОЧТА"],
        "Результаты на почту": ["Результат на почту", "результаты на почту"],
        "СНИЛС": ["страховой полис", "Снилс", "снилс"],
        "Услуга": ["Услуги", "услуга"],
        "Дата взятия": ["дата взятия","Дата выдачи результата"],
        "Код отделения": ["код отделения", "отделение"],
        "Штрихкод": ["штрихкод","Штрих код"]}

cols_eng ={"ФИО": ["ФИО полностью", "Сотрудники", "ФИО сотрудника", "ФИО (полное)","фио"],
        "Дата рождения": ["дата рождения"],
        "Пол": ["пол", "ПОЛ"],
        "Тип документа": ["тип документа", "Тип Документа", "Тип"],
        "Серия документа": ["Серия паспорта", "Серия", "Серия Паспорта", "серия паспорта","Серияпаспорта", "серия документа", "Серия Документа"],
        "Номер документа": ["Номер", "номер паспорта", "Номерпаспорта", "номер документа", "Номер Документа"],
        "Дата выдачи документа": ["Дата выдачи", "Дата выдачи документа", "Когда Выдан", "Дата Выдачи Паспорта", "дата выдачи паспорта"],
        "Кем выдан": ["Кем  ", "Место выдачи документа", "Удостоверение.Кем выдан", "кем выдан"],
        "Адрес фактического проживания": ["Адрес проживания", "Фактический адрес", "Адрес места проживания","адрес фактического проживания"],
        "Место работы": ["место работы"],
        "ЛПУ": ["лпу"],
        "Телефон": ["Телефон мобильный", "Физическое лицо.Мобильный телефон", "телефон"],
        "СМС": ["смс", "SMS"],
        "Почта": ["Эл.почта", "Электронная почта", "почта", "E-Mail", "ПОЧТА"],
        "Результаты на почту": ["Результат на почту", "результаты на почту"],
        "СНИЛС": ["страховой полис", "Снилс", "снилс"],
        "ENG": ["eng","ENG (как в заграничном паспорте)"],
        "Дата взятия": ["дата взятия","Дата выдачи результата"],
        "Код отделения": ["код отделения", "отделение"],
        "Штрихкод": ["штрихкод","Штрих код"]}

columns = ['ФИО', 'Дата рождения', 'Пол', 'Тип документа', 'Серия документа', 'Номер документа', 'Дата выдачи документа', 'Кем выдан', 
           'Адрес фактического проживания', 'Место работы', 'ЛПУ', 'Телефон', 'СМС', 'Почта', 'Результаты на почту', 'СНИЛС', 'Услуга', 'Дата взятия', 'Код отделения', 'Штрихкод']

columns_eng = ['ФИО', 'Дата рождения', 'Пол', 'Тип документа', 'Серия документа', 'Номер документа', 'Дата выдачи документа', 'Кем выдан',
           'Адрес фактического проживания', 'Место работы', 'ЛПУ', 'Телефон', 'СМС', 'Почта', 'Результаты на почту', 'СНИЛС', 'Услуга', 'Дата взятия', 'ENG', 'Код отделения', 'Штрихкод']

service = {}

doctype = ['ПАСПОРТ РФ','ЗАГРАНПАСПОРТ ГРАЖДАНИНА РФ','СВИДЕТЕЛЬСТВО О РОЖДЕНИИ','ПАСПОРТ ИНОСТРАННОГО ГРАЖДАНИНА','ВИД НА ЖИТЕЛЬСТВО']
doctype_var = {"ПАСПОРТ РФ":['паспорт','паспорт рф', 'паспорт РФ','Паспорт РФ','ПАСПОРТ','Паспорт', 'Паспорт гражданина РФ','ПАСПОРТ ГРАЖДАНИНА РФ'],
        "ЗАГРАНПАСПОРТ ГРАЖДАНИНА РФ":['загранпаспорт гражданина рф', 'загранпаспорт гражданина РФ','загранник', 'загран паспорт','ЗАГРАНПАСПОРТ ГРАЖДАНКИ РФ', 'заграничный паспорт РФ','загран паспорт гражданина РФ','ЗАГРАНПАСПОРТ'],
        "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ":['свидетельство о рождении', 'свидетельство','СВ.О РОЖДЕН.','СВ.О РОЖДЕН','свид.о рождении'],
        "ПАСПОРТ ИНОСТРАННОГО ГРАЖДАНИНА":['паспорт иностранного гражданина', 'иностранный паспорт','Паспорт иностранного гражданина'],
        "ВИД НА ЖИТЕЛЬСТВО":['вид на жительство']}


file_cols = 'various.json'
file_cols_eng = 'various_eng.json'
file_columns = 'columns.json'
file_columns_eng = 'columns_eng.json'
file_service = 'service.json'
file_doctype = 'doctype.json'
file_doctype_var = 'doctype_var.json'

with open(file_cols, 'w', encoding='utf-8') as f:
    json.dump(cols, f, ensure_ascii=False)
with open(file_cols_eng, 'w', encoding='utf-8') as f:
    json.dump(cols_eng, f, ensure_ascii=False)
with open(file_columns, 'w', encoding='utf-8') as f:
    json.dump(columns, f, ensure_ascii=False)
with open(file_columns_eng, 'w', encoding='utf-8') as f:
    json.dump(columns_eng, f, ensure_ascii=False)
with open(file_service, 'w', encoding='utf-8') as f:
    json.dump(service, f, ensure_ascii=False)
with open(file_doctype, 'w', encoding='utf-8') as f:
    json.dump(doctype, f, ensure_ascii=False)
with open(file_doctype_var, 'w', encoding='utf-8') as f:
    json.dump(doctype_var, f, ensure_ascii=False)