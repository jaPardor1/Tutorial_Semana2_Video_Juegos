import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_texto import CTexto
from src.ecs.components.c_transform import CTransform
def system_show_texts(world:esper.World):
    components = world.get_components(CTexto,CTransform)
    
    c_t:CTexto
    for entidad_texto , (c_t,c_t_r) in components:
       surface = c_t.font.render(c_t.text, True, c_t.color)
       world.add_component(entidad_texto,CSurface.from_surface(surface))
