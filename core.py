import dbi
import ui
import utils # вспомогательный модуль с полезными для меня утилитами (сам сделал и использовал в разнык проектах)

def instructions():
    instructions = ""
    instructions += "Консольный бот позволяет вести заметки.\n"
    instructions += "Бот хранит отдельные записные книжки для каждого пользователя.\n"
    instructions += "Для работы с ботом необходимо ввести команды из списка ниже.\n"
    instructions += "При вводе заголовка и/или текста заметки нельзя использовать <;> и переход на новую строку.\n"
    instructions += "Ниже представлен доступный список команд\n"
    instructions += "__________________________________________________________________________________________\n"
    instructions += "ADD (ДОБАВИТЬ, ДОБАВЬ) - добавляет запись в расписание. При отсутствии дня и/или времени, запись рассматривается как ежедневная и/или на целый день\n"
    instructions += "PRINT (SHOW, ПЕЧАТЬ) - выводит всю записную книжку.\n"
    instructions += "DATE (ДАТА, FIND, НАЙТИ, НАЙДИ) - поиск записей по дате.\n"
    instructions += "HEADER (HEAD, TEXT, ЗАГОЛОВОК, ТЕКСТ) - поиск записей по заголовку.\n"
    instructions += "DEL (DELETE, УДАЛИТЬ, УДАЛИ) - добавляет запись в расписание.\n"
    instructions += "UPD (CHANGE, ИЗМЕНИТЬ, UPDATE) - добавляет запись в расписание.\n"
    instructions += "CLEAR (CLR, ОЧИСТИТЬ) - полностью очищает расписание.\n"
    instructions += "HELP (?, ПОМОЩЬ, СОС, SOS) - выводит инструкцию по работе.\n"
    instructions += "QUIT (EXIT, ВЫХОД) - закрыть программу.\n"
    return instructions

#Метод для получения подтверждения пользователя
def confirm(input_str = ""):
    answer = utils.check_quit(input(input_str + "Вы уверены? Y/N (Д/Н) - ")).upper()
    if answer == "Y" or answer == "Д": return True
    else: return False

#собственно логика работы записной книжки - метод запускается модулем инициализатором init.py
def notebook_bot(username: str):
    while True:
        request = utils.check_quit(ui.read_string("Введите команду: ")).upper()
        delete_command_flag = False
        update_command_flag = False

        if request == "DEL" or request == "DELETE" or request == "УДАЛИТЬ" or request == "УДАЛИ":
            delete_command_flag = True

        if request == "UPDATE" or request == "ИЗМЕНИТЬ" or request == "CHANGE" or request == "UPD":
            update_command_flag = True

        if request == "ADD" or request == "ДОБАВИТЬ" or request == "ДОБАВЬ":
            entry = list()
            entry.append(ui.read_string("Введите заголовок новой заметки: "))
            entry.append(ui.read_string("Введите текст новой заметки: "))
            if len(entry[0]) == 0:
                entry[0] = "-"
            if len(entry[1]) == 0:
                entry[0] = "-----"
            if dbi.add_new_entry_fromstrlst(entry): ui.print_str("Успешно!")

        elif request == "PRINT" or request == "SHOW" or request == "ПЕЧАТЬ":
            full_notebook = dbi.read_notebook()
            ui.show_entries(full_notebook)

        elif request == "FIND" or request == "НАЙТИ" or request == "НАЙДИ" or request == "DATE" or request == "ДАТА":
            result = dbi.find_entry_bydate(ui.read_string("введите день в формате <XX.XX> или <XX.XX.XXXX>, либо месяц в формате <XX.XXXX>, либо год в формате <XXXX>) - "))
            if len(result) == 0: ui.print_str("Не найдено записей, соответствующих запросу")
            ui.show_entries(result)

#TODO: тут надо будет сменить логику, чтобы удаление было за счет поиска по id.
# Иначе заголовки могут совпадать и пользователь никогда не сможет удалить одну запись.
# При этом не меняя стандартного отображения записей, т.к. внешний вид uuid несколько обескураживает.
# Но я явно не успеваю сделать этого в текущем спринте, а это последний спринт до сдачи.
        elif request == "HEADER" or request == "HEAD" or request == "TEXT" or request == "ЗАГОЛОВОК" or request == "ТЕКСТ" or delete_command_flag or update_command_flag:
            if delete_command_flag: ui.print_str("Необходимо выбрать запись для удаления")
            if update_command_flag: ui.print_str("Необходимо выбрать запись для изменения")
            result = dbi.find_entry_byheader(ui.read_string("Введите строку для поиска записи по заголовку - "))
            length = len(result)
            if length <= 0: ui.print_str("Не найдено записей соответствующих запросу")
            else:
                if delete_command_flag or update_command_flag:
                    if length > 1: ui.print_str("Найдено более 1 записи соответствующей запросу. Повторите запрос более точно.")
                    else:
                        if delete_command_flag:
                            ui.print_str("Найдена 1 запись:")
                            ui.show_entries(result)
                            if confirm("Удалить эту запись? "):
                                if dbi.delete_entry_byid(result[0].split(";")[0]): ui.print_str("Успешно")
                        if update_command_flag:
                            ui.print_str("Найдена 1 запись:")
                            ui.show_entries(result)
                            if confirm("Изменить эту запись? "):
                                old_entry_str_list = result[0].split(";")
                                new_entry_str_list = list()
                                new_entry_str_list.append(old_entry_str_list[0])
                                new_entry_str_list.append(old_entry_str_list[1])
                                ui.print_str("Текущий заголовок: " + old_entry_str_list[2])
                                new_entry_str_list.append(ui.read_string("Введите новый заголовок, либо нажмите ENTER, чтобы сохранить текущий: "))
                                if len(new_entry_str_list[2]) == 0:
                                    new_entry_str_list.pop(2)
                                    new_entry_str_list.append(old_entry_str_list[2])
                                ui.print_str("Текущий текст: " + old_entry_str_list[3])
                                new_entry_str_list.append(ui.read_string("Введите новый текст заметки, либо нажмите ENTER, чтобы сохранить текущий: "))
                                if len(new_entry_str_list[3]) == 0:
                                    new_entry_str_list.pop(3)
                                    new_entry_str_list.append(old_entry_str_list[3])
                                if dbi.delete_entry_byid(new_entry_str_list[0]) and dbi.add_old_entry_fromstrlst(new_entry_str_list):
                                    ui.print_str("Успешно")

                else:
                    ui.show_entries(result)


        elif request == "CLEAR" or request == "CLR" or request == "ОЧИСТИТЬ":
            if confirm("Очистить все расписание? "):
                if dbi.clear_notebook(): ui.print_str("Успешно!")

        elif request == "HELP" or request == "?" or request == "ПОМОЩЬ" or request == "СОС" or request == "SOS" or request == "COC":
            ui.print_str(instructions())

        else: print("Нераспознанная команда.\n")