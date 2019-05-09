import arcade
from math import sin

Box_space = 300
Text_space_from_box = 325

class Menu:
    Price = {'HEART':50,'ATTACK_DELAY':100}
    BOX_NUM = 125

    def __init__(self,width,height,money):
        self.menu_pic = arcade.load_texture('pics/Shop/shop.png')
        self.menu_pic.center_x = 400
        self.menu_pic.center_y = 300

        self.moving = [arcade.load_texture('pics/Shop/1.png'),arcade.load_texture('pics/Shop/11.png')]
        self.set_pic_point(self.moving,width + width//2 - 100,1)

        self.moving_2 = [arcade.load_texture('pics/Shop/2.png'),arcade.load_texture('pics/Shop/22.png')]
        self.set_pic_point(self.moving_2,width + width//2 -100,2)

        self.moving += self.moving_2

        self.width = width
        self.height = height
        self.key = 'UP'
        self.BOX = height//5
        self.BOX_DOW = height
        self.num = self.BOX_NUM
        self.finish_shop = False
        self.player_money = money
        self.mode = False
        self.mode_text = "Easy"

        #Status
        self.health = 3
        self.attack_delay = 0.05

        self.call_time = 0

    @staticmethod
    def set_pic_point(picture,x,y):
        for pic in picture:
            pic.change_x = 1
            pic.change_y = y

            pic.center_y = 300
            pic.center_x = x

    def draw_pic(self,pic):
        arcade.draw_texture_rectangle(pic.center_x, pic.center_y,
                                      texture=pic,height=600,width=800)

    def draw_text_and_box(self):
        pass

    def draw(self):
        arcade.set_background_color(arcade.color.GRAY)

        arcade.draw_texture_rectangle(self.menu_pic.center_x, self.menu_pic.center_y,
                                      texture=self.menu_pic, height=600, width=800)

        self.draw_pic(self.moving[1])
        self.draw_pic(self.moving_2[1])
        self.draw_pic(self.moving[0])
        self.draw_pic(self.moving_2[0])

        arcade.draw_rectangle_filled(self.width // 2, self.height // 8, self.width, self.height // 3,
                                     color=arcade.color.WHITE)
        arcade.draw_rectangle_outline(self.width // 2, self.height // 8, self.width, self.height // 3,
                                      color=arcade.color.BLACK)

        arcade.draw_rectangle_filled(self.BOX_NUM, self.height // 5, self.width // 3, self.height // 10,
                                     color=arcade.color.GRAY)
        arcade.draw_text('Health', 25, self.height // 5, arcade.color.BLACK)

        # arcade.draw_rectangle_filled(self.BOX_NUM, self.height // 14, self.width // 3, self.height // 10,
        #                              color=arcade.color.GRAY)
        # arcade.draw_text('Special jacket', 25, self.height // 14, arcade.color.BLACK)

        arcade.draw_rectangle_filled(self.BOX_NUM + Box_space, self.height // 5, self.width // 3, self.height // 10,
                                     color=arcade.color.GRAY)
        arcade.draw_text('Attack delay', Text_space_from_box, self.height // 5, arcade.color.BLACK)

        # arcade.draw_rectangle_filled(self.BOX_NUM + Box_space, self.height // 14, self.width // 3, self.height // 10,
        #                              color=arcade.color.GRAY)
        # arcade.draw_text('Something', Text_space_from_box, self.height // 14, arcade.color.BLACK)

        arcade.draw_rectangle_filled(self.BOX_NUM + 2*Box_space, self.height // 5, self.width // 3, self.height // 10,
                                     color=arcade.color.BRONZE)
        arcade.draw_text(f'Change mode : {self.mode_text}', Text_space_from_box*2, self.height // 5, arcade.color.BLACK)


        arcade.draw_rectangle_filled(self.BOX_NUM+ 2*Box_space, self.height // 14, self.width // 3, self.height // 10,
                                     color=arcade.color.BRONZE)
        arcade.draw_text('Go to the dungeon', Text_space_from_box*2, self.height // 14, arcade.color.BLACK)

        arcade.draw_text(f'Current Money {self.player_money}', self.width//2 - 50,self.height//2 -100,arcade.color.WHITE,font_size= 40)


        arcade.draw_rectangle_outline(self.num, self.BOX, self.width // 3, self.height // 10,
                                      color=arcade.color.RED)

    def update(self):
        if self.call_time >= 2:
            self.call_time = 0
            for move in self.moving:
                self.update_p(move)
        self.call_time += 1
    def update_p(self,object_m):
        object_m.center_x -= object_m.change_x
        object_m.center_y += sin(object_m.center_x)*object_m.change_y
        if object_m.center_x <= -self.width//2 + 100:
            object_m.center_x = self.width + self.width//2


    def on_key_press(self, key):
        if key == arcade.key.UP:
            self.BOX = self.height // 5

        elif key == arcade.key.DOWN:
            self.BOX = self.height // 14

        elif key == arcade.key.LEFT:
            self.num -= Box_space

        elif key == arcade.key.RIGHT:
            self.num += Box_space

        self.check_exceed()

        if key == arcade.key.ENTER:
            self.check_buying()

    def check_exceed(self):
        if self.num < self.BOX_NUM:
            self.num = self.BOX_NUM
        elif self.num > self.BOX_NUM + 2 * Box_space:
            self.num = self.BOX_NUM + 2*Box_space

    def check_buying(self):
        if self.num == self.BOX_NUM + Box_space*2 and self.BOX == self.height // 14:
            self.finish_shop = True

        elif self.num == self.BOX_NUM + Box_space*2  and self.BOX == self.height//5:
            self.mode = not self.mode
            if self.mode:
                self.mode_text = "Hard"
            else:
                self.mode_text = "Easy"

        elif self.num == self.BOX_NUM and self.BOX == self.height//5:
            money_and_status = self.decease_money(Menu.Price['HEART'])
            if money_and_status[0]:
                self.health += 1
                self.player_money = money_and_status[1]


        elif self.num == self.BOX_NUM + Box_space and self.BOX == self.height//5:
            money_and_status = self.decease_money(Menu.Price['ATTACK_DELAY'])
            if money_and_status[0]:
                self.attack_delay = abs(self.attack_delay + 0.005)
                self.player_money = money_and_status[1]

    def decease_money(self,price):
        money = self.player_money - price
        status = True
        if money <= -1:
            status = False
        return status,money


