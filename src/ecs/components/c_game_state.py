from enum import Enum


class CGameState:
    def __init__(self) -> None:
        self.state = GameState.PLAYING

class GameState(Enum):
    PLAYING = 0
    PAUSED = 1
    

