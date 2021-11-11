class Users:
    """ Собираем и храним пользователей по id чата
    как объект User """
    users = dict()

    def __init__(self, user_id):
        self.user_id = user_id
        Users.add_user(user_id)

    @classmethod
    def add_user(cls, user_id):
        user = User()
        cls.users[user_id] = user

    @classmethod
    def get_user(cls, user_id):
        if user_id not in cls.users:
            Users(user_id)
        return cls.users[user_id]


class User:
    def __init__(self):
        self.command = []
        self.time = []
        self.city_id = None
        self.sum_hotels = None
        self.sum_photo = None
        self.price_list = None
        self.dist_list = None
        self.my_hotels_list = []
