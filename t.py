class Transfer:
    def __init__(self, tiles, things, cat):
        self.tiles = tiles
        self.things = things
        self.cat = cat

    def get_thingsgroup(self):
        return self.things

    def get_tilesgroup(self):
        return self.tiles

    def get_catgroup(self):
        return self.cat
