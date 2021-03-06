import arcade
from time import time
from random import randint,choice
from model import Player,Enemy,Shield,BlueSlime,YellowSlime,RedSlime
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
    def __init__(self,width,height):
        self.width = width
        self.height = height

        # arcade.set_background_color(arcade.color.BLACK)
        self.player = None
        self.enemy_type = arcade.SpriteList()
        # Just collect some bool to make the fucntion work
        self.time_check = 0
        # Page changer
        self.page_number = 0
        # For Character pic
        self.motion = 0

        #background
        self.bg = arcade.load_texture('pics/bg.png')
        self.set_center(self.bg)
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
        # Hurt
        self.hurt_status = False
        self.hurt_time = time()
        #Money
        self.MONEY = 50
        #ZA WADORU
        self.hard_mode = False
        #Shield
        self.shield = Shield('pics/attack/slash.png',0.1,0,0)

    def set_center(self,file):
        file.center_x = self.width // 2
        file.center_y = self.height // 2

    def setup_menu(self):
        self.menu = Menu(self.width,self.height,self.MONEY)

    def setup(self):

        # For Player
        self.player = Player("pics/character/pixel.png",'pics/character/pixel2.png', SCALE, point_x, point_y,
                             'pics/attack/fire.png',self.menu.attack_delay,self.menu.health)

        # For Enemy
        self.enemy_type = arcade.SpriteList()

        enemy_num = self.num_enemy(self.level)

        for monster in range(enemy_num):

            enemy = randint(1,30)

            if enemy > 25:
                slime = RedSlime('pics/enemy/enemyr1.png','pics/enemy/enemyr2.png', SCALE, randint(self.width // 2, self.width - 50), point_y)
            elif enemy >= 19:
                slime = YellowSlime('pics/enemy/enemyy1.png','pics/enemy/enemyy2.png', SCALE, randint(self.width // 2, self.width - 50), point_y)
            elif enemy > 10:
                slime = BlueSlime('pics/enemy/enemyb1.png','pics/enemy/enemyb2.png', SCALE, randint(self.width // 2, self.width - 50), point_y)
            elif enemy >= 1:
                slime = Enemy('pics/enemy/enemy.png', 'pics/enemy/enemy2.png', SCALE,
                          randint(self.width // 2, self.width - 50), point_y)

            self.enemy_type.append(slime)

        # For map
        self.map = Map(self.width, self.height, self.level,self.enemy_type)
        self.map.reset(self.player)
        self.wall = self.map.wall_list

        # For Invicible peraid
        self.time_check = 0
        self.player.life_time = time()
        self.hurt_time = time()

        # Status
        self.hurt_status = False

        # For physic
        self.physic = Physic()
        self.physic.add_physic(self.player,self.enemy_type,self.wall)

        #For shop
        self.menu.player_money = self.MONEY

        #Mode
        self.hard_mode = self.menu.mode

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
            pic = [arcade.load_texture('pics/menu/menu1.png'), arcade.load_texture('pics/menu/menu2.png', ),
                        arcade.load_texture('pics/menu/menu3.png')]
            # For menu pic
            for each_pic in pic:
                self.set_center(each_pic)
            arcade.draw_texture_rectangle(pic[self.motion].center_x,pic[self.motion].center_y,
                                          texture=pic[self.motion],height=700,width=900)
            #For 1.3.7
            #arcade.draw_text('Press ENTER to start the game', 0, 100, arcade.color.AMETHYST, width=self.width,
            #                    font_size=35)
            arcade.draw_text('Press ENTER to start the game', 0, 100, arcade.color.AMETHYST, font_size=35)
            arcade.draw_text('Just An Ordinary Dungeon Crawler game', 0, 200, arcade.color.GOLD_FUSION, font_size=50, width=3500)

        elif self.page_number == -1:
            self.menu.draw()

        elif self.page_number == 1:
            arcade.draw_texture_rectangle(self.bg.center_x,self.bg.center_y,
                                          texture=self.bg,height=600,width=800)
            self.player.draw()
            self.enemy_type.draw()
            self.player.attack(self.time_check)
            self.map.map_component()
            arcade.draw_text(f'The current level is {self.level}', self.width - 200, self.height - 100,
                                 arcade.color.BLACK)
            arcade.draw_text(f'Current life {self.player.life}', 100, self.height - 100,arcade.color.BLACK)
            arcade.draw_text(f'Current Money {self.MONEY}', self.width//2 - 50,self.height -100,arcade.color.BLACK)
            self.shield.draw()
            if self.hurt_status:
                arcade.draw_rectangle_outline(self.width//2,self.height//2,self.width,self.height,arcade.color.RED,10)
                if time() - self.hurt_time >= 1.5:
                    self.hurt_status = False

        elif self.page_number == -3 or self.page_number == -2:
            tutorial = arcade.load_texture('pics/scene/t2.png')
            if self.page_number == -2:
                tutorial = arcade.load_texture('pics/scene/t1.png')
            self.set_center(tutorial)
            arcade.draw_texture_rectangle(tutorial.center_x,tutorial.center_y,
                                          texture=tutorial, height=600, width=800)


        elif self.page_number == 3:
            bonus = arcade.load_texture('pics/game_over/game.png')
            self.set_center(bonus)
            arcade.draw_texture_rectangle(bonus.center_x,bonus.center_y,
                                          texture=bonus, height=700, width=900)
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
                self.shield.check_side(self.player.center_x,self.player.center_y)
                self.physic.update()
                self.jumping()
                if self.hard_mode:
                     self.enemy_type.update()
                self.check_boarder(self.enemy_type)
                self.check_die()
                self.update_physic()
        elif self.page_number == -1:
            self.menu.update()

    @staticmethod
    def check_boarder(wat_want):
        for i in wat_want:
            i.boarder()

    def deflect(self):
        defect_list = arcade.check_for_collision_with_list(self.shield,self.enemy_type)
        for i in defect_list:
            if i.can_deflect:
                i.center_x += self.shield.width//2
                i.change_x = -i.change_x
                i.change_y = -i.change_y
            else:
                if i.can_teleport:
                    i.center_x = self.player.center_x
                    i.center_y = self.player.center_y
                else:
                    self.kill_enemy(i)


    def check_die(self):
        self.deflect()
        kill_list = None
        if self.player.attack_status:
            kill_list = arcade.check_for_collision_with_list(self.player.at_pic, self.enemy_type)
        if kill_list:
            for enemy in kill_list:
                if enemy.can_kill:
                    self.kill_enemy(enemy)
        if len(self.enemy_type) == 0:
            self.level += 1
            if self.level % 10 == 0:
                self.menu.player_money = self.MONEY
                self.page_number = -1
                self.menu.finish_shop = False
                return
            else:
                self.setup()
        self.check_die_player()

    def kill_enemy(self,enemy):
        self.MONEY += 10
        enemy.kill()

    def check_die_player(self):
        status = arcade.check_for_collision_with_list(self.player, self.enemy_type)

        if status:
            if time() - self.player.life_time >= 2:
                self.player.life -= 1
                self.menu.health -= 1
                self.hurt_status = True
                self.hurt_time = time()
                self.player.life_time = time()

        if self.player.life == 0:
            self.reset_game()

    def update_physic(self):
        # Important
        self.physic.add_physic(self.player, self.enemy_type, self.wall)

    def reset_game(self):
        self.page_number = choice([0, 3])
        self.MONEY = 50
        # self.page_number = 3
        if self.page_number == 3:
            self.dialog_status = self.dialog.b_page(self.page_number)
        self.level = 1
        self.skip_t = True
        self.setup_menu()
        self.setup()

    def jumping(self):
        for each in range(len(self.physic.physic_enemy)):
            if self.enemy_type[each].want_to_jump:
                if self.physic.physic_enemy[each].can_jump():
                    self.enemy_type[each].change_y = randint(5,10)
            else:
                if self.enemy_type[each].change_y == 0:
                    self.enemy_type[each].change_y = randint(1,2)
                if not randint(0,20):
                    self.enemy_type[each].change_y = -10
                self.enemy_type[each].update()

    #END OF UPDATE ZONE

    def reset_motion(self):
        self.player.still = time()

    def on_key_press(self, symbol: int, modifiers: int):
        if self.dialog_status:
            self.dialog.on_key_press(symbol,modifiers)
            self.dialog_status = self.dialog.check()
            if self.page_number == -3 and self.dialog.num_context == 4:
                self.page_number = -2
            if -3 <= self.page_number <= -2 and self.dialog.context == None:
                self.page_number = -1
            if not self.dialog_status and self.page_number == 3:
                self.page_number = 0


        elif self.page_number == -1:
            self.menu.on_key_press(symbol)
            if self.menu.finish_shop:
                self.MONEY = self.menu.player_money
                self.page_number = 1
                self.setup()

        elif self.page_number == 0:
            if symbol == arcade.key.T:
                self.skip_t = False
                self.dialog.tutorial()
            if symbol == arcade.key.ENTER:
                if not self.skip_t:
                    self.dialog_status = True
                    self.skip_t = True
                    self.page_number = -3
                else:
                    self.page_number = -1
                self.setup_menu()
                arcade.set_background_color(arcade.color.BLACK)

        elif self.page_number == 1:
            if symbol == arcade.key.X or symbol == arcade.key.NUM_0:
                if time() - self.time_check >= 1:
                    self.player.attack_status = True
                    self.time_check = time()

            if symbol == arcade.key.UP:
                if self.physic.physic_player.can_jump():
                    self.player.change_y = JUMP_SPEED
                    self.reset_motion()

            if symbol == arcade.key.LEFT:
                self.player.change_x = -SPRITE_SPEED
                self.reset_motion()

            elif symbol == arcade.key.RIGHT:
                self.player.change_x = SPRITE_SPEED
                self.reset_motion()

            if symbol == arcade.key.R:
                self.reset_game()

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
