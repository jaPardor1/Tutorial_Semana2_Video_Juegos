
import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.c_hunter import CHunter
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_texto import CTexto
from src.ecs.components.c_tiempo_vida import CTiempoVida
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_ability import AbilityState, CTagAbility
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_chaser import CTagChaser
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_pause import CTagPause
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet
from src.engine.service_locator import ServiceLocator


def create_square(ecs_world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color)-> int:
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                CTransform(pos))
    ecs_world.add_component(cuad_entity, 
                CVelocity(vel))
    return cuad_entity

def create_sprite (world:esper.World,pos:pygame.Vector2,vel:pygame.Vector2,
                   surface:pygame.Surface) -> int : 
     sprite_entity = world.create_entity()
     world.add_component(sprite_entity,CSurface.from_surface(surface))
     world.add_component(sprite_entity,CTransform(pos))
     world.add_component(sprite_entity,CVelocity(vel))

     return sprite_entity
     

def create_enemy_spawner(world:esper.World,level_data:dict):
        spawner_entity = world.create_entity()
        world.add_component(spawner_entity,CEnemySpawner(level_data["enemy_spawn_events"]))

def create_enemy_square(world:esper.World,pos:pygame.Vector2,enemy_info:dict):
   #enemy_surface = pygame.image.load(enemy_info["image"]).convert_alpha()
   enemy_surface = ServiceLocator().images_service.get(enemy_info["image"])
   vel_max= enemy_info["velocity_max"]
   vel_min= enemy_info["velocity_min"]
   vel_range = random.randrange(vel_min,vel_max)
   velocity = pygame.Vector2(random.choice([-vel_range,vel_range]),
                             random.choice([-vel_range,vel_range]))
   enemy_entity=create_sprite(world,pos,velocity,enemy_surface)
   world.add_component(enemy_entity,CTagEnemy())
   ServiceLocator.sounds_service.play(enemy_info["sound"])


def create_enemy_hunter(world:esper.World,pos:pygame.Vector2,enemy_info:dict):
   #enemy_surface = pygame.image.load(enemy_info["image"]).convert_alpha()
   enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
   vel  = pygame.Vector2(0,0)
   enemy_entity=create_sprite(world,pos,vel,enemy_surface)
   velocity_chase = enemy_info["velocity_chase"]
   velocity_return = enemy_info["velocity_return"]
   distance_start_chase = enemy_info["distance_start_chase"]
   distance_start_return = enemy_info["distance_start_return"]
   world.add_component(enemy_entity,CTagEnemy())
   world.add_component(enemy_entity,CTagChaser())
   world.add_component(enemy_entity,CHunter(pos,velocity_chase,velocity_return,distance_start_chase,distance_start_return))
   world.add_component(enemy_entity,CHunterState())
   world.add_component(enemy_entity,CAnimation(enemy_info["animations"]))
   



def create_player_square(world:esper.World,player_info:dict,player_lvl_info:dict)-> int:
     

     #player_surface = pygame.image.load(player_info["image"]).convert_alpha()
     player_surface = ServiceLocator.images_service.get(player_info["image"])
     size = player_surface.get_size()
     pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size[0]/2),
                          player_lvl_info["position"]["y"]-  (size[1]/2))
     vel = pygame.Vector2(0,0)
     player_entity = create_sprite(world,pos,vel,player_surface)
     world.add_component(player_entity,CTagPlayer())
     world.add_component(player_entity,CAnimation(player_info["animations"]))
     world.add_component(player_entity,CPlayerState())
     return player_entity

def create_bullet_square(world:esper.World,pos:pygame.Vector2,bullet_info:dict):
     
         
     #bullet_surface = pygame.image.load(bullet_info["image"])
     bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
     vel = bullet_info["velocity"]
     x, y = pygame.mouse.get_pos()
     vect_mouse = pygame.Vector2(x,y)
     vel_real = (vect_mouse-pos)
     vel_real = vel_real.normalize() * vel

     velocity = vel_real
     bullet_entity = create_sprite(world,pos,velocity,bullet_surface)
     world.add_component(bullet_entity,CTagBullet())
     ServiceLocator.sounds_service.play(bullet_info["sound"])
     

def create_input_player(world:esper.World):
     input_left = world.create_entity()
     input_right = world.create_entity()
     input_up = world.create_entity()
     input_down = world.create_entity()
     MOUSE_down = world.create_entity()
     input_pause = world.create_entity()
     input_special = world.create_entity()
     world.add_component(input_left,CInputCommand("PLAYER_LEFT",pygame.K_LEFT))
     world.add_component(input_right,CInputCommand("PLAYER_RIGHT",pygame.K_RIGHT))
     world.add_component(input_up,CInputCommand("PLAYER_UP",pygame.K_UP))
     world.add_component(input_down,CInputCommand("PLAYER_DOWN",pygame.K_DOWN))
     world.add_component(MOUSE_down,CInputCommand("PLAYER_FIRE",pygame.BUTTON_LEFT))
     world.add_component(input_pause,CInputCommand("PLAYER_PAUSE",pygame.K_p))
     world.add_component(input_special,CInputCommand("PLAYER_SPECIAL",pygame.BUTTON_RIGHT))



def create_explosion(world:esper.World,pos:pygame.Vector2,explosion_info:dict):
     
     #explosion_surface = pygame.image.load(explosion_info["image"]).convert_alpha()
     explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
     pos = pygame.Vector2(pos.x,
                          pos.y)
     vel = pygame.Vector2(0,0)
     explosion_entity = create_sprite(world,pos,vel,explosion_surface)
     world.add_component(explosion_entity,CTagExplosion())
     world.add_component(explosion_entity,CTiempoVida())
     world.add_component(explosion_entity,CAnimation(explosion_info["animations"]))
     ServiceLocator.sounds_service.play(explosion_info["sound"])

def create_textos_fijos(world:esper.World):
     text_entity = world.create_entity()
     color = pygame.Color(255, 255, 255)
     world.add_component(text_entity,CTexto("EJERCICIO 04",10,color))
     pos = pygame.Vector2(10,10)
     world.add_component(text_entity,CTransform(pos))

     ###################################################################
     text_entity = world.create_entity()
     color = pygame.Color(255, 255, 255)
     world.add_component(text_entity,CTexto("ESPECIAL",8,color))
     pos = pygame.Vector2(10,320)
     world.add_component(text_entity,CTransform(pos))

     ###################################################################

     text_entity = world.create_entity()
     color = pygame.Color(4, 221, 4)
     world.add_component(text_entity,CTexto("100%",8,color))
     pos = pygame.Vector2(10,330)
     world.add_component(text_entity,CTransform(pos))
     world.add_component(text_entity,CTagAbility())


     #################################################################

     text_entity = world.create_entity()
     color = pygame.Color(253,253, 9)
     texto = "Controles: tecla p= pausa , flechas = mover jugador , click izquierdo: Disparar, click derecho: **Especial**  "

     world.add_component(text_entity,CTexto(texto,5,color))
     pos = pygame.Vector2(10,25)
     world.add_component(text_entity,CTransform(pos))

def create_game_control(world:esper.World)-> int:
     game_entity = world.create_entity()
     world.add_component(game_entity,CGameState())
     return game_entity
def create_game_pause_text(world:esper.World):
        text_entity = world.create_entity()
        color = pygame.Color(253,253, 9)
        texto = "**** Pausa ****"
        world.add_component(text_entity,CTexto(texto,7,color))
        pos = pygame.Vector2(300,150)
        world.add_component(text_entity,CTransform(pos))
        world.add_component(text_entity,CTagPause())

def delete_game_pause_text(world:esper.World):
        components = world.get_components(CTexto,CTransform,CTagPause)
        c_t:CTexto
        for entidad ,(c_t,c_t_r,c_t_p)  in components:
             if(c_t.text=="**** Pausa ****") :
                  world.delete_entity(entidad)
                  break

def activate_ability(world:esper.World):
     components = world.get_components(CTagBullet,CTransform,CVelocity,CSurface)
     
     text_component = world.get_components(CTexto,CTagAbility)
     
     for comp , (c_t,c_t_a) in text_component:
          if(c_t_a.state ==AbilityState.FULL ):
              print("si")
              c_t.text = "0%"
              print(c_t_a.state)
          
     if(not c_t_a ==AbilityState.CHARGING ):
        c_t_a.state =AbilityState.CHARGING 
        limit = 4
        amnt =1
     
        for bullet_entity , (_,c_t,c_v,c_s) in components:
           x=0
           y=0
           while amnt <=limit:
             x = c_t.pos.x + c_s.area.width* (1 if amnt % 2 == 0 else -1)  # Alternar entre ancho y -ancho para la posición x
             y = c_t.pos.y + c_s.area.height * (1 if amnt < 2 else -1) 
             print(c_t.pos)
             new_pos= pygame.Vector2(x,y)
             create_special_bullet(world,new_pos,c_v.vel)
             amnt +=1
             world.delete_entity(bullet_entity)


def create_special_bullet(world:esper.World,pos:pygame.Vector2,velo:pygame.Vector2):
     bullet_surface = ServiceLocator.images_service.get("assets/img/bullet_especial.png")
     special_bullet_entity = create_sprite(world,pos,velo,bullet_surface)
     world.add_component(special_bullet_entity,CTagSpecialBullet(True))
     world.add_component(special_bullet_entity,CTagBullet())
     
