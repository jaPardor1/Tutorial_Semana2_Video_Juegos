from enum import Enum


class CTagAbility():
    def __init__(self) -> None:
        self.state=AbilityState.FULL

class AbilityState(Enum):
    FULL = 0
    CHARGING = 1