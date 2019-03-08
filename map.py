import arcade
from random import randint

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SPRITE_SIZE = 0.2

class Map:
    def __init__(self, width, height, level,enemy):
        self.base = width//4
        self.start_x = randint(100,SCREEN_WIDTH//2)
        self.end_x = randint(SCREEN_WIDTH//2,SCREEN_WIDTH-100)
        self.enemy = enemy
        self.wall_list = None
        # self.physic = None
        # self.physic_enemy = []

    def reset(self,player):
        self.wall_list = arcade.SpriteList()
        self.physic_enemy = []
        for x in range(0,SCREEN_WIDTH+40,40):
            wall = arcade.Sprite('pics/obsticle.png', SPRITE_SIZE)
            wall.center_x = x
            wall.center_y = 25
            self.wall_list.append(wall)

        for num in range(2,5,2):
            for x in range(self.start_x,self.end_x,randint(40,200)):
                wall = arcade.Sprite('pics/obsticle.png', SPRITE_SIZE)
                wall.center_x = x
                wall.center_y = SCREEN_HEIGHT//num
                self.wall_list.append(wall)

        # self.physic = arcade.PhysicsEnginePlatformer(player,self.wall_list,gravity_constant=GRAVITY)
        # for each in self.enemy:
        #     enemy = arcade.PhysicsEnginePlatformer(each, self.wall_list)
        #     enemy.can_jump()
            # self.physic_enemy.append(arcade.PhysicsEnginePlatformer(each, self.wall_list))
            # self.physic_enemy.append(enemy)

    # def update(self):
    #     self.physic.update()
    #     for each in self.physic_enemy:
    #         each.update()


    def map_component(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT//12, SCREEN_WIDTH, 2, arcade.color.GRAY)
        self.wall_list.draw()

