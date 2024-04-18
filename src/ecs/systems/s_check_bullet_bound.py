

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
          bullet_rect = CSurface.get_area_relative(c_s.area,c_t.pos)
          if not screen_rect.contains(bullet_rect):
               world.delete_entity(bullet_entity)
              

     