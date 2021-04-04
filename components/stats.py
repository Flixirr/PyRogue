from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from input_handler import GameOverEventHandler
from rendering_help import Order

if TYPE_CHECKING:
    from entity import Actor

class EntityStats(BaseComponent):
    entity: Actor

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
        if self._hp == 0:
            self.die()
    
    def die(self) -> None:
        if self.entity is self.engine.player:
            self.engine.event_handler = GameOverEventHandler(self.engine)
        message = f"{self.entity.name} died!"

        self.entity.char = "#"
        self.entity.color = (150, 0, 0)
        self.entity.block_movement = False
        self.entity.ai = None
        self.entity.name = f"remains of {self.entity.name}"
        self.r_order = Order.CORPSE

        print(message)