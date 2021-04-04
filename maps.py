from __future__ import annotations

import numpy as np
from tcod.console import Console

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import tile_type

from entity import Actor

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine

class MainMap:
    def __init__(self, engine:Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.engine = engine
        self.tiles = np.full((width, height), fill_value=tile_type.wall, order="F")
        self.entities = set(entities)

        self.visible = np.full(
            (width, height), 
            fill_value=False,
             order="F"
             )

        self.explored = np.full(
            (width, height), 
            fill_value=False, 
            order="F"
            )

    @property
    def actors(self) -> Iterator[Actor]:
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )
    
    def get_blocking_entity(self, location_x: int, location_y: int) -> Optional[Entity]:
        for e in self.entities:
            if e.block_movement and e.x == location_x and e.y == location_y:
                return e
        
        return None

    def get_actor_loc(self, x: int, y: int) -> Optional[Actor]:
        for a in self.actors:
            if a.x == x and a.y == y:
                return a
        
        return None

    def in_bounds(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["color_light"], self.tiles["color_dark"]],
            default=tile_type.fog_of_war,
        )

        
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)