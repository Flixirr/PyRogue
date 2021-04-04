from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        return self.entity.g_map.engine

    def perform(self) -> None:
        raise NotImplementedError()

class Escape(Action):
    def perform(self) -> None:
        raise SystemExit()

class Wait(Action):
    def perform(self) -> None:
        pass

class DirectedAction(Action):
    def __init__(self, entity: Actor, dx:int, dy:int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy
    
    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.engine.g_map.get_blocking_entity(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.g_map.get_actor_loc(*self.dest_xy)

    def perform(self) -> None:
        return NotImplementedError()

class MeleeAttack(DirectedAction):
    def perform(self) -> None:
        target = self.target_actor
        
        if not target:
            return
        
        damage = self.entity.stats._power - target.stats._def

        att_txt = f"{self.entity.name} attacks for {damage}"

        if damage > 0:
            target.stats.hp -= damage
            
        print(att_txt)
        

class Movement(DirectedAction):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.g_map.in_bounds(dest_x, dest_y):
            return 
        if not self.engine.g_map.tiles["walk"][dest_x, dest_y]:
            return
        if self.engine.g_map.get_blocking_entity(dest_x, dest_y):
            return
        
        self.entity.move(self.dx, self.dy)

class Bump(DirectedAction):
    def perform(self):
        if self.target_actor:
            return MeleeAttack(self.entity, self.dx, self.dy).perform()
        else:
            return Movement(self.entity, self.dx, self.dy).perform()