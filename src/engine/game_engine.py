import asyncio
import json
import pygame
import esper

from src.create.prefab_creator import create_bullet_square, create_game_control, create_input_player, create_player_square, create_square,create_enemy_spawner, create_textos_fijos
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_texto import CTexto
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import system_animation

from src.ecs.systems.s_check_bullet_bound import system_check_bullet_bound
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_explosion_time import system_explosion_time
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_limit_bullet_amont import system_limit_bullet_amount
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_pause import system_pause_control
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_restrain_player_bounds import system_restrain_player_bound
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_text import system_show_texts

class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), 
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

        # Original framerate = 0
        # Original bg_color (0, 200, 128)

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/bullet.json", encoding="utf-8") as player_bullet:
            self.bullets_cfg = json.load(player_bullet)
        with open("assets/cfg/explosion.json", encoding="utf-8") as enemy_explosion:
            self.explosion_cfg = json.load(enemy_explosion)
            

            
        

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
       self._player_entity = create_player_square(self.ecs_world,self.player_cfg,self.level_01_cfg["player_spawn"])
       self._player_c_v = self.ecs_world.component_for_entity(self._player_entity,CVelocity)
       self._player_c_t = self.ecs_world.component_for_entity(self._player_entity,CTransform)
       self._player_c_s = self.ecs_world.component_for_entity(self._player_entity,CSurface)
       
       self._game_entity = create_game_control(self.ecs_world)
       self._game_g_s = self.ecs_world.component_for_entity(self._game_entity,CGameState)


       create_enemy_spawner(self.ecs_world,self.level_01_cfg)
       create_input_player(self.ecs_world)
       create_textos_fijos(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
    
    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world,event,self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        
        system_show_texts(self.ecs_world)
        #system_animation(self.ecs_world,self.delta_time)
        if(self._game_g_s.state == GameState.PLAYING ):
           system_movement(self.ecs_world, self.delta_time)
           system_enemy_spawner(self.ecs_world,self.enemies_cfg,self.delta_time)
           system_animation(self.ecs_world,self.delta_time)
        
        
        system_screen_bounce(self.ecs_world, self.screen)
        system_check_bullet_bound(self.ecs_world, self.screen)
        system_explosion_time(self.ecs_world)
        system_collision_player_enemy(self.ecs_world,self._player_entity,self.level_01_cfg,self.explosion_cfg)
        system_collision_bullet_enemy(self.ecs_world,self.explosion_cfg)
        system_limit_bullet_amount(self.ecs_world,self.level_01_cfg["player_spawn"]["max_bullets"])
        system_restrain_player_bound(self.ecs_world, self.screen)
        system_pause_control(self.ecs_world,self._game_entity)
        #system_hunter_chase(self.ecs_world,self._player_entity,self.enemies_cfg["Hunter"])
        system_hunter_state(self.ecs_world,self._player_entity)
        
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self,c_input:CInputCommand):
        print(c_input.name+" "+str(c_input.phase))
        
        if c_input.name=="PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]
        if c_input.name=="PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
        if c_input.name=="PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.y += self.player_cfg["input_velocity"]
        if c_input.name=="PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.y -= self.player_cfg["input_velocity"]
        if(c_input.name == "PLAYER_FIRE"):
            print("fire!!")
            if c_input.phase == CommandPhase.START:
               ####
               pos_x = self._player_c_t.pos.x + self._player_c_s.area.size[0]/2 
               pos_y = self._player_c_t.pos.y + self._player_c_s.area.size[1]/2
               ####
               create_bullet_square(self.ecs_world,pygame.Vector2(pos_x,pos_y),self.bullets_cfg)
        if  c_input.name =="PLAYER_PAUSE":
               if c_input.phase == CommandPhase.START:
                   if(self._game_g_s.state == GameState.PAUSED):
                      self._game_g_s.state = GameState.PLAYING
                   else :
                      self._game_g_s.state = GameState.PAUSED


    
    
    

  




    
