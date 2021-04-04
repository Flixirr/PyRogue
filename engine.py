from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov


from input_handler import MainGameEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from maps import MainMap
    from input_handler import EventHandler

class Engine:
    g_map: MainMap


    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.g_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        self.g_map.visible[:] = compute_fov(
            self.g_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )

        self.g_map.explored |= self.g_map.visible

    def render(self, console: Console, context: Context) -> None:
        """Method for rendering objects in TCOD terminal"""
        self.g_map.render(console)

        console.print(x=1, y=47,
                        string=f"HP: {self.player.stats.hp}/{self.player.stats.max_hp}")

        context.present(console)

        console.clear()