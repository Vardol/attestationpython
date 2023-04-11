#Database interface - файл отвечающий за хранение и считывание данных
import datetime
import os
import uuid

#вспомогательный метод, который переводит лист строк в строку разделенную заданным разделителем (по умолчанию - ;)
def strlist2dsv(strlist: list,delimiter=";"):
    entry = ""
    for i in range(0,len(strlist)):
        entry += str(strlist[i])
        entry += delimiter
    return entry

# Метод, который генерирует название записой книжки текущего пользователя.
# Пользователь должен быть указан в файле current_username.txt
# Пользователя в этот файл вносит инициализатор
def find_notebook():
    with open("current_username.txt","r", encoding="utf-8") as current_username:
        filename = current_username.read() + ".csv"
    return filename

# Проверяет существование записной книжки текущего пользователя
def check_notebook_exists():
    filename = find_notebook()
    if filename in (os.listdir()): return True
    else: return False

#считывает всю книгу и кладет строки в лист строк
def read_notebook():
    entry_list = []
    with open(find_notebook(), "r", encoding = "utf-8") as notebook:
        for entry_str in notebook:
            entry_list.append(entry_str)
    return entry_list

#записывает всю книгу
def write_notebook(entry_list:list):
    full_notebook = ""
    for string in entry_list:
        full_notebook += string
    with open(find_notebook(), "w", encoding = "utf-8") as notebook:
        notebook.write(full_notebook)
    return entry_list

#добавляет новую запись в файл. При этом присваивая ей id и снабжая временной меткой
def add_new_entry_fromstr(string:str):
    entry = str(uuid.uuid4()) + ";"
    entry += str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")) + ";"
    entry += string
    with open(find_notebook(), "a", encoding = "utf-8") as notebook:
        notebook.write(entry + "\n")
    return True

#вариант для переданного списка строк, а не готовой строки
def add_new_entry_fromstrlst(stringlist:list):
    return add_new_entry_fromstr(strlist2dsv(stringlist))

#создание записи из списка строк, без присвоения нового id - для правки существующих записей
def add_old_entry_fromstrlst(stringlist:list):
    stringlist.pop(1)
    stringlist.insert(1,str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
    with open(find_notebook(), "a", encoding = "utf-8") as notebook:
        notebook.write(strlist2dsv(stringlist) + "\n")
    return True

#поиск записи по заголовку
def find_entry_byheader(header:str):
    entry_list = []
    with open(find_notebook(), "r", encoding = "utf-8") as notebook:
        for entry_str in notebook:
            if entry_str.split(";")[2].lower().count(header.lower()) > 0:
                entry_list.append(entry_str)
    return entry_list

#поиск записи по id
def find_entry_byid(id:str):
    entry_list = []
    with open(find_notebook(), "r", encoding = "utf-8") as notebook:
        for entry_str in notebook:
            if entry_str.split(";")[0].count(id) > 0:
                entry_list.append(entry_str)
    return entry_list

#поиск записи по дате
def find_entry_bydate(date:str):
    entry_list = []
    with open(find_notebook(), "r", encoding = "utf-8") as notebook:
        for entry_str in notebook:
            if entry_str.split(";")[1].split(" ")[0].count(date) > 0:
                entry_list.append(entry_str)
    return entry_list

#удаление по id
#функционал удаления реализован только по id, чтобы избежать ошибок
def delete_entry_byid(id:str):
    full_notebook = []
    with open(find_notebook(), "r", encoding = "utf-8") as notebook:
        for entry_str in notebook:
            if entry_str.split(";")[0].count(id) == 0:
                full_notebook.append(entry_str)
    write_notebook(full_notebook)
    return True

# создает пустую записную книжку (очищает ее, если она была)
def clear_notebook():
    with open(find_notebook(), "w", encoding = "utf-8") as notebook:
        notebook.write("")
    return True

#clear_notebook()
# mylist = list()
# mylist.append("Header")
# mylist.append("TEXTTEXTTEXTTEXT!!!")
# add_new_entry_fromstrlst(mylist)


# mylist = read_notebook()
# mylist.pop()
# write_notebook(mylist)

