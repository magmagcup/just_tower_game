import arcade
from random import randint
from time import time

SCREEN_WIDTH = 800

class Dialog(arcade.Sprite):
    def __init__(self, scale, pointx, pointy):
        #NEED TO FIX BUT TOO LAZY JUST HARD CODE IT
        super().__init__()
        self.dialog_dict = {0:self.dialog_0(),1:self.dialog_1(),2:self.dialog_2()}
        self.num_context = 0
        self.center_x = pointx
        self.center_y = pointy
        self.pic = ['pics/dialog/normal.png','pics/dialog/speak.png','pics/dialog/smile.png','pics/dialog/pique.png','pics/dialog/male.png']
        for each_pic in self.pic:
            self.textures.append(arcade.load_texture(each_pic,scale=scale))
        self.time_for_dialog = time()
        self.context = False
        self.tutorial()

        #FOR DIALOG




    def tutorial(self):
        self.context = [("Hello and welcome to the tutorial of the game.",1),
        ("My name is viola a former magician who serve this country for about...",2),
        ("Hmm? We don't need a back story yet?",0),
                        ("Well... Just ignore what I said earlier.",3),
                        ("Ahem Let's me teach you about the basic control.",1),
                        ("Press x to attack",1),
                        ("Move with keys pad",0),
                        ("Hm... I think that's all",3),
                        ("Enjoy the game!",1),
                        ]

    #For dialog
    @staticmethod
    def dialog_0():
        return [("Hey guys main protag here sorry for the delay.",-1),("The dev is very busy to the point where he couldn't paint the main protag *crying*",-1)
            ,("But worry not! You will see me in---",-1),('Just ignore him.',2)]
    @staticmethod
    def dialog_1():
        return [("Ouch my feet hurt...",1),("Obviously! Who can jump that high without hurting their feet!",-1),('Mario?',3),('I mean a real person...',-1)]
    @staticmethod
    def dialog_2():
        return [("Wait a minute.",-1),('Hm what wrong?',1),
                ('After some consideration about mario jumping I came up with this conclusion.',-1),
                ("What if Mario feet really hurt but he can't express his pain?",-1),
                ('...',0),('...',1),("...Let's hope not",3)]




    def b_dialog_0(self):
        self.context = [('Are you okay?',1),("HELP!",-1)]
        return True

    #For dialog

    def check(self):
        if self.context is None:
            return False
        elif self.num_context == len(self.context):
            self.num_context = 0
            self.context = None
            return False
        return True

    def time_check(self,level):
        if level <= 1:
            self.time_for_dialog = time()
        elif level > 1 and time() - self.time_for_dialog >= 40:
            self.context = self.dialog_dict[randint(0,2)]
            # self.context = self.dialog_dict[2]
            self.time_for_dialog = time()
            return True
        return None

    def on_key_press(self,key,modifier):
        if key == arcade.key.ENTER:
            self.num_context += 1

        if key == arcade.key.X:
            self.num_context = len(self.context)

    def on_draw(self,status):
        if self.context is not None and status:
            arcade.draw_rectangle_filled(SCREEN_WIDTH//2 - 100,100,500,100,arcade.color.GRAY)
            self.set_texture(self.context[self.num_context][1])
            self.draw()
            arcade.draw_text(self.context[self.num_context][0],0,100,arcade.color.WHITE,font_size=20)

    def b_page(self,num):
        return self.b_dialog_0()