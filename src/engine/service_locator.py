
from src.engine.services.images_service import ImageService
from src.engine.services.sounds_service import SoundService



class ServiceLocator:
    images_service = ImageService()
    sounds_service = SoundService()