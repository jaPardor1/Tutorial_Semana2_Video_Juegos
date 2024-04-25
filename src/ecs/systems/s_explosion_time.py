
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_tiempo_vida import CTiempoVida
from src.ecs.components.tags.c_tag_explosion import CTagExplosion

def system_explosion_time(world:esper):
    explosiones = world.get_components(CAnimation,CTagExplosion)
    c_a:CAnimation
    for explosion_entity , (c_a,_) in explosiones:
        if c_a.current_frame == c_a.animations_list[c_a.current_animation].end:
            world.delete_entity(explosion_entity)


    # for explosion ,(c_t_e,c_t_v) in explosiones:
    #     c_t_v.tiempo_vida -=1
    #     if c_t_v.tiempo_vida==0 :
    #         world.delete_entity(explosion)

