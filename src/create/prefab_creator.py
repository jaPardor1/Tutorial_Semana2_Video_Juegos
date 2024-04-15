
import random
import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_square(ecs_world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color):
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                CTransform(pos))
    ecs_world.add_component(cuad_entity, 
                CVelocity(vel))

def create_enemy_square(world:esper.World,pos:pygame.Vector2,enemy_info:dict):
   size = pygame.Vector2(enemy_info["size"]["x"],enemy_info["size"]["y"])
   color = pygame.Color(enemy_info["color"]["r"],
                          enemy_info["color"]["g"],
                          enemy_info["color"]["b"])
   vel_max= enemy_info["velocity_max"]
   vel_min= enemy_info["velocity_min"]
   vel_range = random.randrange(vel_min,vel_max)
   velocity = pygame.Vector2(random.choice([-vel_range,vel_range]),
                             random.choice([-vel_range,vel_range]))
   create_square(world,size,pos,velocity,color)

def create_enemy_spawner(world:esper.World,level_data:dict):
        spawner_entity = world.create_entity()
        world.add_component(spawner_entity,CEnemySpawner(level_data["enemy_spawn_events"]))
