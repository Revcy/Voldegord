import telebot as tg

data_file = 'bot_info/userlist_notice.txt'

def notice_check_status(user_id):
    func_result = ''

    with open(data_file, 'r', encoding='utf8') as file:
        user_list = file.readlines()
        file.close()

    for user_info in user_list:
        if str(user_id) in user_info:
            func_result = 'allow'
            break
        else:
            func_result = 'reject'

    if func_result == 'allow':
        return True
    else:
        return False
    
def notice_user_add(user_id):
    with open(data_file, 'w', encoding='utf8') as file:
        file.write(f'{user_id}')
        file.close()

def notice_user_delete(user_id):
    with open(data_file, 'r', encoding='utf8') as file:
        user_list = file.readlines()
        file.close()

    with open(data_file, 'w', encoding='utf8') as file:  
        file.truncate(0)

        user_list.remove(str(user_id))

        file.writelines(user_list)
        file.close()
