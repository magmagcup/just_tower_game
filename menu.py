import arcade

Box_space = 250

class Menu:
    HEART = 50
    ATTACK_DELAY = 100
    BOX_NUM = 125


    def __init__(self,width,height):
        self.menu_pic = arcade.Sprite('pics/Shop/shop.png')
        self.menu_pic.center_x = 300
        self.menu_pic.center_y = 300

        self.width = width
        self.height = height
        self.key = 'UP'
        self.BOX = height//5
        self.BOX_DOW = height
        self.num = self.BOX_NUM
        self.finish_shop = False

        #Status
        self.health = 3
        self.attack_delay = 0.5


    def draw(self,dialog_status):
        self.menu_pic.draw()

        if not dialog_status:
            arcade.set_background_color(arcade.color.GRAY)
            arcade.draw_rectangle_filled(self.width // 2, self.height // 8, self.width, self.height // 3,
                                         color=arcade.color.WHITE)
            arcade.draw_rectangle_outline(self.width // 2, self.height // 8, self.width, self.height // 3,
                                          color=arcade.color.BLACK)

            arcade.draw_rectangle_filled(self.BOX_NUM, self.height // 5, self.width // 3, self.height // 10,
                                         color=arcade.color.GRAY)
            arcade.draw_text('Health', 25, self.height // 5, arcade.color.BLACK)
            arcade.draw_rectangle_filled(self.BOX_NUM, self.height // 14, self.width // 3, self.height // 10,
                                         color=arcade.color.GRAY)
            arcade.draw_text('Special jacket', 25, self.height // 14, arcade.color.BLACK)
            arcade.draw_rectangle_filled(self.BOX_NUM + Box_space, self.height // 5, self.width // 3, self.height // 10,
                                         color=arcade.color.GRAY)
            arcade.draw_text('Attack delay', 275, self.height // 5, arcade.color.BLACK)
            arcade.draw_rectangle_filled(self.BOX_NUM + Box_space, self.height // 14, self.width // 3, self.height // 10,
                                         color=arcade.color.GRAY)
            arcade.draw_text('Go to the dungeon', 275, self.height // 14, arcade.color.BLACK)
            arcade.draw_rectangle_outline(self.num, self.BOX, self.width // 3, self.height // 10,
                                          color=arcade.color.RED)


    def on_key_press(self, key):
        if key == arcade.key.UP:
            self.BOX = self.height // 5

        elif key == arcade.key.DOWN:
            self.BOX = self.height // 14

        elif key == arcade.key.LEFT:
            self.num = 125

        elif key == arcade.key.RIGHT:
            self.num = 125 + Box_space

        if key == arcade.key.ENTER:
            self.check_buying()

    def check_buying(self):
        if self.num == 125 + Box_space and self.BOX == self.height // 14:
            self.finish_shop = True

        elif self.num == 125 and self.BOX == self.height//5:
            self.health += 1

        elif self.num == 125 + Box_space and self.BOX == self.height//5:
            self.attack_delay = abs(self.attack_delay + 0.05)

