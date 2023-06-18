from Sprites import BaseSprite

class Cursor(BaseSprite):
    def __init__(self):
        image_path = "img/cursor.png"
        super().__init__(image_path)
        self.rect = self.image.get_rect()
        self.wait = 0
    
    def pause(self):
        if self.wait == 1:
            self.wait = 0
        else:
            self.wait = 1
    
    def hover(self, mouse, surface):
        if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
            self.pygame.mouse.set_visible(False)
            self.rect.center = self.pygame.mouse.get_pos()  # update position 
            surface.blit(self.image, self.rect)
        else:
            self.pygame.mouse.set_visible(True)