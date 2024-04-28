
import esper
from src.create.prefab_creator import create_game_pause_text, delete_game_pause_text
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.tags.c_tag_pause import CTagPause

def system_pause_control(world:esper.World,game_entity:int):
    game_state = world.component_for_entity(game_entity,CGameState)
    if(game_state.state == GameState.PAUSED):
        component = len(world.get_components(CTagPause))
        if(component==0):
           create_game_pause_text(world)
    else:
       delete_game_pause_text(world)
        
        
