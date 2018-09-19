from Orders import vars
from SlackBot import slack_functions


def check_room_order(room):
    i = len(vars.order_que)
    while i > 0:
        if vars.order_que[i - 1]['room'] == room:
            return i - 1
        i = i - 1
    return -1


def check_user_order(user, ident2=None):
    i = len(vars.order_que)
    while i > 0:
        if vars.order_que[i - 1]['user'] == user or vars.order_que[i - 1]['user'] == ident2:
            return i - 1
        i = i - 1
    return -1


def add_order(user, room, type, priority=False):
    result = check_user_already_placed_order(user, type)
    real_name = slack_functions.get_real_name(user, type)
    if result is None:
        if priority:
            vars.order_que.insert(0, {'room': room, 'user': user, 'real_name': real_name, 'type': type})
            position = 0
        else:
            result = check_room_order(room)
            if result >= 0:
                vars.order_que.insert(result + 1, {'room': room, 'user': user, 'real_name': real_name, 'type': type})
                position = result + 1
            else:
                vars.order_que.append({'room': room, 'user': user, 'real_name': real_name, 'type': type})
                position = len(vars.order_que) - 1

        return True, position
    else:
        return False, result


def delete_oder(identifier, type):
    if type == 'email':
        email = identifier
        id = slack_functions.get_id_by_email(email)
    else:
        id = identifier
        email = slack_functions.get_email_by_id(id)

    index = check_user_order(id, email)
    if index >= 0:
        vars.order_que.pop(index)
        return True
    else:
        return False


def check_user_already_placed_order(identifier, type):
    if type == 'email':
        email = identifier
        id = slack_functions.get_id_by_email(email)
    else:
        id = identifier
        email = slack_functions.get_email_by_id(id)

    index = check_user_order(id, email)
    if index >= 0:
        return vars.order_que[index]
    else:
        return None


def get_orders():
    return vars.order_que


def get_current_destination():
    if len(vars.order_que) > 0:
        return vars.order_que[0]['room']
    else:
        return "No Destination"
