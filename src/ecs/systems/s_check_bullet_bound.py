

#sistema para eliminar las balas que se salen de la pantalla

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet



def system_check_bullet_bound(world:esper.World, screen:pygame.Surface):
      screen_rect = screen.get_rect()
      bullet_components = world.get_components(CTransform, CVelocity, CSurface,CTagBullet)
      for bullet_entity, (c_t, c_v, c_s,c_e) in bullet_components:
          bullet_rect = c_s.surf.get_rect(topleft=c_t.pos) 
          if not screen_rect.contains(bullet_rect):
               world.delete_entity(bullet_entity)
              

      # cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
      #   if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
      #      world.delete_entity(bullet_component)
      #   if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
      #       world.delete_entity(bullet_component)