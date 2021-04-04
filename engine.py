from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions import Escape, Movement
from entity import Entity
from maps import MainMap
from input_handler import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, g_map: MainMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.g_map = g_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        """Method for handling events such as user input in the engine"""
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov()

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

        for entity in self.entities:
            if self.g_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()