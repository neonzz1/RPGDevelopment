from Sprites import BaseSprite


class Skillsys(BaseSprite):
    def __init__(self, player, handler):
        image_path = "img/status_bar.png"
        super().__init__(image_path)
        self.skills = []
        self.skillimage = None
        self.hide = True
        self.avalible_skills = ["fireball", "Bolt", "energyblast", "deathball", "self destruct", "fireballv2", "fired"]
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

            for i, item in enumerate(self.avalible_skills):
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
        if wskill in self.skills:
            print('You already have {}!'.format(wskill))
        else:
            if wskill == 'fireball':
                if self.handler.money >= 1 and self.player.level >= 1:
                    self.handler.money -= 1
                    self.skills.append(wskill)
                else:
                    print('Not Enough money or level is too low!')

            elif wskill == 'Bolt':
                if self.handler.money >= 10 and self.player.level >= 5:
                    self.handler.money -= 10
                    self.skills.append(wskill)
                else:
                    print('Not enough money or level too low')

            if wskill == 'energyblast':
                if self.handler.money > 15 and self.player.level >= 10:
                    self.handler.money -= 15
                    self.skills.append(wskill)
                else:
                    print('Not enough money or level too low')
            
            if wskill == 'deathball':
                if self.handler.money > 100 and self.player.level >= 40:
                    self.handler.money -= 100
                    self.skills.append(wskill)
                else:
                    print('Not enough money or level too low')

            if wskill == 'self destruct':
                if self.handler.money > 0 and self.player.level >= 0:
                    self.handler.money -= 0
                    self.skills.append(wskill)
                else:
                    print('Not enough money or level too low')

            if wskill == 'fired':
                if self.handler.money > 20 and self.player.level >= 20:
                    self.handler.money -= 20
                    self.skills.append(wskill)
                else:
                    print('Not enough money or level too low')

            if wskill == 'fireballv2':
                if self.handler.money >= 30 and self.player.level >= 10:
                    self.handler.money -= 30
                    self.skills.append(wskill)
                else:
                    print('Not enough money or level too low')
            else:
                print(wskill)
            
        print('clicked')
    
    def skill(self):
        for i in self.skills:
            if i == self.avalible_skills.index(0):
                self.avalible_skills.remove(i)

    def load_image(self, image_path):
        try:
            self.skillimage = self.pygame.image.load(image_path).convert_alpha()
        except self.pygame.error as e:
            print("Error loading skills image:", str(e))

