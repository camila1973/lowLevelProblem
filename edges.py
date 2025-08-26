
from typing import List, Tuple

Edge = Tuple[int, int, int]  # (u, v, w)

# Grafo del enunciado
EDGES: List[Edge] = [
    (0, 1, 2),
    (0, 2, 4),
    (0, 4, -2),
    (0, 5, 1),
    (0, 6, 5),
    (2, 3, 3),
    (2, 4, 2),
    (3, 8, -4),
    (4, 3, 5),
    (4, 8, 1),
    (4, 7, 2),
    (5, 7, -1),
    (5, 8, -3),
    (6, 7, 6),
    (7, 8, 2),
]
SOURCE: int = 0
