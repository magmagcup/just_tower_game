import arcade

GRAVITY = 0.6


class Physic:
    def __init__(self):
        self.physic_player = None
        self.physic_enemy = []

    def add_physic(self,player,enemy,wall):
        self.physic_player = None
        self.physic_enemy = []
        player_phy = arcade.PhysicsEnginePlatformer(player,wall,gravity_constant=GRAVITY)
        self.physic_player = player_phy
        for each_enemy in enemy:
            enemy_phy = arcade.PhysicsEnginePlatformer(each_enemy,wall,gravity_constant=GRAVITY)
            self.physic_enemy.append(enemy_phy)

    def update(self):
        self.physic_player.update()
        for each in self.physic_enemy:
            each.update()
