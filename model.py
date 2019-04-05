from time import time
from random import randint
import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
JUMP_HEIGHT = 60

DELETE_HEIGHT = 25

class Model(arcade.Sprite):
    def __init__(self, filename, filename2,scale, pointx, pointy):
        super().__init__()
        #PIC
        self.pic_left = arcade.load_texture(filename, mirrored=True, scale=scale)
        self.textures.append(self.pic_left)
        self.textures.append(arcade.load_texture(filename2, mirrored=True, scale=scale))
        self.pic_right = arcade.load_texture(filename, scale=scale)
        self.textures.append(self.pic_right)
        self.textures.append(arcade.load_texture(filename2, scale=scale))

        self.RIGHT = 2
        self.RIGHT_move = 3
        self.LEFT = 0
        self.LEFT_move = 1

        self.center_x = pointx
        self.center_y = pointy

        #time
        self.jump_timer = time()
        self.skin_changer = time()



class Enemy(Model):
    def __init__(self, filename,filename2, scale, pointx,pointy):
        super().__init__(filename,filename2,scale,pointx,pointy)
        # For checking
        self.facing_status = self.LEFT
        self.set_texture(self.LEFT)

        self.change_x = -randint(1,3)
        self.set_texture(self.LEFT)

    def boarder(self):

        if self.change_x < 0:
            self.set_texture(self.LEFT)
            self.facing_status = self.LEFT

        elif self.change_x > 0:
            self.set_texture(self.RIGHT)
            self.facing_status = self.RIGHT

        if self.left < 0:
            self.change_x = 2
        elif self.right > SCREEN_WIDTH - 1:
            self.change_x = -2

        if self.change_y == 0:
            if self.facing_status == self.RIGHT:
                self.set_texture(self.RIGHT_move)
            else:
                self.set_texture(self.LEFT_move)
        #Constant
        if self.center_y <= 35:
            self.center_y = 60


    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y



class Player(Model):
    MONEY = 50
    def __init__(self, filename,filename2, scale,pointx,pointy,attack,attack_delay_speed,life):
        super().__init__(filename,filename2,scale,pointx,pointy)
        # For checking
        self.facing_status = self.RIGHT
        self.set_texture(self.RIGHT)
        #status for move
        self.attack_status = False
        #Attack sprite
        self.at_pic = Attack(attack,scale/9,pointx,pointy)
        # Life
        # Invincible time
        self.life_time = time()
        #Attack_delay
        self.attack_delay = attack_delay_speed
        #Money
        self.money = Player.MONEY
        #life
        self.life = life


    def attack(self,time_check):
        if self.attack_status:
            #CONSTANT
            self.at_pic.explosion(self.center_x,self.center_y,self.facing_status)
            self.at_pic.draw()

        if time() - time_check >= self.attack_delay:
            self.attack_status = False

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x < 0:
            self.set_texture(self.LEFT_move)
            self.facing_status = self.LEFT

        elif self.change_x > 0:
            self.set_texture(self.RIGHT_move)
            self.facing_status = self.RIGHT

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1


class Attack(Model):
    def __init__(self,filename, scale, pointx, pointy):
        super().__init__(filename,filename, scale=scale, pointx= pointx, pointy=pointy)

    #Constant
    def explosion(self, x, y, faceing):
        if faceing == 0:
            self.center_x = x - 50
            self.center_y = y

        elif faceing == 2:
            self.center_x = x + 50
            self.center_y = y

        self.set_texture(faceing)


class Shield(Model):
    def __init__(self,filename, scale, pointx, pointy):
        super().__init__(filename,filename, scale=scale, pointx= pointx, pointy=pointy)

    def check_side(self,player_x,player_y):
        if self.center_x < player_x:
            self.set_texture(0)
        else:
            self.set_texture(2)

