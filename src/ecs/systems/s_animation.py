
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(world:esper.World,delta_time:float):
    
    components = world.get_components(CSurface,CAnimation)
    # disminuir el valor del current time de la animacion
    for _ , (c_s,c_a) in components:
        c_a.current_animation_time -= delta_time
        # si el current time es menor o igual que 0 , cambio de frame
        if(c_a.current_animation_time <=0):
            # restaurar el tiempo 
            c_a.current_animation_time = c_a.animations_list[c_a.current_animation].framerate
            c_a.current_frame +=1# cambio de frame
            #Limitar el frame con sus propiedades de start y end
            if c_a.current_frame > c_a.animations_list[c_a.current_animation].end:
                c_a.current_frame = c_a.animations_list[c_a.current_animation].start
            # calcular la nueva subarea del rectangulo de sprite
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.current_frame