from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from actions import Action, MeleeAttack, Movement, Wait
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class BaseAI(Action, BaseComponent):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        cost = np.array(self.entity.g_map.tiles["walk"], dtype=np.int8)

        for e in self.entity.g_map.entities:
            if e.block_movement and cost[e.x, e.y]:
                cost[e.x, e.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        path_finder = tcod.path.Pathfinder(graph)

        path_finder.add_root((self.entity.x, self.entity.y))

        path: List[List[int]] = path_finder.path_to((dest_x, dest_y))[1:].tolist()

        return [(i[0], i[1]) for i in path]


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.g_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAttack(self.entity, dx, dy).perform()
            
            self.path = self.get_path(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return Movement(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y
            ).perform()

        return Wait(self.entity).perform()