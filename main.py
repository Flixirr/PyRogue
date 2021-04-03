#!/usr/bin/env python3
import tcod
from actions import Escape, Movement
from input_handler import EventHandler
from entity import Entity

def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(screen_width // 2, screen_height // 2, "P", (255, 255, 255))
    npc = Entity(screen_width // 2 - 5, screen_height // 2 - 5, "N", (255, 255, 0))
    entities = {npc, player}

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F") #order=F sets numpy arrays access to [x,y]
        while True:
            root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)
            
            context.present(root_console)

            root_console.clear()

            for event in tcod.event.wait(): 
                action = event_handler.dispatch(event)

                if action is None:
                    continue
                
                if isinstance(action, Movement):
                    player.move(dx=action.dx, dy=action.dy)

                elif isinstance(action, Escape):
                    raise SystemExit()

if __name__ == "__main__":
    main()#!/usr/bin/env python3
import tcod


def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=1, y=1, string="@")
            
            context.present(root_console)

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()


if __name__ == "__main__":
    main()