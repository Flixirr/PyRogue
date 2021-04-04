from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from maps import MainMap
import tile_type

if TYPE_CHECKING:
    from entity import Entity

class RectRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
    
    @property
    def center(self) -> Tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return (center_x, center_y)
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersect(self, other: RectRoom) -> bool:
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def generate_tunnel(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2
    
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
    

def generate_rooms(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity
) -> MainMap:
    """Generate rooms for map"""

    dungeon = MainMap(map_width, map_height)

    rooms: List[RectRoom] = []

    for room in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)
        
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        create_room = RectRoom(x, y, room_width, room_height)

        if any(create_room.intersect(other_room) for other_room in rooms):
            continue

        dungeon.tiles[create_room.inner] = tile_type.floor

        if len(rooms) == 0:
            player.x, player.y = create_room.center
        else:
            for x, y in generate_tunnel(rooms[-1].center, create_room.center):
                dungeon.tiles[x, y] = tile_type.floor
        
        rooms.append(create_room)

    return dungeon
