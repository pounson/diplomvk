import sqlalchemy
from functions_vk import *
from vk_db import User, Photo, create_db
from vk_classes import Vkinder, Message
from settings import get_token_group, get_user_token, DSN


def search_result(id_, vki):
    raw_user = vki.get_user_info(id_)[0]
    if check_user(raw_user):
        new_user = User(user_id=raw_user['id'],
                        first_name=raw_user['first_name'],
                        last_name=raw_user['last_name'],
                        sex=raw_user['sex'],
                        bdate=raw_user['bdate'],
                        city=raw_user['city']['title'])

        photo = [Photo(user_id=new_user.user_id, url=one_url) for one_url in
                 get_best_prof_photos(vki, new_user.user_id)]

        return {'user': new_user, 'photo': photo}
    else:
        return False


def start_vkinder(vki, session_maker):
    x = vki.read_msg()
    new_client = x.user_id
    message = Message(vki, new_client)

    resp = vki.get_user_info(new_client)

    user = resp[0]
    message.write(f"{user['first_name']} {user['last_name']}, сейчас найдем для тебя пару")
    res = make_search(vki, user, message)
    dump_list = []
    for r in res:
        if session_maker:
            already_in_db = session_maker().query(User).filter(User.user_id == r['id']).first()
        else:
            already_in_db = False

        if not already_in_db:
            new_id = search_result(r['id'], vki)
            if not new_id:
                continue
            else:
                message.write(f"как тебе {new_id['user']}")
                [message.write(item) for item in new_id['photo']]

                dump_it(session_maker, new_id['user'], new_id['photo'])

                message.write(f"Нажми 'q' чтобы выйти или найди еще пару")
                q = message.read()
                if q == 'q':
                    message.write(f"Заходи еще")
                    break


if __name__ == '__main__':
    try:
        Session = create_db(DSN)
    except sqlalchemy.exc.OperationalError as error_msg:
        print(error_msg)
        Session = False

    vkinder = Vkinder(token=get_user_token(), group_token=get_token_group())
    start_vkinder(vkinder, Session)
