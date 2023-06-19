from Sprites import BaseSprite

class Skills(BaseSprite):
    def __init__(self):
        super().__init__()
        skills = []
        self.avalible_skills = []
    
    def rendering(self):
        ''

    def Buy_Skill(self, player, handler):
        if player.level >= 1 and handler.money >= 10:
            print('Success!!')
            handler.money -= 10
    
    def skill(self, player):
        if player.level >= 1 and player.level < 20:
            self.avalible_skills.append("fireball")
            self.avalible_skills.append("Bolt")
            self.avalible_skills.append("energyblast")
            self.avalible_skills.append("deathball")
            self.avalible_skills.append("self destruct")
            self.avalible_skills.append("fireballv2")
            self.avalible_skills.append("")
            self.avalible_skills.append("fired")

