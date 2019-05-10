import arcade
from time import time
from random import randint
from World import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Just An Ordinary Dungeon Clawer game'

class GameMU(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title,resizable=True)
        self.set_mouse_visible(False)
        # arcade.set_background_color(arcade.color.BLACK)
        self.world = World(width,height)

    def on_draw(self):
        self.world.on_draw()

    def update(self, delta_time: float):
        self.world.update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        self.world.on_key_press(symbol,modifiers)

    def on_key_release(self, key, modifiers):
        self.world.on_key_release(key,modifiers)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.world.on_mouse_motion(x,y)

def main():
    window = GameMU(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

main()