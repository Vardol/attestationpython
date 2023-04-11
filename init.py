#модуль инициализатор - настраивает программу и запускает ядро программы

import core # - модуль содержащий саму логику программы
import ui # - модуль содерржащий методы отображения и считывания информации у пользователя
import dbi # - модуль отвечающий за хранение и считывание данных

#метод устанавливающий текущего пользователя (прописывает его в файл)
def set_username(name = "notebook"):
    with open("current_username.txt","w",encoding="utf-8") as current_username:
        current_username.write(name.lower())

#Метод отображения приветствия для пользователя
def greetings():
    print("\n Console notebook v 1.0\n")
    print("print 'quit' or 'exit' or 'выход' to close program\n")

#метод инициализации - считывает имя, прописывает его в текущего пользователя, создает для него записную книжку (если ее не было)
def initialize():
    username = input("Введите имя пользователя (без пробелов и служебных символов): ")
    if username.find(" ") != -1: username = username[:(username.find(" "))]
    set_username(username.lower())
    if not dbi.check_notebook_exists():
        print("Вы еще не заводили свою записную книжку, " + username + ". Либо уже удалили её.")
        dbi.clear_notebook()        #Если не файла для пользователя не существует - мы его создаем
    else: print("С возвращением, " + username)
    ui.print_str("Введите команду ? для получения инструкций.")
    core.notebook_bot(username)


greetings()
initialize()