from time import time
from random import randint
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
JUMP_HEIGHT = 60

DELETE_HEIGHT = 25

class Model(arcade.Sprite):
    def __init__(self, filename, filename2,scale, pointx, pointy):
        super().__init__()
        #PIC
        self.textures.append(arcade.load_texture(filename, mirrored=True, scale=scale))
        self.textures.append(arcade.load_texture(filename2, mirrored=True, scale=scale))
        self.textures.append(arcade.load_texture(filename, scale=scale))
        self.textures.append(arcade.load_texture(filename2, scale=scale))

        self.direction = {'RIGHT':2,'RIGHT_move':3,'LEFT':0,'LEFT_move':1}

        # self.RIGHT = 2
        # self.RIGHT_move = 3
        # self.LEFT = 0
        # self.LEFT_move = 1

        self.center_x = pointx
        self.center_y = pointy

        #time
        self.jump_timer = time()
        self.skin_changer = time()



class Enemy(Model):
    def __init__(self, filename,filename2, scale, pointx,pointy):
        super().__init__(filename,filename2,scale,pointx,pointy)
        # For checking
        self.facing_status = self.direction['LEFT']
        self.set_texture(self.direction['LEFT'])

        self.change_x = -randint(1,3)
        self.can_deflect = True
        self.can_kill = True

    def boarder(self):

        if self.change_x < 0:
            self.set_texture(self.direction['LEFT'])
            self.facing_status = self.direction['LEFT']

        elif self.change_x > 0:
            self.set_texture(self.direction['RIGHT'])
            self.facing_status = self.direction['RIGHT']

        if self.left < 0:
            self.change_x = 2
        elif self.right > SCREEN_WIDTH - 1:
            self.change_x = -2

        if self.change_y == 0:
            if self.facing_status == self.direction['RIGHT']:
                self.set_texture(self.direction['RIGHT_move'])
            else:
                self.set_texture(self.direction['LEFT_move'])
        #Constant
        if self.center_y <= 35:
            self.center_y = 60


    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y


class BlueSlime(Enemy):
    def __init__(self, filename, filename2, scale, pointx, pointy):
        super().__init__(filename, filename2, scale, pointx, pointy)
        self.can_deflect = False
        self.can_kill = False


class Player(Model):

    def __init__(self, filename,filename2, scale,pointx,pointy,attack,attack_delay_speed,life):
        super().__init__(filename,filename2,scale,pointx,pointy)
        # For checking
        self.facing_status = self.direction['RIGHT']
        self.set_texture(self.direction['RIGHT'])
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
        #life
        self.life = life
        #Movement
        self.still = time()
        self.motion_status = self.direction['RIGHT']

    def attack(self,time_check):
        if self.attack_status:
            #For 1.3.7
            #self.at_pic.scale += 0.1
            self.at_pic.scale += 0.01
            #CONSTANT
            self.at_pic.explosion(self.center_x,self.center_y,self.facing_status)
            self.at_pic.draw()

        if time() - time_check >= self.attack_delay:
            self.attack_status = False
            self.at_pic.scale = self.scale/9

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if time() - self.still >= 0.5:
            motion = None
            if self.motion_status == self.direction['LEFT']:
                self.set_texture(self.direction['LEFT_move'])
                motion = self.direction['LEFT_move']
            elif self.motion_status == self.direction['LEFT_move']:
                self.set_texture(self.direction['LEFT'])
                motion = self.direction['LEFT']
            elif self.motion_status == self.direction['RIGHT']:
                self.set_texture(self.direction['RIGHT_move'])
                motion = self.direction['RIGHT_move']
            elif self.motion_status == self.direction['RIGHT_move']:
                self.set_texture(self.direction['RIGHT'])
                motion = self.direction['RIGHT']

            self.motion_status = motion
            self.still = time()

        if self.change_x < 0:
            self.set_texture(self.direction['LEFT_move'])
            self.facing_status = self.direction['LEFT']
            self.motion_status = self.direction['LEFT_move']

        elif self.change_x > 0:
            self.set_texture(self.direction['RIGHT_move'])
            self.facing_status = self.direction['RIGHT']
            self.motion_status = self.direction['RIGHT_move']

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

