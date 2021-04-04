from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32), #character to represent tile
        ("fg", "3B"), #foreground
        ("bg", "3B"), #background
    ]
)

tile_dt = np.dtype(
    [
        ("walk", bool),
        ("transparent", bool),
        ("color_dark", graphic_dt),
        ("color_light", graphic_dt)
    ]
)

def new_tile(
    *, #keywords
    walk: int,
    transparent: int,
    color_dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    color_light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    return np.array((walk, transparent, color_dark, color_light), dtype=tile_dt)

fog_of_war = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walk=True,
    transparent=True,
    color_dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    color_light=(ord(" "), (255, 255, 255), (200, 180, 50))
)

wall = new_tile(
    walk=False,
    transparent=False,
    color_dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    color_light=(ord(" "), (255, 255, 255), (130, 110, 50))
)
