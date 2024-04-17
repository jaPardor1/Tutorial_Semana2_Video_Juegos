import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_limit_bullet_amount(world:esper.World,bullet_max_limit:int):
    bullet_components=world.get_components(CSurface,CTransform,CTagBullet)
    
    print(str(len(bullet_components)) +'/'+str(bullet_max_limit))
    
    if len(bullet_components) > bullet_max_limit:
         last_bullet = None
         for bullet_entity ,(b_s,b_t,_) in bullet_components:
             last_bullet=bullet_entity  

         world.delete_entity(last_bullet)
    
            
            


