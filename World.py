import arcade
from time import time
from random import randint,choice
from model import Player,Enemy,Shield
from map import Map
from dialog import Dialog
from physic import Physic
from menu import Menu

SCALE = 1
SPRITE_SPEED = 2
JUMP_SPEED = 10
JUMP_HEIGHT = 60
#SPAWN POINT
point_y = 75
point_x = 50


class World:
    def __init__(self,x,y):
        self.width = x
        self.height = y

        # arcade.set_background_color(arcade.color.BLACK)
        self.player = None
        self.enemy_type = arcade.SpriteList()
        # Just collect some bool to make the fucntion work
        self.time_check = 0
        # Page changer
        self.page_number = 0
        # For Character pic
        self.motion = 0
        self.pic = [arcade.load_texture('pics/menu/menu1.png'), arcade.load_texture('pics/menu/menu2.png',),
                    arcade.load_texture('pics/menu/menu3.png')]
        # For menu pic
        for each_pic in self.pic:
            each_pic.center_x = self.width // 2
            each_pic.center_y = self.height // 2

        self.bonus = arcade.Sprite('pics/game_over/game.png', scale=0.6)
        self.bonus.set_position(self.width // 2, self.height // 2)

        # Game level
        self.map = None

        self.level = 1
        #Physic engine
        self.physic = None

        # Dialog
        self.dialog = Dialog(SCALE / 1.5, self.width - 50, (self.height // 5) - 10)
        #Kinda confuse cause I mean it first a fault for set up.
        self.dialog_status = False
        self.skip_t = False

        #Menu
        self.menu = Menu(self.width,self.height)

        # Hurt
        self.hurt_status = False
        self.hurt_time = time()


        #ZA WADORU
        self.time_stop = False
        self.check_stop = False


        #Shield
        self.shield = Shield('pics/attack/slash.png',0.1,0,0)

    def setup_menu(self):
        self.menu = Menu(self.width,self.height)



    def setup(self):

        #For shop

        # For Player
        self.player = Player("pics/character/pixel.png",'pics/character/pixel2.png', SCALE, point_x, point_y,
                             'pics/attack/fire.png',self.menu.attack_delay,self.menu.health)

        # For Enemy
        self.enemy_type = arcade.SpriteList()

        enemy_num = self.num_enemy(self.level)

        for monster in range(enemy_num):
            slime = Enemy('pics/enemy/enemy.png','pics/enemy/enemy2.png', SCALE, randint(self.width // 2, self.width - 50), point_y)
            self.enemy_type.append(slime)

        # For map
        self.map = Map(self.width, self.height, self.level,self.enemy_type)
        self.map.reset(self.player)
        self.wall = self.map.wall_list

        # For Time
        self.time_check = -2
        self.player.life_time = time()
        self.hurt_time = time()

        #time stop
        self.time_stop = False
        self.check_stop = False

        # Status
        self.hurt_status = False

        # For physic
        self.physic = Physic()
        self.physic.add_physic(self.player,self.enemy_type,self.wall)

    @staticmethod
    def num_enemy(num):
        new_num = (num % 10)
        if new_num == 0:
            new_num = 10
        return new_num

    def on_draw(self):
        arcade.start_render()
        if self.page_number == 0:
            arcade.draw_circle_filled(50, 50, 500, arcade.color.WHITE)
            arcade.set_background_color(arcade.color.GRAY)
            if time() - self.time_check >= 1:
                self.motion = randint(0, 2)
                self.time_check = time()
            arcade.draw_texture_rectangle(self.pic[self.motion].center_x,self.pic[self.motion].center_y,
                                          texture=self.pic[self.motion],height=600,width=800)
            arcade.draw_text('Press ENTER to start the game', 0, 100, arcade.color.AMETHYST, width=self.width,
                                 font_size=35)

        elif self.page_number == -1:
            self.menu.draw(self.dialog_status)

        elif self.page_number == 1:
            self.player.draw()
            self.enemy_type.draw()
            self.player.attack(self.time_check)
            self.map.map_component()
            arcade.draw_text(f'The current level is {self.level}', self.width - 200, self.height - 100,
                                 arcade.color.WHITE)
            arcade.draw_text(f'Current life {self.player.life}', 100, self.height - 100,arcade.color.WHITE)
            self.shield.draw()
            if self.hurt_status:
                arcade.draw_rectangle_outline(self.width//2,self.height//2,self.width,self.height,arcade.color.RED,10)
                if time() - self.hurt_time >= 1.5:
                    self.hurt_status = False

        elif self.page_number == 3:
            self.bonus.draw()

        self.dialog.on_draw(self.dialog_status)

    #UPDATE_ZONE

    def update(self, delta_time: float):

        # Pretty long code
        if self.page_number == 1:
            # Dialog that will appear in the game
            check = self.dialog.time_check(self.level)
            if check is True:
                self.dialog_status = check

            if not self.dialog_status:
                self.player.update()
                self.jumping()
                self.shield.check_side(self.player.center_x,self.player.center_y)
                self.deflect()
                self.physic.update()
                if not self.time_stop:
                    self.enemy_type.update()
                self.check_boarder(self.enemy_type)
                self.check_die()



    @staticmethod
    def check_boarder(wat_want):
        for i in wat_want:
            i.boarder()

    def deflect(self):
        defect_list = arcade.check_for_collision_with_list(self.shield,self.enemy_type)
        for i in defect_list:
            i.center_x += self.shield.width//2
            i.change_x = -i.change_x
            i.change_y = -i.change_y


    def check_die(self):
        kill_list = None
        if self.player.attack_status:
            kill_list = arcade.check_for_collision_with_list(self.player.at_pic, self.enemy_type)
        if kill_list:
            for enemy in kill_list:
                enemy.kill()
                self.time_stop = False
                self.check_stop = True
            if len(self.enemy_type) == 0:
                self.level += 1
                if self.level % 10 == 0:
                    self.page_number = -1
                    self.menu.finish_shop = False
                    return
                else:
                    self.setup()
            self.physic.add_physic(self.player, self.enemy_type, self.wall)
        status = arcade.check_for_collision_with_list(self.player, self.enemy_type)

        if status:
            if time() - self.player.life_time >= 2:
                self.player.life -= 1
                self.menu.health -= 1
                self.hurt_status = True
                self.hurt_time = time()
                self.player.life_time = time()

        if self.player.life == 0:
            self.page_number = choice([0, 3])
            # self.page_number = 3
            if self.page_number == 3:
                self.dialog_status = self.dialog.b_page(self.page_number)
            self.level = 1
            self.skip_t = True
            self.setup_menu()
            self.setup()

    def jumping(self):
        for each in range(len(self.physic.physic_enemy)):
            if self.physic.physic_enemy[each].can_jump():
                self.enemy_type[each].change_y = randint(5,10)

    #END OF UPDATE ZONE

    def on_key_press(self, symbol: int, modifiers: int):
        if self.dialog_status:
                self.dialog.on_key_press(symbol,modifiers)
                self.dialog_status = self.dialog.check()
                if not self.dialog_status and self.page_number != -1:
                    self.page_number = 1

        elif self.page_number == -1:
            self.menu.on_key_press(symbol)
            if self.menu.finish_shop:
                self.page_number = 1
                self.setup()

        elif self.page_number == 0:
            if symbol == arcade.key.ENTER:
                if not self.skip_t:
                    self.dialog_status = True
                    self.skip_t = True
                self.page_number = -1
                self.setup_menu()
                arcade.set_background_color(arcade.color.BLACK)

        elif self.page_number == 1:
            if symbol == arcade.key.X:
                if time() - self.time_check >= 1:
                    self.player.attack_status = True
                    self.time_check = time()

            if symbol == arcade.key.UP:
                if self.physic.physic_player.can_jump():
                    self.player.change_y = JUMP_SPEED

            if symbol == arcade.key.Z:
                if not self.check_stop:
                    self.time_stop = True

            if symbol == arcade.key.LEFT:
                self.player.change_x = -SPRITE_SPEED

            elif symbol == arcade.key.RIGHT:
                self.player.change_x = SPRITE_SPEED

        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

    def on_mouse_motion(self,x,y):
        if not self.dialog_status:
            self.shield.center_x = x
            self.shield.center_y = y

    def on_key_release(self, key, modifiers):
        # if key == arcade.key.UP:
        #     self.player.change_y = 0
        if self.page_number == 1:
            if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player.change_x = 0
