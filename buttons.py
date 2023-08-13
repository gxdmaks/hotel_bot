from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_menu(room_from_db):
    kb = InlineKeyboardMarkup(row_width=3)
    order = InlineKeyboardButton(text='Снять комнату', callback_data='order')
    move_out = InlineKeyboardButton(text='Выселится', callback_data='move_out')
    rooms = [InlineKeyboardButton(text=i[0],callback_data=i[1])
                    for i in room_from_db]
    kb.row(order)
    kb.row(move_out)
    kb.add(*rooms)
    return kb

def choose_room():
    kb = InlineKeyboardMarkup(row_width=4)
    simple_room = InlineKeyboardButton(text='Обычный номер', callback_data='simple_room')
    lux_room = InlineKeyboardButton(text='Люкс номер', callback_data='lux_room')
    vip_room = InlineKeyboardButton(text='Вип номер', callback_data='vip_room')
    back = InlineKeyboardButton(text='Назад', callback_data='back')
    kb.row(simple_room)
    kb.row(lux_room)
    kb.row(vip_room)
    kb.row(back)
    return kb

def choose_room_num(plus_or_minus='',current_amount=1):
    kb = InlineKeyboardMarkup(row_width=3)
    back = InlineKeyboardButton(text='Назад',callback_data='back')
    plus = InlineKeyboardButton(text='+',callback_data='increment')
    minus = InlineKeyboardButton(text='-',callback_data='decrement')
    count = InlineKeyboardButton(text=str(current_amount),
                                 callback_data=str(current_amount))
    will_settle = InlineKeyboardButton(text='Заселится',callback_data='will_settle')

    if plus_or_minus == 'increment':
        new_amount = int(current_amount)+1
        count = InlineKeyboardButton(text=str(new_amount),
                                     callback_data=str(new_amount))

    elif plus_or_minus == 'decrement':
        if int(current_amount) > 1:
            new_amount = int(current_amount)-1
            count = InlineKeyboardButton(text=str(new_amount),
                                         callback_data=str(new_amount))

    kb.add(minus,count,plus)
    kb.row(will_settle)
    kb.row(back)
    return kb

def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    number = KeyboardButton('Поделится контактом', request_contact=True)
    kb.add(number)

    return kb

def get_accept_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Подтвердить')
    no = KeyboardButton('Отменить')
    kb.add(yes,no)

    return kb

def get_room_kb():
    kb = InlineKeyboardMarkup(row_width=1)

    clear_cart = InlineKeyboardButton('Выселится',callback_data='move_out')
    order = InlineKeyboardButton('Заселится',callback_data='order')
    back = InlineKeyboardButton('Назад',callback_data='back')

    kb.add(clear_cart,order,back)