from Sprites import BaseSprite


class Skillsys(BaseSprite):
    def __init__(self, player, handler):
        image_path = "img/skills.png"
        super().__init__(image_path)
        self.skillimage = None
        self.hide = True
        self.available_skills = {
            # first value is cost second is level
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
            clicked = self.pygame.mouse.get_pressed()
            mousepos = self.pygame.mouse.get_pos()
            self.skillimage = self.pygame.transform.scale(self.skillimage, (250,350))
            surface.blit(self.skillimage, (110, 0))
            skills_to_render = [skill for skill in self.available_skills.keys() if skill not in self.player.skills]

            if "fireball" in skills_to_render:
                fireball_image = self.pygame.image.load("img/fireball_skill.png").convert_alpha()
                fireball_image = self.pygame.transform.scale(fireball_image, (25,25))
                fire_rect = fireball_image.get_rect(center=(152, 71))

                surface.blit(fireball_image, fire_rect)
                if fire_rect.collidepoint(mousepos):
                    stat_image = self.pygame.image.load("img/status_bar.png").convert_alpha()
                    stat_surface = self.pygame.Surface((140, 100))
                    text = self.smallerfont.render("Fireball", True, (255,255,255))
                    fire_text_rect = text.get_rect(center=(30,10))
                    skill_info = self.smallerfont.render("Damage:\n10% spellpower", True, (255,255,255))
                    skill_info_rect = skill_info.get_rect(center=(70,50))
                    stat_surface.blit(stat_image, fire_rect)
                    stat_surface.blit(text, fire_text_rect)
                    stat_surface.blit(skill_info, skill_info_rect)
                    surface.blit(stat_surface, fire_rect)
                    if clicked[2]:
                        wskill = "fireball"
                        self.Buy_Skill(wskill)

            if "energyblast" in skills_to_render:
                energyball_image = self.pygame.image.load("img/Energyblast_skill.png").convert_alpha()
                energy_rect = energyball_image.get_rect(center=(210, 71))

                surface.blit(energyball_image, energy_rect)
                if energy_rect.collidepoint(mousepos): #TODO think about how to optimise this
                    stat_image = self.pygame.image.load("img/status_bar.png").convert_alpha()
                    stat_surface = self.pygame.Surface((140, 100))
                    text = self.smallerfont.render("Energy blast", True, (255,255,255))
                    energy_text_rect = text.get_rect(center=(50,10))
                    skill_info = self.smallerfont.render("Damage:\n20% spellpower", True, (255,255,255))
                    skill_info_rect = skill_info.get_rect(center=(70,50))
                    stat_surface.blit(stat_image, energy_rect)
                    stat_surface.blit(text, energy_text_rect)
                    stat_surface.blit(skill_info, skill_info_rect)
                    surface.blit(stat_surface, energy_rect)
                    if clicked[2]:
                        wskill = "energyblast"
                        self.Buy_Skill(wskill)


            for i, item in enumerate(skills_to_render):
                text_surface = self.smallerfont.render(item, True, (0, 0, 0))  # Render the text
                text_rect = text_surface.get_rect()
                text_rect.topleft = (40, i * 30 + 30)  # Position the text
                surface.blit(text_surface, text_rect)  # Blit the text onto the window
                
                if text_rect.collidepoint(mousepos):
                    
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

