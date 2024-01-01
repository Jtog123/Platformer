import pygame

class FinishFlag:
    def __init__(self, position, flag_image, size) -> None:
        self.position = list(position)
        self.flag_image = flag_image
        self.size = size
    
    def update(self):
        pass

    def render(self, surface, offset=(0,0)):
        surface.blit(self.flag_image, (self.position[0] - offset[0], self.position[1] - offset[1]))

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
