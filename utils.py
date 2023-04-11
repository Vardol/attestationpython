# вспомогательный модуль с полезными для меня утилитами (сам сделал и использовал в разнык проектах)


#проверяем все вводы строк на выражение волеизъявления пользователя прекратить происходящее
def check_quit(input_str: str):
    input_str = input_str.lower()
    if len(input_str) == 4 and (input_str.find("quit") != -1 or input_str.find("exit") != -1 or input_str.find("выход") != -1): exit()
    else: return input_str

#замена символа в строке по индексу
def str_replace_char_byindex(input_str: str, index_to_replace: int, str_toinsert: str):
    if index_to_replace not in range(0,len(input_str)) or str_toinsert == "": return input_str
    else:
        l = list(input_str)
        l[index_to_replace] = str_toinsert
        return "".join(l)