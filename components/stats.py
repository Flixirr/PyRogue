from components.base_component import BaseComponent

class EntityStats(BaseComponent):
    def __init__(self, s_hp: int, s_def: int, s_power: int):
        self.max_hp = s_hp
        self._hp = s_hp
        self._def = s_def
        self._power = s_power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, val: int) -> None:
        self._hp = max(0, min(val, self.max_hp))