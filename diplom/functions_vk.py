import random


def dump_it(session_maker, new_user, photo):
    res = False
    if session_maker:
        session = session_maker()
        session.add(new_user)
        for p in photo:
            session.add(p)
            session.commit()
            res = True
    return res


def make_search(vki, user, message):
    sex = make_sex(user['sex'])
    birth_year = make_birth_year(user, message)
    city = 1

    search_params = {'sort': 0,
                     'is_closed': False,
                     'has_photo': 1,
                     'sex': sex,
                     'birth_year': birth_year,
                     'city': city,
                     'status': 1}

    res = vki.search(search_params)

    return res


def check_user(user):
    if user['is_closed']:
        return False
    param_list = ['id', 'first_name', 'last_name', 'sex', 'bdate', 'city']
    for field in param_list:
        if field not in user.keys():
            return False
    return True


def best_size(sizes_list):
    type_ = ['s', 'm', 'x', 'o', 'p', 'q', 'r', 'y', 'z', 'w']
    size_ = range(1, len(type_) + 1)
    sizes_rating = dict(zip(type_, size_))
    top_size = sorted(sizes_list, key=(lambda item: sizes_rating[item['type']]), reverse=True)[0]
    return top_size


def get_best_prof_photos(vki, id_):
    req = vki.get_photos(id_)
    top_3_links = None
    if 'items' in req.keys():
        res = vki.get_photos(id_)['items']
        res.sort(key=lambda item: item['likes']['count'], reverse=True)
        top_3 = res[0: min(3, len(res))]
        top_3_links = [best_size(item['sizes'])['url'] for item in top_3]

    return top_3_links


def make_sex(sex):
    if sex != 0:
        sex = 3 - sex
    return sex


def make_birth_year(user, message):
    if 'bdate' not in user.keys():
        birth_year = None
        while not (isinstance(birth_year, int) and 1900 < birth_year < 2021):
            birth_year = int(message.read('Какой год рождения?'))
    elif len(user['bdate'].split('.')) != 3:
        birth_year = None
        while not (isinstance(birth_year, int) and 1900 < birth_year < 2021):
            birth_year = int(message.read('Какой год рождения?'))
    else:
        birth_year = user['bdate'].split('.')[-1]

    return int(birth_year) + random.randrange(-5, 5)
