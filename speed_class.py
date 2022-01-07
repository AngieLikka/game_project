class Speed():
    def __init__(self, v):
        self.v = v

    def change_v(self):
        self.v += 0.1

    def get_v(self):
        return self.v