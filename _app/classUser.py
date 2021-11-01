class User:
    def __init__(self):
        self.command = None
        self.city_id = None
        self.sum_hotels = None
        self.sum_photo = None
        self.price_list = None
        self.dist_list = None


class History:
    def __init__(self):
        self.command = []
        self.time = []
        self.hotels = []
