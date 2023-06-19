from Sprites import BaseSprite

class Skillsys(BaseSprite):
    def __init__(self):
        image_path = "img/status_bar.png"
        super().__init__(image_path)
        skills = []
        self.skillimage = None
        self.hide = True
        self.avalible_skills = ["fireball", "Bolt", "energyblast", "deathball", "self destruct", "fireballv2", "fired"]
        self.load_image(image_path)
        self.pressed = 0

    def toggle_visibility(self):
        self.pressed += 1
        if self.pressed == 1:
            self.hide = not self.hide
            self.pressed = 0
    
    def rendering(self, surface):
        if not self.hide:

            surface.blit(self.skillimage, (40, 30))

            for i, item in enumerate(self.avalible_skills):
                text_surface = self.smallerfont.render(item, True, (0, 0, 0))  # Render the text
                text_rect = text_surface.get_rect()
                text_rect.topleft = (40, i * 30 + 28)  # Position the text
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

