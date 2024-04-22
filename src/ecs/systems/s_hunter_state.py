import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter import CHunter
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_hunter_state(world:esper.World,pl:int):
    components = world.get_components(CTransform,CVelocity,CAnimation,CHunterState,CHunter)
    
    for _,(c_t,c_v,c_a,c_hst,c_h) in components:
        if c_hst.state==HunterState.IDLE:
            _set_animation(c_a,1)
            _perseguir(world,pl,c_t,c_v,c_hst,c_h)
            #_do_idle_state(c_v,c_a,c_hst)
        elif c_hst.state == HunterState.CHASING:
            _set_animation(c_a,0)
            _perseguir(world,pl,c_t,c_v,c_hst,c_h) 
            #_do_move_state(c_v,c_a,c_hst)
        elif c_hst.state == HunterState.TARGET_LOST:
            _set_animation(c_a,1)
            _return_to_original_pos(world,pl,c_t,c_v,c_hst,c_h)

def _set_animation(c_a:CAnimation,num_anim:int):
    if c_a.current_animation == num_anim:
        return
    c_a.current_animation = num_anim
    c_a.current_animation_time = 0
    c_a.current_frame = c_a.animations_list[c_a.current_animation].start


def _perseguir(world:esper.World,player_entity:int,c_t:CTransform,c_v:CVelocity,c_hst:CHunterState,c_h:CHunter):
    pl_t = world.component_for_entity(player_entity,CTransform)
    distance = pl_t.pos.distance_to(c_t.pos)
    
    if(distance<=c_h.distance_start_chase):
        #print('chasing!!!')
        c_hst.state = HunterState.CHASING
        c_v.vel.x = pl_t.pos.x - c_t.pos.x
        c_v.vel.y = pl_t.pos.y - c_t.pos.y
        c_v.vel.scale_to_length(c_h.velocity_chase)
    elif(distance<=c_h.distance_start_return):
        #print('target lost :(')
        c_hst.state = HunterState.TARGET_LOST

def _return_to_original_pos(world:esper.World,player_entity:int,c_t:CTransform,c_v:CVelocity,c_hst:CHunterState,c_h:CHunter):
    distance_to_orig =  c_t.pos.distance_to(c_h.pos_origen)
    if(distance_to_orig<=1):
        c_v.vel.x=0
        c_v.vel.y=0
        c_hst.state = HunterState.IDLE
    else:
        c_v.vel.x = c_h.pos_origen.x - c_t.pos.x
        c_v.vel.y = c_h.pos_origen.y - c_t.pos.y
        c_v.vel.scale_to_length(c_h.velocity_return)

     

        
    