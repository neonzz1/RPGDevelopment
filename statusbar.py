from Sprites import BaseSprite

color_white = (255,255,255)

class StatusBar(BaseSprite):
    def __init__(self):
        image_path = "img/status_bar.png"
        super().__init__(image_path)
        self.surf = self.pygame.Surface((90, 66))
        self.rect = self.surf.get_rect(center = (500, 10))

    def update_draw(self, handler, player, FPS_CLOCK, surface):
        # Create the text to be displayed
        text1 = self.smallerfont.render("STAGE: " + str(handler.stage) , True , color_white)
        text2 = self.smallerfont.render("EXP: " + str(player.experience) , True , color_white)
        text3 = self.smallerfont.render("Money: " + str(handler.money) , True , color_white)
        text4 = self.smallerfont.render("FPS: " + str(int(FPS_CLOCK.get_fps())) , True , color_white)
 
      # Draw the text to the status bar
        surface.blit(text1, (585, 7))
        surface.blit(text2, (585, 22))
        surface.blit(text3, (585, 37))
        surface.blit(text4, (585, 52))