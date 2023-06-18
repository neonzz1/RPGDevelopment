from Sprites import BaseSprite

class Skills(BaseSprite):
    def __init__(self):
        super().__init__()
        skills = []
    
    def rendering(self):
        ''

    def Buy_Skill(self, player, handler):
        if player.level >= 1 and handler.money >= 10:
            print('Success!!')
            handler.money -= 10