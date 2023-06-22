from Sprites import BaseSprite


class Skillsys(BaseSprite):
    def __init__(self, player, handler):
        image_path = "img/status_bar.png"
        super().__init__(image_path)
        self.skillimage = None
        self.hide = True
        self.available_skills = {
            "fireball": (0, 0),
            "Bolt": (10, 5),
            "energyblast": (15, 10),
            "deathball": (100, 40),
            "selfdestruct": (0, 0),
            "fired": (20, 20),
            "fireballv2": (30, 10)
        }
        self.load_image(image_path)
        self.pressed = 0
        self.player = player
        self.handler = handler

    def toggle_visibility(self):
        self.pressed += 1
        if self.pressed == 1:
            self.hide = not self.hide
            self.pressed = 0
    
    def rendering(self, surface):
        if not self.hide:
            surface.blit(self.skillimage, (40, 30))
            skills_to_render = [skill for skill in self.available_skills.keys() if skill not in self.player.skills]

            for i, item in enumerate(skills_to_render):
                text_surface = self.smallerfont.render(item, True, (0, 0, 0))  # Render the text
                text_rect = text_surface.get_rect()
                text_rect.topleft = (40, i * 30 + 30)  # Position the text
                surface.blit(text_surface, text_rect)  # Blit the text onto the window
                mousepos = self.pygame.mouse.get_pos()
                if text_rect.collidepoint(mousepos):
                    clicked = self.pygame.mouse.get_pressed() #TODO finish implementing this!
                    if clicked[0]:
                        wskill = item
                        self.Buy_Skill(wskill)  

    def Buy_Skill(self, wskill):
        if wskill in self.player.skills:
            print('You already have {}!'.format(wskill))

        else:
            cost, level_requirement = self.available_skills.get(wskill, (0, 0))
            if self.handler.money >= cost and self.player.level >= level_requirement:
                self.handler.money -= cost
                self.player.skills.append(wskill)
                self.skill()

            else:
                print('Not enough money or level too low')

    def skill(self):
        for i in self.player.skills:
            if i in self.available_skills:
                self.available_skills.pop(i)

    def load_image(self, image_path):
        try:
            self.skillimage = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading skills image:", str(e))

