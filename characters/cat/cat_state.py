from characters.cat.cat_sprite import CatFighter


class CatState:
    def __init__(self, cat: CatFighter):
        self.cat = cat

    def handle_input(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def on_enter(self, *args, **kwargs):
        pass

    def on_exit(self, *args, **kwargs):
        pass
