#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Low Level Problem — Covalto (esqueleto)
---------------------------------------
Ejecutar por ítem:
    python low_level_problem.py 1   # Item 1: nodo más alcanzable
    python low_level_problem.py 2   # Item 2: caminos a V ordenados por costo
    python low_level_problem.py 3   # Item 3: insertar V' cumpliendo (a) y (b)
    python low_level_problem.py 4   # Item 4: detectar/imprimir imposibilidad de (3.b)
    python low_level_problem.py 5   # Item 5: imprimir inserción de V' en formato de entrada
    python low_level_problem.py 6   # Item 6: insertar V' permitiendo V->V' (flujo exitoso)
"""

from collections import defaultdict, deque

import sys
from typing import Dict, List, Tuple, Iterable, Set

Edge = Tuple[int, int, int]  # (u, v, w)


# Tipos e imports arriba…
from typing import Dict, List, Tuple, Iterable, Set
Edge = Tuple[int, int, int]

# 1) Intenta leer desde edges.py
try:
    from edges import EDGES, SOURCE
except ImportError:
    # 2) Fallback si no existe edges.py
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
    SOURCE = 0

# -----------------------------
# UTILIDADES DE GRAFO
# -----------------------------
def build_graph(edges: Iterable[Edge]):
    """
    Construye lista de adyacencia (salientes) y su reverso (entrantes),
    junto con el conjunto de nodos.
    """
    adj: Dict[int, List[Tuple[int, int]]] = defaultdict(list)   # u -> [(v, w)]
    radj: Dict[int, List[Tuple[int, int]]] = defaultdict(list)  # v -> [(u, w)]
    nodes: Set[int] = set()
    for u, v, w in edges:
        adj[u].append((v, w))
        radj[v].append((u, w))
        nodes.add(u); nodes.add(v)
    # asegurar claves vacías
    for n in list(nodes):
        adj.setdefault(n, [])
        radj.setdefault(n, [])
    return adj, radj, sorted(nodes)


def topo_order(adj: Dict[int, List[Tuple[int, int]]], nodes: Iterable[int]) -> List[int]:
    """
    Orden topológico usando Kahn.
    """
    indeg = {n: 0 for n in nodes}
    for u in nodes:
        for v, _ in adj[u]:
            indeg[v] += 1
    q = deque([n for n in nodes if indeg[n] == 0])
    order: List[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != len(list(nodes)):
        raise ValueError("El grafo no es un DAG (ciclo detectado).")
    return order


def count_paths_from_source(adj: Dict[int, List[Tuple[int, int]]],
                            nodes: Iterable[int],
                            topo: List[int],
                            source: int) -> Dict[int, int]:
    """
    DP sobre orden topológico: ways[v] = número de caminos distintos desde source a v.
    """
    ways = {n: 0 for n in nodes}
    ways[source] = 1
    for u in topo:
        for v, _ in adj[u]:
            ways[v] += ways[u]
    return ways


def enumerate_paths_dfs(adj: Dict[int, List[Tuple[int, int]]],
                        source: int,
                        target: int) -> List[Tuple[List[int], int]]:
    """
    DFS con backtracking: devuelve todos los caminos [nodos] y su costo acumulado.
    """
    paths: List[Tuple[List[int], int]] = []

    def dfs(u: int, acc_cost: int, path: List[int]):
        if u == target:
            paths.append((path.copy(), acc_cost))
            return
        for v, w in adj[u]:
            path.append(v)
            dfs(v, acc_cost + w, path)
            path.pop()

    dfs(source, 0, [source])
    return paths


def neighbors_undirected(adj: Dict[int, List[Tuple[int, int]]],
                         radj: Dict[int, List[Tuple[int, int]]],
                         node: int) -> Set[int]:
    """
    Vecinos (entrantes y salientes) de 'node' (tratado sin dirección).
    """
    outs = {v for v, _ in adj[node]}
    ins = {u for u, _ in radj[node]}
    return outs | ins


def reachable_from_source(adj: Dict[int, List[Tuple[int, int]]], source: int) -> Set[int]:
    """
    Nodos alcanzables desde 'source'
    """
    seen: Set[int] = set()
    stack = [source]
    while stack:
        u = stack.pop()
        if u in seen: 
            continue
        seen.add(u)
        for v, _ in adj[u]:
            if v not in seen:
                stack.append(v)
    return seen



# -----------------------------
# ITEM 1: Vértice más alcanzable desde 0
# -----------------------------
def solve_item1(edges=EDGES, source=SOURCE):
    adj, radj, nodes = build_graph(edges)
    order = topo_order(adj, nodes)
    ways = count_paths_from_source(adj, nodes, order, source)
    V = max(nodes, key=lambda n: ways[n])
    print("ways:", ways)
    print(f"V más alcanzable desde {source}: {V} con {ways[V]} caminos")
    return V, ways, adj, radj, nodes


# -----------------------------
# ITEM 2: Ordenar caminos hacia V por costo (desc)
# -----------------------------
def solve_item2(edges=EDGES, source=SOURCE):
    V, ways, adj, radj, nodes = solve_item1(edges, source)
    paths = enumerate_paths_dfs(adj, source, V)
    paths_sorted = sorted(paths, key=lambda pc: pc[1], reverse=True)
    print(f"\nTotal caminos hacia V={V}: {len(paths_sorted)}")
    for p, c in paths_sorted:
        print(p, "costo =", c)
    return V, ways, adj, radj, nodes, paths_sorted


# -----------------------------
# ITEM 3: Insertar V' cumpliendo (a) y (b)
#   (a) V' es ahora el más alcanzable.
#   (b) Ningún vecino de V comparte arista con V'.
# Estrategia:
#   - Hallar vecinos de V: N(V) = entrantes ∪ salientes.
#   - Nodos permitidos P = alcanzables_desde_source - (N(V) ∪ {V})
#   - Conectar V' desde nodos en P (sólo edges u->V') hasta superar ways[V].
#   - Pesos 0 por simplicidad (no afecta conteo de caminos), y V' como sumidero.
# -----------------------------
# Firma nueva: agrega allow_v_as_parent=False
def propose_V_prime_insertion(edges=EDGES, source=SOURCE, vprime: int = None, allow_v_as_parent: bool = False):
    adj, radj, nodes = build_graph(edges)
    order = topo_order(adj, nodes)
    ways = count_paths_from_source(adj, nodes, order, source)
    V = max(nodes, key=lambda n: ways[n])

    NV = neighbors_undirected(adj, radj, V)
    reach = reachable_from_source(adj, source)

    # 🔁 Línea clave: allowed depende de la política
    if allow_v_as_parent:
        allowed = sorted(reach - NV)          # ✔️ permite V como padre de V'
    else:
        allowed = sorted(reach - NV - {V})    # ❌ política original (estricta)

    cap = sum(ways[u] for u in allowed)
    if cap <= ways[V]:
        return {
            "possible": False,
            "reason": (
                f"No se puede cumplir (3.a) sin violar (3.b): "
                f"suma máxima de caminos desde nodos permitidos ({cap}) "
                f"<= caminos a V ({ways[V]})."
            ),
            "V": V,
            "waysV": ways[V],
            "cap": cap,
            "allowed": allowed,
            "neighborsV": sorted(NV),
        }

    vprime = max(nodes) + 1 if vprime is None else vprime

    pick, acc = [], 0
    for u in sorted(allowed, key=lambda x: ways[x], reverse=True):
        pick.append(u)
        acc += ways[u]
        if acc > ways[V]:
            break

    insertion_edges: List[Edge] = [(u, vprime, 0) for u in pick]

    candidate_edges = edges + insertion_edges
    adj2, radj2, nodes2 = build_graph(candidate_edges)
    order2 = topo_order(adj2, nodes2)
    ways2 = count_paths_from_source(adj2, nodes2, order2, source)
    V2 = max(nodes2, key=lambda n: ways2[n])

    return {
        "possible": True,
        "V": V,
        "waysV": ways[V],
        "V_prime": vprime,
        "waysV_prime": ways2[vprime],
        "becomes_most_reachable": (V2 == vprime),
        "neighborsV": sorted(NV),
        "allowed": allowed,
        "picked_parents_for_V_prime": pick,
        "insertion_edges": insertion_edges,
    }


def solve_item3(edges=EDGES, source=SOURCE):
    result = propose_V_prime_insertion(edges, source)
    if not result["possible"]:
        print(result["reason"])
        print("V:", result["V"], " caminos a V:", result["waysV"])
        print("N(V):", result["neighborsV"])
        print("Permitidos:", result["allowed"])
        print("Capacidad:", result["cap"])
        return result

    print(f"V = {result['V']} con {result['waysV']} caminos")
    print(f"Propuesta V' = {result['V_prime']}  (becomes_most_reachable={result['becomes_most_reachable']})")
    print("Aristas a insertar (u, V', w=0):")
    for e in result["insertion_edges"]:
        print(e)
    print("Padres elegidos:", result["picked_parents_for_V_prime"])
    print("ways[V'] =", result["waysV_prime"])
    return result


# -----------------------------
# ITEM 4: Si (3.b) es imposible, mostrar error explicando por qué
# (Ya cubierto en propose_V_prime_insertion con 'possible=False' y 'reason')
# -----------------------------
def solve_item4(edges=EDGES, source=SOURCE):
    res = propose_V_prime_insertion(edges, source)
    if res["possible"]:
        print("En este grafo, (3.b) SÍ es posible. (Nada que reportar como error.)")
    else:
        print(res["reason"])
    return res


# -----------------------------
# ITEM 5: Imprimir inserción de V' en formato de entrada
# -----------------------------
def solve_item5(edges=EDGES, source=SOURCE):
    res = propose_V_prime_insertion(edges, source)
    if not res["possible"]:
        print(res["reason"])
        return res
    print("Inserción de V' en formato de entrada {u, v, w}:")
    for (u, v, w) in res["insertion_edges"]:
        print(f"{{{u}, {v}, {w}}}")
    return res



def solve_item6(edges=EDGES, source=SOURCE):
    """
    Flujo alternativo: permitir V -> V' para demostrar caso exitoso de inserción.
    """
    res = propose_V_prime_insertion(edges, source, allow_v_as_parent=True)
    if not res["possible"]:
        print(res["reason"])
        return res

    print(f"V = {res['V']} con {res['waysV']} caminos")
    print(f"Propuesta V' = {res['V_prime']}  (becomes_most_reachable={res['becomes_most_reachable']})")
    print("Aristas a insertar (u, V', w=0):")
    for e in res["insertion_edges"]:
        print(e)
    print("Padres elegidos:", res["picked_parents_for_V_prime"])
    print("ways[V'] =", res["waysV_prime"])
    return res

# -----------------------------
# DRIVER
# -----------------------------
def main():
    option = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if option == 1:
        solve_item1()
    elif option == 2:
        solve_item2()
    elif option == 3:
        solve_item3()
    elif option == 4:
        solve_item4()
    elif option == 5:
        solve_item5()
    elif option == 6:
        solve_item6()
    else:
        print("Opción no válida. Usa 1..5")

if __name__ == "__main__":
    main()
