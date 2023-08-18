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
            "bolt": (10, 5),
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

            skill_data = { #TODO set correct requirements and add all skills 
                "bolt": {
                    "image_path": "img/bolt_skill.png",
                    "position": (152, 71),
                    "name": "Bolt",
                    "description": "Damage:\n5% spellpower",
                    "requirements": "Requirements:\nlevel 0 1 coin"
                },
                "energyblast": {
                    "image_path": "img/Energyblast_skill.png",
                    "position": (266, 71),
                    "name": "Energyblast",
                    "description": "Damage:\n20% spellpower",
                    "requirements": "Requirements:\nlevel 0 1 coin"
                },
                "fireball": {
                    "image_path": "img/fireball_skill.png",
                    "position": (209, 71),
                    "name": "Fireball",
                    "description": "Damage:\n10% spellpower",
                    "requirements": "Requirements:\nlevel 0 1 coin"
                },
                
                "deathball": {
                    "image_path": "img/deathball_skill.png",
                    "position": (325,71),
                    "name": "Death ball",
                    "description": "Damage:\n25% spellpower",
                    "requirements": "Requirements:\nlevel 0 1 coin"
                }
            }

            colliding_skill_rects = []
            names = []

            for skill in skills_to_render:
                
                if skill in skill_data:
                    skill_info = skill_data[skill]
                    skill_image = self.pygame.image.load(skill_info["image_path"]).convert_alpha()
                    skill_image = self.pygame.transform.scale(skill_image, (25, 25))
                    skill_rect = skill_image.get_rect(center=skill_info["position"])
                    #skill_info = skill_data[skill]
                    

                    surface.blit(skill_image, skill_rect)
                    if skill_rect.collidepoint(mousepos):
                        colliding_skill_rects.append(skill_rect)
                        stat_image = self.pygame.image.load("img/status_bar.png").convert_alpha()
                        stat_surface = self.pygame.Surface((140, 140))
                        
                        text = self.skillfont.render(skill_info["name"], True, (255, 255, 255))
                        text_rect = text.get_rect(center=(60, 10))
                        skill_info_text = self.skillfont.render(skill_info["description"], True, (255, 255, 255))
                        skill_info_rect = skill_info_text.get_rect(center=(65, 50))
                        requirements_info_text = self.skillfont.render(skill_info["requirements"], True, (255, 255, 255))
                        requirements_info_rect = requirements_info_text.get_rect(center = (55, 100))
                        stat_surface.blit(text, text_rect)
                        stat_surface.blit(skill_info_text, skill_info_rect)
                        stat_surface.blit(requirements_info_text, requirements_info_rect)
                        stat_surface.blit(stat_image, skill_rect)
                        if clicked[2]:
                            self.Buy_Skill(skill)
                        
                if colliding_skill_rects:
                    stat_surface.set_alpha(200)
                    surface.blit(stat_surface, colliding_skill_rects[0])

            
                    
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

