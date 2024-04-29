import esper
import pygame
from src.ecs.components.c_texto import CTexto
from src.ecs.components.tags.c_tag_ability import AbilityState, CTagAbility
def system_ability_status(world:esper.World):
   component = world.get_components(CTexto,CTagAbility)
   
   c_t_a:CTagAbility
   for comp , (c_t,c_t_a) in component:
   
      if(c_t_a.state ==AbilityState.CHARGING ):
         #print(c_t_a.state)
         c_t.text = str(int(   c_t.text.replace("%","")   )+1)+"%"
         c_t.color = pygame.Color(230,3,3)
         if(c_t.text=="100%"):
            c_t_a.state = AbilityState.FULL 
            c_t.color = pygame.Color(1,247,1)
      

