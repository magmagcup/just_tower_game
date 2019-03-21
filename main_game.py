import arcade
from time import time
from random import randint
from World import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'TOWER_GAME'
SCALE = 1
SPRITE_SPEED = 2
JUMP_SPEED = 10
JUMP_HEIGHT = 60
#SPAWN POINT
point_y = 75
point_x = 50

class GameMU(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title,resizable=True)
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

def main():
    window = GameMU(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

main()