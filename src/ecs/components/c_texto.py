
import pygame 
class Ctexto:
    def __init__(self,text:str,font_path:str,font_size:int,color:pygame.Color) -> None:
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        #self.position_ratio = position_ratio
        self.font = pygame.font.Font(font_path, font_size)

        