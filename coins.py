class Coins:  # класс монет
    def __init__(self):
        self.coins = 0

    def add_coin(self):
        self.coins += 1

    def get_coins(self):
        return self.coins

    def set_coins(self):
        self.coins = 0
