import pygame
class CHunter:
    def __init__(self,pos:pygame.Vector2,velocity_chase:int,
                 velocity_return:int,distance_start_chase:int,
                 distance_start_return:int
                 ) -> None:
       self.pos_origen = pygame.Vector2(pos.x,pos.y)
       self.velocity_chase=velocity_chase
       self.velocity_return=velocity_return
       self.distance_start_chase=distance_start_chase
       self.distance_start_return=distance_start_return
       #print(self.pos_origen)