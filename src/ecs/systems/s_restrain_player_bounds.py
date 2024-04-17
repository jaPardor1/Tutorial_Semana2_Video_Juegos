# sistema para restringir al jugador de no salirse de la pantalla


import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_restrain_player_bound(world:esper.World, screen:pygame.Surface):
      screen_rect = screen.get_rect()
      player_component = world.get_components(CTransform, CVelocity, CSurface,CTagPlayer)
      for player, (c_t, c_v, c_s,c_e) in player_component:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
           cuad_rect.clamp_ip(screen_rect)
           c_t.pos.x = cuad_rect.x
        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.y = cuad_rect.y