import arcade
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPRITE_SIZE = 0.2

class Map:
    def __init__(self, width, height, level,enemy):
        self.base = width//4
        self.start_x = randint(100,SCREEN_WIDTH//2)
        self.end_x = randint(SCREEN_WIDTH//4,SCREEN_WIDTH-100)
        self.start_y = randint(100,SCREEN_HEIGHT//4)
        self.end_y = randint(SCREEN_HEIGHT//2,SCREEN_HEIGHT-50)
        self.enemy = enemy
        self.wall_list = None
        # self.physic = None
        # self.physic_enemy = []

    def reset(self,player):
        self.wall_list = arcade.SpriteList()
        self.physic_enemy = []
        choice = randint(0,1)
        for x in range(0,SCREEN_WIDTH+40,40):
            wall = arcade.Sprite('pics/obsticle.png', SPRITE_SIZE)
            wall.center_x = x
            wall.center_y = 25
            self.wall_list.append(wall)
        # if choice == 0:
        self.map1()
        # elif choice == 1:
        #     self.map1()
        #     self.map2()



    def map1(self):

        for num in range(2,5,2):
            for x in range(self.start_x,self.end_x,randint(40,200)):
                wall = arcade.Sprite('pics/obsticle.png', SPRITE_SIZE)
                wall.center_x = x
                wall.center_y = SCREEN_HEIGHT//num
                self.wall_list.append(wall)

    def map2(self):

        for num in range(2,5,1):
            for y in range(self.start_y,self.end_y,randint(40,200)):
                wall = arcade.Sprite('pics/obsticle.png', SPRITE_SIZE)
                wall.center_x = num*150
                wall.center_y = y
                self.wall_list.append(wall)

    def map_component(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT//12, SCREEN_WIDTH, 2, arcade.color.GRAY)
        self.wall_list.draw()
