from enum import Enum


class CHunterState:
    def __init__(self) -> None:
        self.state = HunterState.IDLE

class HunterState(Enum):
    IDLE = 0
    CHASING = 1
    TARGET_LOST =2

