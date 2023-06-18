from Sprites import BaseSprite

color_dark = (100,100,100)

class StageDisplay(BaseSprite):
    def __init__(self, handler, surface):
        image_path = "img/castle.png"
        super().__init__(image_path)
        self.handler = handler
        self.text = self.headingfont.render("STAGE: " + str(handler.stage) , True , color_dark)
        self.rect = self.text.get_rect()
        self.posx = -100
        self.posy = 100
        self.display = False
        self.surface = surface
        self.clear = False

    def move_display(self):
            # Create the text to be displayed
            self.text = self.headingfont.render("STAGE: " + str(self.handler.stage) , True , color_dark)
            if self.posx < 700:
                  self.posx += 5
                  self.surface.blit(self.text, (self.posx, self.posy))
            else:
                self.display = False
                self.posx = -100
                self.posy = 100
    def stage_clear(self):
      self.text = self.headingfont.render("STAGE CLEAR!", True , color_dark)
      if self.posx < 720:
            self.posx += 10
            self.surface.blit(self.text, (self.posx, self.posy))
            self.clear = True
      else:
            self.clear = False
            self.posx = -100
            self.posy = 100