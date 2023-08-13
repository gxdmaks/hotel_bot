import database
import buttons
import telebot
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot('5834035718:AAG5WAAAfonu8ncFJG6wX2EosiKpqyVYuzw')

users = {'room_count': {}, 'room_name': {}}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    print(user_id)
    checker = database.check_user(user_id)
    if checker:
        rooms = database.get_room_name_id()
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(rooms))
    elif not checker:
        bot.send_message(user_id, 'Привет\nОтправь имя')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'отправь свой номер', reply_markup=buttons.phone_number_kb())
    bot.register_next_step_handler(message, get_number, name)


def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        database.register_user(user_id, name, phone_number)
        rooms = database.get_room_name_id()
        bot.send_message(user_id, 'Привет', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'выберите пункт меню', reply_markup=buttons.main_menu(rooms))
    elif not message.contact:
        bot.send_message(user_id, 'отправьте свой номер используя кнопку!', reply_markup=buttons.phone_number_kb())
        bot.register_next_step_handler(message, get_number, name)


@bot.callback_query_handler(lambda call: call.data in ['simple_room', 'lux_room', 'vip_room', 'back'])
def choose_room(call):
    user_id = call.message.chat.id
    room = database.get_exact_room(user_id)
    if call.data == 'simple_room':
        bot.send_message(user_id, 'Описание:\nОбычный номер\n\nЦена:\n230$\n\nВыберите номер',
                         reply_markup=buttons.choose_room_num())

    elif call.data == 'lux_room':
        bot.send_message(user_id, 'Описание:\nЛюкс номер\n\nЦена:\n280$\n\nВыберите номер',
                         reply_markup=buttons.choose_room_num())

    elif call.data == 'vip_room':
        bot.send_message(user_id, 'Описание:\nВип номер\n\nЦена:\n300$\n\nВыберите номер',
                         reply_markup=buttons.choose_room_num())
    elif call.data == 'back':
        rooms = database.get_room_name_id()
        bot.edit_message_text('Выберете пункт меню',
                              user_id
                              , call.message.message_id,
                              reply_markup=buttons.main_menu(rooms))
    users['room_count'][user_id] = 1
    users['room_name'][user_id] = call.data


@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'will_settle', 'back'])
def get_user_room_number(call):
    user_id = call.message.chat.id
    if call.data == 'increment':

        actual_count = users['room_count'][user_id]
        users['room_count'][user_id] += 1
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_room_num('increment', actual_count))
        print(users)
    elif call.data == 'decrement':
        actual_count = users['room_count'][user_id]
        users['room_count'][user_id] -= 1
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_room_num('decrement', actual_count))
    elif call.data == 'back':
        rooms = database.get_room_name_id()
        bot.edit_message_text('Выберете пункт меню',
                              user_id
                              , call.message.message_id,
                              reply_markup=buttons.main_menu(rooms))

    elif call.data == 'will_settle':
        quantity = users['room_count'][user_id]
        user_room = users['room_name'][user_id]
        print(quantity, user_room)
        database.add_room(user_id, user_room, quantity)
        bot.send_message(user_id, f"Комната {user_room} снята")
        start(call)
        bot.send_message(-912319996, 'Новый заказ на комнату')

@bot.callback_query_handler(lambda call: call.data in ['order', 'move_out'])
def main_menu_handle(call):
    user_id = call.message.chat.id
    user_room = database.get_exact_room(user_id)
    message_id = call.message.message_id
    if call.data == 'order':
        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, 'Выберите номер', reply_markup=buttons.choose_room())
    elif call.data == 'move_out':
        user_id = call.message.chat.id
        database.delete_users_from_all_room(user_id)
        bot.edit_message_text('Вы выселились с номера',
                              chat_id=user_id,
                              message_id=message_id,
                              reply_markup=buttons.main_menu(database.get_room_name_id()))


def get_location(message):
    user_id = message.from_user.id
    if message.location:
        user_cart = database.get_exact_room(user_id)
        full_text = 'Ваш заказ:\n\n'
        user_info = database.get_user_number_name(user_id)
        full_text += f'Имя: {user_info[0]}\nНомер телефона: {user_info[1]}\n\n'
        total_amount = 0
        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        full_text += f'\nИтог: {total_amount}\n'
        bot.send_message(user_id, full_text, reply_markup=buttons.get_accept_kb())






bot.polling(non_stop=True)
