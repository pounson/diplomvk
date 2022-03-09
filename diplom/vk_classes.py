from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class Vkinder:
    def __init__(self, token=None, group_token=None):
        self.token = token
        self.group_token = group_token
        self.vk_session = vk_api.VkApi(token=self.token).get_api()
        self.group_session = vk_api.VkApi(token=self.group_token)
        self.longpoll = VkLongPoll(vk_api.VkApi(token=self.group_token))

    def get_user_info(self, id_=None):
        vk_user = self.vk_session.users.get(user_ids=id_, fields='sex, bdate, city, relation')
        return vk_user

    def get_photos(self, id_):
        photo = self.vk_session.photos.get(owner_id=id_, album_id='profile', extended=1)
        return photo

    def search(self, params):
        tool = vk_api.tools.VkTools(self.vk_session)
        res = tool.get_all_iter('users.search', 1000, values=params)
        return res

    def send_msg(self, user_id, message):
        self.group_session.method('messages.send',
                                  {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    def read_msg(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    return event


class Message:
    def __init__(self, k, id_):
        self.k = k
        self.id_ = id_

    def write(self, message):
        self.k.send_msg(self.id_, message)

    def read(self):
        text = False
        while not text:
            event = self.k.read_msg()
            if event.user_id == self.id_:
                text = event.text
        return text
