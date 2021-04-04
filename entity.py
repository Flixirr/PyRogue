from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.stats import EntityStats
    from maps import MainMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
    Object to represent entities
    """

    g_map: MainMap

    def __init__(
        self,
        g_map: Optional[MainMap] = None,
        x: int = 0, 
        y: int = 0, 
        char: str = " ", 
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        block_movement: bool = False
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.block_movement = block_movement
        if g_map:
            self.g_map = g_map
            g_map.entities.add(self)

    def spawn(self: T, g_map: MainMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.g_map = g_map
        g_map.entities.add(clone)
        return clone

    def place(self, x: int, y: int, g_map: Optional[MainMap] = None) -> None:
        self.x = x
        self.y = y
        if g_map:
            if hasattr(self, "g_map"):
                self.g_map.entities.remove(self)
            self.g_map = g_map
            self.g_map.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

class Actor(Entity):
    def __init__(
        self,
        *, 
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_class: Type[Base],
        stats: EntityStats
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            block_movement=True
        )

        self.ai: Optional[BaseAI] = ai_class(self)
        self.stats = stats
        self.stats.entity = self

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)