#метод вывода записи
def show_entry(entry:str):
    entry_list = entry.split(";")
    print("Дата изменения: " + entry_list[1] + ".")
    print("________________________________________________")
    print("Тема: " + entry_list[2])
    print(entry_list[3])
    print("________________________________________________")
    return entry

#служебный метод для вывода записи с ID
def show_entry_id(entry:str):
    entry_list = entry.split(";")
    print("ID записи: " + entry_list[0] + ".")
    show_entry(entry)
    return entry

#метод вывода нескольких записей
def show_entries(entries:list):
    for element in entries:
        show_entry(element)
        print("\n")

def print_str(string:str):
    print(string)
    return string


def read_string(prompting_msg = "\n"):
    string = input(prompting_msg)
    return string