import vars


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
    real_name = "Test User"
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
    index = check_user_order(identifier)

    if index >= 0:
        vars.order_que.pop(index)
        return True
    else:
        return False


def check_user_already_placed_order(identifier, type):
    index = check_user_order(identifier)
    if index >= 0:
        return vars.order_que[index]
    else:
        return None


def get_orders():
    return vars.order_que
