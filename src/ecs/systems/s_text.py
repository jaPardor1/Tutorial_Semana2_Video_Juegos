import esper
from src.ecs.components.c_texto import Ctexto
def system_show_texts(world:esper.World):
    components = world.get_components(Ctexto)

    for entidad_texto , (c_t) in components:
        