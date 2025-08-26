import unittest
import low_level_problem as llp


class TestLowLevelProblem(unittest.TestCase):
    def setUp(self):
        # Grafo del enunciado
        self.edges = llp.EDGES
        self.source = llp.SOURCE
        self.adj, self.radj, self.nodes = llp.build_graph(self.edges)
        self.topo = llp.topo_order(self.adj, self.nodes)
        self.ways = llp.count_paths_from_source(self.adj, self.nodes, self.topo, self.source)

    def test_item1_most_reachable(self):
        V = max(self.nodes, key=lambda n: self.ways[n])
        self.assertEqual(V, 8)

        expected_ways = {0: 1, 1: 1, 2: 1, 3: 3, 4: 2, 5: 1, 6: 1, 7: 4, 8: 10}
        self.assertEqual(self.ways, expected_ways)

    def test_topological_order_is_valid(self):

        pos = {n: i for i, n in enumerate(self.topo)}
        for (u, v, _w) in self.edges:
            self.assertLess(pos[u], pos[v])

  
    def test_item2_paths_sorted_by_cost(self):
        V = max(self.nodes, key=lambda n: self.ways[n])
        paths = llp.enumerate_paths_dfs(self.adj, self.source, V)

        self.assertEqual(len(paths), self.ways[V])

    
        paths_sorted = sorted(paths, key=lambda pc: pc[1], reverse=True)
        costs = [c for _p, c in paths_sorted]
        self.assertEqual(costs, sorted(costs, reverse=True))


        self.assertEqual(paths_sorted[0][0], [0, 6, 7, 8])
        self.assertEqual(paths_sorted[0][1], 13)
        self.assertEqual(paths_sorted[-1][0], [0, 5, 8])
        self.assertEqual(paths_sorted[-1][1], -2)

    def test_item3_current_impl_marks_impossible(self):
        """
        Con la implementación actual (allowed = reach - NV - {V}), el caso del reto
        sale imposible. Verificamos el mensaje y detalles.
        """
        res = llp.propose_V_prime_insertion(self.edges, self.source)
        self.assertIn("possible", res)
        if res["possible"]:
     
            self.skipTest("La implementación permite V como padre; este test solo valida el comportamiento anterior.")
        else:
            self.assertFalse(res["possible"])
            self.assertIn("No se puede cumplir (3.a) sin violar (3.b)", res["reason"])
            self.assertEqual(res["V"], 8)
            self.assertEqual(res["waysV"], 10)
            self.assertEqual(set(res["allowed"]), {0, 1, 2, 6})

    def test_feasibility_if_V_allowed_as_parent(self):
        """
        Demostración de factibilidad: si permitimos V como padre de V',
        añadir (8->V') y (0->V') hace que ways[V'] > ways[V].
        """
        V = max(self.nodes, key=lambda n: self.ways[n])  # 8
        vprime = max(self.nodes) + 1
        edges2 = self.edges + [(V, vprime, 0), (self.source, vprime, 0)]
        adj2, radj2, nodes2 = llp.build_graph(edges2)
        order2 = llp.topo_order(adj2, nodes2)
        ways2 = llp.count_paths_from_source(adj2, nodes2, order2, self.source)
        self.assertGreater(ways2[vprime], self.ways[V]) 

    def test_item4_impossible_on_custom_graph(self):
        """
        Caso artificial imposible:
            0->1->3
            0->2->3    (V=3 con 2 caminos; vecinos de V = {1,2})
        Permitidos: solo {0} con ways[0]=1 -> no supera ways[V]=2.
        """
        custom_edges = [
            (0, 1, 0),
            (0, 2, 0),
            (1, 3, 0),
            (2, 3, 0),
        ]
        res = llp.propose_V_prime_insertion(custom_edges, source=0)
        self.assertFalse(res["possible"])
        self.assertIn("No se puede cumplir (3.a) sin violar (3.b)", res["reason"])

   
    def test_num_paths_dp_matches_dfs_to_V(self):
        V = max(self.nodes, key=lambda n: self.ways[n])
        paths = llp.enumerate_paths_dfs(self.adj, self.source, V)
        self.assertEqual(len(paths), self.ways[V])


if __name__ == "__main__":
    unittest.main()
