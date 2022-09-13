<<<<<<< HEAD
from datetime import datetime
from tkinter import *
from tkinter.filedialog import *
from tkinter import scrolledtext 
import pandas
import json
from datetime import datetime, timedelta
import os
import os.path
import shutil
import numpy

def log_load():
    log_txt_ok.delete('1.0', END)
    log_txt_fail.delete('1.0', END)
    name = os.path.basename(log_fp)
    dst = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    fail_log = dst + """\Input_Error\\""" + name + "-FAIL.log"
    ok_log = dst + """\Input_Error\\""" + name + "-OK.log"
    if gl_lang == 'rus':
        dst2 = dst + """\Input\Test\\""" + name
    else:
        dst2 = dst + """\Input\Test_ENG\\""" + name
    try:
        excel_df = pandas.read_excel(dst2, sheet_name='1556')
    except FileNotFoundError:
        log_txt_ok.insert(INSERT, 'Файл пропал - иди разбирайся сам...\n')
    else:
        log_txt_ok.insert(INSERT, 'Файл на меcте - еще грузится.\n')
    try:
        with open(ok_log, 'r') as f:
            o = f.read()
    except FileNotFoundError:
        log_txt_ok.insert(INSERT, 'No log file\n')
    else:
        log_txt_ok.insert(INSERT, '\n' + o)
    try:
        with open(fail_log, 'r') as f:
                o = f.read()
    except FileNotFoundError:
        log_txt_fail.insert(INSERT, 'No log file\n')
    else:
        log_txt_fail.insert(INSERT, '\n' + o)

def write_file(excel_df, lang, filepath):
    #writer = pandas.ExcelWriter(filepath, engine='xlsxwriter')
    #excel_df.to_excel(writer, '1556')
    #writer.save()
    dst = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if lang == 'rus':
        dst = dst + """\Input\Test"""
    else:
        dst = dst + """\Input\Test_ENG"""
    shutil.copy(filepath, dst, follow_symlinks=True)
    log_txt.insert(INSERT, 'Файл скопирован.\n\n')
    df = pandas.DataFrame(numpy.arange(15).reshape(3,5))
    log_txt.insert(INSERT, 'Строк в таблице - ' + str(excel_df.shape[0]))
    global log_fp
    global log_fd
    global gl_lang
    log_fp = filepath
    log_fd = dst
    gl_lang = lang


#хуята для правки даты из инта для экселя (не закончено)
def from_excel_ordinal(ordinal, _epoch0=datetime(1899, 12, 31)):
    if ordinal >= 60:
        ordinal -= 1  # Excel leap year bug, 1900 is not a leap year!
    return (_epoch0 + timedelta(days=ordinal)).replace(microsecond=0)

def open_file():
    def check_data(excel_df, lang, filepath):
        #дергалка типа документа для проверки серии и номера по правилу потом
        def check_doctype(excel_df,i):
            val = excel_df['Тип документа']
            if val[i] == "ПАСПОРТ РФ":
                return(1)
            elif val[i] == "ЗАГРАНПАСПОРТ ГРАЖДАНИНА РФ":
                return(2)
            elif val[i] == "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ":
                return(3)
            elif val[i] == "ПАСПОРТ ИНОСТРАННОГО ГРАЖДАНИНА":
                return(4)
            elif val[i] == "ВИД НА ЖИТЕЛЬСТВО":
                return(5)
            else:
                return(6)

        log_txt.insert(INSERT, 'Запуск функции проверки данных\n\n')

        #Правим СНИЛС
        excel_df['СНИЛС'] = excel_df['СНИЛС'].astype(object)
        val = excel_df['СНИЛС']
        x = '00000000000'
        y = '00000000nan'
        for i in range (0,len(val)):
            a = str(val[i])
            b = a.replace("-", "")
            a = b.replace(" ","")
            while len(a)<11:
                c = str('0')
                a = c + a
            val[i] = a
            if val[i] == x:
                val[i] = ''
            if val[i] == y:
                val[i] = ''                
        excel_df['СНИЛС'] = val

       #правим тип документа
        val = excel_df['Тип документа']
        dst = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        filename3 = dst + '\\EmportUp\\files\\doctype.json'
        filename4 = dst + '\\EmportUp\\files\\doctype_var.json'
        with open(filename3, 'r', encoding='utf-8') as f:
            cols = json.load(f)
        with open(filename4, 'r', encoding='utf-8') as f:
            var_cols = json.load(f)

        for i in range (0, len(val)):
            x = 1
            for j in range (0, len(cols)):
                if val[i] == cols[j]:
                    x = 2
                    break
            if x != 2:
                for j in range (0,len(cols)):
                    s = var_cols[cols[j]]
                    for k in range(0, len(s)):
                        if s[k] == val[i]:
                            val[i] = cols[j]
        excel_df['Тип документа'] = val


        #правим номер документа и серию в зависимости от типа
        excel_df['Серия документа'] = excel_df['Серия документа'].astype(object)
        excel_df['Номер документа'] = excel_df['Номер документа'].astype(object)
        val = excel_df['Серия документа']
        val2 = excel_df['Номер документа']
                
        for i in range (0,len(val)):
            a = str(val[i])
            b = a.replace("-", "")
            a = b.replace(" ","")
            val[i] = a
        for i in range (0,len(val2)):
            a = str(val2[i])
            b = a.replace("-", "")
            a = b.replace(" ","")
            val2[i] = a            
        for i in range(0, len(val)):
            d_tpe = check_doctype(excel_df,i)
            c = str('0')
            if d_tpe == 1:
                a = str(val[i])
                while len(a)<4:
                    a = c + a
                    val[i] = a
                b = str(val2[i])
                while len(b)<6:
                    b = c + b
                    val2[i] = b
            if d_tpe == 2 or d_tpe == 5:
                a = str(val[i])
                while len(a)<2:
                    a = c + a
                    val[i] = a
                b = str(val2[i])
                while len(b)<7:
                    b = c + b
                    val2[i] = b
        excel_df['Серия документа'] = val
        excel_df['Номер документа'] = val2    

        #правим колонку Услуг
        excel_df['Услуга'] = excel_df['Услуга'].astype(object)
        val = excel_df['Услуга']
        for i in range (0,len(val)):
            a = str(val[i])
            b = a.replace(";", ",")
            a = b.replace(" ","")
            b = a.replace("Р","P")
            a = b.replace("К","K")
            b = a.replace("В","B")
            val[i] = b
        excel_df['Услуга'] = val 
        log_txt.insert(INSERT, 'Данные исправлены. Копируем файл в необходимую папку\n\n')               
        write_file(excel_df,lang,filepath)

   



    def rename_columns(miss_cols, bad_cols, lang, filepath):
        dst = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if lang == 'rus':
            filename2 = dst + '\\EmportUp\\files\\various.json'
        else:
            filename2 = dst + '\\EmportUp\\files\\various_eng.json'
        with open(filename2, 'r', encoding='utf-8') as f:
            var_cols = json.load(f)
        s = []
        d = []
        ddd = []
        for i in range(0, len(miss_cols)):
            s = var_cols[miss_cols[i]]
            for ii in range(0, len(s)):
                for iii in range(0, len(bad_cols)):
                    if s[ii] == bad_cols[iii]:
                        excel_df.rename(columns={bad_cols[iii]: miss_cols[i]}, inplace=True)
                        d.append(miss_cols[i])
                        ddd.append(bad_cols[iii])
        for x in d:
            miss_cols.remove(x)
        for x in ddd:
            bad_cols.remove(x)
        ex_cols = excel_df.columns.ravel()
        check_columns(ex_cols, lang, filepath, 2)


    def check_columns(ex_cols, lang, filepath, trai):
        dst = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        print(dst)
        if lang == 'rus':
            filename = dst + '\\EmportUp\\files\\columns.json'
        else:
            filename = dst + '\\EmportUp\\files\\columns_eng.json'
        bad_cols = []
        for i in range(0, len(ex_cols)):
            bad_cols.append(ex_cols[i])
            # загружаем список необходимых колонок
            cols = []
            miss_cols = []
            with open(filename, 'r', encoding='utf-8') as f:
                cols = json.load(f)
            with open(filename, 'r', encoding='utf-8') as f:  # поправить эту порнографию
                miss_cols = json.load(f)

        for i in range(0, len(cols)):
            x = 1
            for j in range(0, len(ex_cols)):
                if cols[i] == ex_cols[j]:
                    while x == 1:  # удалим лишник заголовки
                        try:
                            miss_cols.remove(ex_cols[j])
                            bad_cols.remove(ex_cols[j])
                        except ValueError:
                            x = 2
        try:
            miss_cols[0]
        except IndexError:
            log_txt.insert(INSERT, 'Нет неверных колонок. Проверяем данные\n\n')
            check_data(excel_df, lang, filepath)
        else:
            try:
                bad_cols[0]
            except IndexError:
                for c in miss_cols:
                    for index, row in excel_df.iterrows(): excel_df.at[index, c] = None
                    check_data(excel_df, lang, filepath)
            else:
                if trai == 1:
                    log_txt.insert(INSERT, 'Запуск функции переименовывания колонок\n\n')
                    rename_columns(miss_cols, bad_cols, lang, filepath)
                else:
                    log_txt.insert(INSERT, 'Что-то пошло не так. Измените названия колонок вручную\n\n')
                    os.startfile(filepath)


    filepath = askopenfilename()  # получаем название файла
    ex_cols = []
    log_txt.delete('1.0', END)
    log_txt_ok.delete('1.0', END)
    log_txt_fail.delete('1.0', END)
    try:
        excel_df = pandas.read_excel(filepath, sheet_name='1556')
    except:
        xl = pandas.ExcelFile(filepath)
        a = xl.sheet_names
        excel_df = pandas.read_excel(filepath, sheet_name=a[0])
        log_txt.insert(INSERT, """В файле нет листа '1556', открываем первый лист\n\n""")
    else:
        log_txt.insert(INSERT, "Файл открыт\n\n")
    finally:
        ex_cols = excel_df.columns.ravel()  
        cols_test = []
        for i in range(0, len(ex_cols)):
            cols_test.append(ex_cols[i])
        if cols_test.count('ENG') > 0 or cols_test.count('eng') > 0:
            log_txt.insert(INSERT, """В файле обнаружена колонка 'ENG'\n""")
            log_txt.insert(INSERT, 'Запуск функции проверки колонок\n\n')
            check_columns(cols_test, 'eng', filepath, 1)
        else:
            log_txt.insert(INSERT, """Колонка 'ENG' отсутствует\n""")
            log_txt.insert(INSERT, 'Запуск функции проверки колонок\n\n')
            check_columns(cols_test, 'rus', filepath, 1)


log_fp = 'hello, motherfucker'
log_fd = 'how is your ass going?'
gl_lang = 'no'

root = Tk()
root.title("Антиманагер")
root.minsize(width=500, height=400)

btn = Button(root, text="Открыть файл", command=open_file)
btn_log = Button(root, text="Проверить логи", command=log_load)    
lbl = Label(root, text="Логи событий")
lbl_lo = Label(root, text="Логи записей")  
lbl_lf = Label(root, text="Логи ошибок")   
lbl2 = Label(root, text="                  ")  
log_txt = scrolledtext.ScrolledText(root, width=40, height=15)
log_txt_ok = scrolledtext.ScrolledText(root, width=40, height=30) 
log_txt_fail = scrolledtext.ScrolledText(root, width=40, height=30) 



btn.grid(column=0, row=0)
btn_log.grid(column=0, row=1)  
lbl.grid(column=2, row=0)  
lbl2.grid(column=1, row=0)
lbl2.grid(column=1, row=1)
lbl_lo.grid(column=0, row=2)  
lbl_lf.grid(column=2, row=2)  
log_txt.grid(column=2, row=1)
log_txt_ok.grid(column=0, row=3)
log_txt_fail.grid(column=2, row=3)


root.mainloop()
=======
print("ПИЗДЕЦ")
>>>>>>> 051a9ff8c4d2e1bfbd7e51f93089f04db67f5d02
