from components.ai import HostileEnemy
from components.stats import EntityStats
from entity import Actor

player = Actor(
    char="@", 
    color=(255, 255, 255), 
    name="Player", 
    ai_class=HostileEnemy,
    stats=EntityStats(100, 2, 5)
)

rat = Actor(
    char="R", 
    color=(0, 127, 0),
    name="Rat", 
    ai_class=HostileEnemy,
    stats=EntityStats(20, 0, 2)
)

spider = Actor(
    char="M", 
    color=(63, 127, 63), 
    name="Spider", 
    ai_class=HostileEnemy,
    stats=EntityStats(30, 1, 3)
)