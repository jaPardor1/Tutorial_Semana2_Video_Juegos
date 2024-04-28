
import pygame 
class CTexto:
    def __init__(self,text:str,font_size:int,color:pygame.Color) -> None:
        _font_path = "assets/fnt/PressStart2P.ttf"
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(_font_path, font_size)
        #self.position_ratio = position_ratio
        

        