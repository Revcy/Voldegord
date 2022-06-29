import telebot as tg

from func.notice_module import *

with open('bot_info/token.txt', encoding='utf8') as file:
    token = file.readline()
    bot = tg.TeleBot(token)
    file.close()

@bot.message_handler(commands=['start'], chat_types=['private'])
def start_function(message):
    bot.send_message(message.chat.id, 'Bot for re-sending messages - Voldegord')

@bot.message_handler(commands=['notice'], chat_types=['private'])
def notice_function(message):
    keys = tg.types.InlineKeyboardMarkup(row_width=2)
    button1 = tg.types.InlineKeyboardButton(text='Follow', callback_data='notice_allow')
    button2 = tg.types.InlineKeyboardButton(text='Unfollow', callback_data='notice_reject')
    keys.add(button1, button2)

    user_id = message.from_user.id
    notice_status = notice_check_status(user_id)
    
    if notice_status == True:
        notice_status_result = "Active"
    else:
        notice_status_result = "Inactive"

    bot.send_message(message.chat.id, f'Notice follow status: {notice_status_result}\nChoose action', reply_markup=keys)

@bot.callback_query_handler(func=lambda callback: callback.data)
def notice_manage_function(callback):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    chat_id = callback.message.chat.id

    if callback.data == 'notice_allow':
        user_check = notice_check_status(user_id)
        if user_check == True:
            # bot.send_message(chat_id, 'You was been followed to notifications')
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='You was been followed to notifications')
            pass
        else:
            notice_user_add(user_id)
            # bot.send_message(chat_id, 'You have been successfully followed to notifications')
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='You have been successfully followed to notifications')
    elif callback.data == 'notice_reject':
        user_check = notice_check_status(user_id)
        if user_check == False:
            # bot.send_message(chat_id, "You don't been followed to notifications")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="You don't been followed to notifications")
            pass
        else:
            notice_user_delete(user_id)
            # bot.send_message(chat_id, 'You have been successfully unfollowed to notifications')
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='You have been successfully unfollowed to notifications')

@bot.message_handler(commands=['publish'], chat_types=['private'])
def publish_function(message):
    publish_register = bot.send_message(message.chat.id, 'Type message for notifications')
    bot.register_next_step_handler(publish_register, notice_publish_function)

def notice_publish_function(message):
    with open('bot_info/userlist_notice.txt') as file:
        user_list = file.readlines()
        file.close()

    for user_id in user_list:
        bot.send_message(int(user_id), message.text)
    
    bot.send_message(message.chat.id, 'Publish done!')

bot.infinity_polling()
