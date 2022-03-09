def get_token_group():
    with open('group token', 'r') as file:
        token = file.read()
        return token


def get_user_token():
    with open('user token', 'r') as file:
        token = file.read()
        return token

