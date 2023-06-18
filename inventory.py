from Sprites import BaseSprite

class inventory(BaseSprite):
    def __init__(self):
        image_path = "img/status_bar.png"
        super().__init__(image_path)
        self.items = []
        self.imagee = self.pygame.image.load("img/status_bar.png").convert_alpha()
        self.hide = True
    
    def renderr(self, surface, handler):    
        gold = self.smallerfont.render('Gold', str(handler.money), True, (255,255,255))
        if self.hide == False:
            surface.blit(self.imagee, (175,350))
        print('render called')
        self.pygame.display.flip()