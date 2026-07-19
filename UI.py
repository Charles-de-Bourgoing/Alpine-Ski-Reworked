from ursina import *
from direct.stdpy import thread
from player import Player
from monde import Level

class MenuManager:
    def __init__(self):
        self.play_button = Button('Play', on_click=self.show_loading_screen)
        self.loading_screen = None

    def show_loading_screen(self):
        destroy(self.play_button)
        self.loading_screen = Entity(model='quad', texture='loading_image')
        # Chargement en arrière-plan
        thread.start_new_thread(function=self.load_level, args=())

    def load_level(self):
        # Instanciation des modules externes
        level = Level()
        player = Player()
        
        destroy(self.loading_screen)