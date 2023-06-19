from Sprites import BaseSprite

class Skills(BaseSprite):
    def __init__(self):
        image_path = "img/status_bar.png"
        super().__init__(image_path)
        skills = []
        self.skillimage = None
        self.avalible_skills = ["fireball", "Bolt", "energyblast", "deathball", "self destruct", "fireballv2", "fired"]
        self.load_image(image_path)
    
    def rendering(self, surface):
        if not self.hide:

            for i, item in enumerate(self.avalible_skills):
                text_surface = self.smallerfont.render(item, True, (255, 255, 255))  # Render the text
                text_rect = text_surface.get_rect()
                text_rect.topleft = (10, i * 30 + 10)  # Position the text
                surface.blit(text_surface, text_rect)  # Blit the text onto the window

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

    def load_image(self, image_path):
        try:
            self.skillimage = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading inventory image:", str(e))

