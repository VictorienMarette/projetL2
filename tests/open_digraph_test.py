import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *

class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)

    def test_init_open_digraph(self):
        d0 = open_digraph([0], [1], [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {})])
        self.assertEqual(d0.inputs, [0])
        self.assertEqual(d0.outputs, [1])
        self.assertEqual(d0.nodes, {0: node(0, 'i', {}, {1:2}), 1: node(1, 'j', {0:2}, {})})
        self.assertIsInstance(d0, open_digraph)
        self.assertEqual(d0.lastNewId, 1)

    def test_init_bool_circ(self):
        dref = open_digraph([0], [1], [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {})])
        d0 = bool_circ(dref)
        self.assertEqual(d0.inputs, [0])
        self.assertEqual(d0.outputs, [1])
        self.assertEqual(d0.nodes, {0: node(0, 'i', {}, {1:2}), 1: node(1, 'j', {0:2}, {})})
        self.assertIsInstance(d0, open_digraph)
        self.assertEqual(d0.lastNewId, 1)
        


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])
        self.n = node(0, 'a', [], [1])
        self.nn = node(1, 'j', {0:2}, {})
        self.ni = node(0, 'i', {},  {3: 2})
        self.nj = node(2, 'j', {0: 2}, {1: 1})
        self.nk = node(1, 'k', {2:1}, {})
        self.graph = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1}),
                    node(1, 'i1', {}, {3:1}),
                    node(2, 'n2', {0:1}, {3:2}),
                    node(3, 'n3', {1:1, 2:2}, {4:1}),
                    node(4, 'o4', {3: 1}, {})]
                    )

    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')
    def test_copy(self):
        self.assertIsNot(self.n.copy(), self.n)
        self.assertIsNot(self.nn.copy(), self.nn)
    def test_isDirectParentsChildren(self):
        self.assertTrue(self.nj.isDirectChild(0))
        self.assertTrue(self.nj.isDirectParent(1))
        self.assertFalse(self.nk.isDirectChild(0))
    def test_remove_parent_once_child_once_parent_id_child_id(self):
        self.nj.remove_parent_once(0)
        self.ni.remove_child_once(3)
        self.nk.remove_child_id(2)
        self.nj.remove_child_id(1)
        self.nj.remove_child_id(2)
        self.assertTrue(self.nj.parents == {0:1})
        self.assertTrue(self.ni.children == {3:1})
        self.assertTrue(self.nk.children == {})
        self.assertTrue(self.nj.children == {})
        self.nj.remove_parent_once(0)
        self.assertTrue(self.nj.parents == {})


    # Les getters et setters sont assez simples pour
    # ne pas avoir a les tester

    def test_three_degree_function(self):
        theNode2 = self.graph.get_node_by_id(2)
        theNode3 = self.graph.get_node_by_id(3)
        self.assertEqual(theNode2.outdegree(), 2)
        self.assertEqual(theNode3.indegree(), 3)
        self.assertEqual(theNode2.degree(), 3)
        self.assertEqual(theNode3.degree(), 4)

class OpenDigraphTest(unittest.TestCase):
    def setUp(self):
        # Noeud mal forme qu'on garde pour les tests
        self.d0 = open_digraph([0], [1], [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {})])
        self.d1 = open_digraph([0], [2], [
            node(0, 'i', {}, {1:1}), 
            node(1, 'j', {0:1}, {2:1}), 
            node(2, 'k', {1:1}, {})])
        self.d2 = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1}),
                    node(1, 'i1', {}, {3:1}),
                    node(2, 'n2', {0:1}, {3:2}),
                    node(3, 'n3', {1:1, 2:2}, {4:1}),
                    node(4, 'o4', {3: 1}, {})]
                    )
        self.d3 = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1}),
                    node(1, 'i1', {}, {3:1}),
                    node(2, 'n2', {0:1}, {3:2}),
                    node(3, 'n3', {1:1, 2:3}, {4:1}),
                    node(4, 'o4', {3: 1}, {})]
                    )
        self.d4 = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1}),
                    node(1, 'i1', {}, {2:1}),
                    node(2, 'n2', {0:1, 1:1}, {3:2}),
                    node(3, 'n3', {2:2}, {5:1}),
                    node(5, 'n4', {3:1}, {4:1}),
                    node(4, 'o4', {5: 1}, {})]
                    )
        self.d5 = open_digraph([0, 1], [4], [
                    node(0, 'luffy', {4:1}, {1:1, 5:1}),
                    node(1, 'saitema', {0:1}, {2:1}),
                    node(2, 'naruto', {1:1}, {3:1}),
                    node(3, 'spike', {2:1}, {4:1}),
                    node(4, 'major', {4:1}, {0:1}),
                    node(5, 'tintin', {0: 1}, {})]
                    )

        self.g = open_digraph([0,1,2], [8], [
                    node(0, 'x1', {}, {3:1}),
                    node(1, 'x2', {}, {4:1}),
                    node(2, 'x3', {}, {5:1}),
                    node(3, '&', {0:1, 4:1}, {7:1}),
                    node(4, '', {1:1}, {3:1, 5:1}),
                    node(5, '|', {2:1, 4:1}, {6:1}),
                    node(6, '~', {5:1}, {7:1}),
                    node(7, '|', {3:1, 6:1}, {8:1}),
                    node(8, 'out', {7:1}, {})])

        self.d = d = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1,5:1}),
                    node(1, 'i1', {}, {2:1}),
                    node(2, 'n2', {0:1, 1:1}, {3:2}),
                    node(3, 'n3', {2:2}, {5:1}),
                    node(5, 'n4', {3:1,0:1}, {4:1}),
                    node(4, 'o4', {5: 1}, {})]
                    )

    # Tests des getters
    def test_get_inputs(self):
        self.assertEqual(self.d0.get_input_ids(), [0])
    def test_get_outputs(self):
        self.assertEqual(self.d0.get_output_ids(), [1])
    def test_get_node_map(self):
        self.assertEqual(self.d0.get_id_node_map()[0], node(0, 'i', {}, {1:2}))
        self.assertEqual(self.d0.get_id_node_map()[1], node(1, 'j', {0:2}, {}) )
    def test_get_nodes(self):
        self.assertEqual(list(self.d0.get_nodes()), [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {})])
    def test_get_node_ids(self):
        self.assertEqual(self.d0.get_node_ids(), [0, 1])
    def test_get_node_by_id(self):
        self.assertEqual(self.d0.get_node_by_id(1), node(1, 'j', {0:2}, {}))
        
    def test_copy(self):
        d = open_digraph([0], [2], [node(0, 'i0', {}, {2:1}), node(2, 's', {0:1}, {})])
        self.assertIsNot(d.copy(), d)

    def test_NewId(self):
        self.assertIsNot(self.d0.new_id(), 0)
        self.assertIsNot(self.d0.new_id(), 1)

    def test_add_edge(self):
        self.d0.add_edge(0, 1)
        self.assertEqual(self.d0.get_node_by_id(0), node(0, 'i', {}, {1:3}))
        self.assertEqual(self.d0.get_node_by_id(1), node(1, 'j', {0:3}, {}))
        self.d0 = open_digraph([0], [2], [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {2:1}), node(2, 'k', {1:1}, {})])
        self.d0.add_edge(0, 2)
        self.assertEqual(self.d0.get_node_by_id(0), node(0, 'i', {}, {1:2, 2:1}))
        self.assertEqual(self.d0.get_node_by_id(2), node(2, 'k', {1:1, 0:1}, {}))

    def test_add_node(self):
        self.d0.add_node('new', {}, {0:2})
        self.assertEqual(self.d0.get_node_by_id(2), node(2, 'new', {}, {0:2}))
        self.assertEqual(self.d0.get_node_by_id(0), node(0, 'i', {2:2}, {1:2}))
        self.d0.add_node('new2', {1:7}, {})
        self.assertEqual(self.d0.get_node_by_id(3), node(3, 'new2', {1:7}, {}))
        self.assertEqual(self.d0.get_node_by_id(1), node(1, 'j', {0:2}, {3:7}))

        self.d1.add_node('new2', {1:2}, {1:2})
        self.assertEqual(self.d1.get_node_by_id(3).parents[1], 2)
        self.assertEqual(self.d1.get_node_by_id(3).children[1], 2)
        self.assertTrue(self.d1.is_well_formed())

    def test_remove_edge(self):
        self.d2.remove_edge(2,3)
        self.assertEqual(self.d2.get_node_by_id(2).get_children_ids(), [3])
        self.assertEqual(self.d2.get_node_by_id(2).children[3], 1)
        self.assertEqual(self.d2.get_node_by_id(3).get_parent_ids(), [1,2])
        self.assertEqual(self.d2.get_node_by_id(3).parents[2], 1)
        self.assertTrue(self.d2.is_well_formed())
        self.d2.remove_edge(2,3)
        self.assertEqual(self.d2.get_node_by_id(2).get_children_ids(), [])
        self.assertEqual(self.d2.get_node_by_id(3).get_parent_ids(), [1])
        self.assertTrue(self.d2.is_well_formed())

    
    def test_remove_parallel_edges(self):
        self.d2.remove_parallel_edges(2,3)
        self.assertEqual(self.d2.get_node_by_id(2).get_children_ids(), [])
        self.assertEqual(self.d2.get_node_by_id(3).get_parent_ids(), [1])
        self.assertTrue(self.d2.is_well_formed())
  
    def test_remove_node_by_id(self):
        self.d4.remove_node_by_id(3)
        self.assertEqual(self.d4.get_node_by_id(2).get_children_ids(), [])
        self.assertEqual(self.d4.get_node_by_id(5).get_parent_ids(), [])
        self.assertTrue(self.d4.is_well_formed())

        
    def test_is_well_formed(self):
        self.assertFalse(self.d0.is_well_formed())
        self.assertTrue(self.d2.is_well_formed())
        self.assertFalse(self.d3.is_well_formed())
        self.assertTrue(self.d4.is_well_formed())

    def test_add_input_output_node(self):
        self.d1.add_input_node('newInput', 1)
        self.assertEqual(self.d1.get_input_ids(), [0, 3])
        self.assertEqual(self.d1.get_node_by_id(1).parents[3], 1)
        self.assertTrue(self.d1.is_well_formed())
        self.d1.add_output_nodes('newOutput', 1)
        self.assertEqual(self.d1.get_output_ids(), [2, 4])
        self.assertEqual(self.d1.get_node_by_id(1).children[4], 1)
        self.assertTrue(self.d1.is_well_formed())

    def test_is_cyclic(self):
        self.assertTrue(self.d5.is_cyclic())
        self.assertFalse(self.d4.is_cyclic())

    def test_max_min_id(self):
        self.assertEqual(self.d1.max_id(), 2)
        self.assertEqual(self.d1.min_id(), 0)

    def test_shift_indice(self):
        self.assertTrue(self.d1.is_well_formed())
        self.d1.shift_indices(3)
        self.assertEqual(self.d1.get_input_ids(), [3])
        self.assertEqual(self.d1.get_output_ids(), [5])
        self.assertEqual(sorted(self.d1.get_node_ids()), [3, 4, 5])
        self.assertEqual(self.d1.get_node_by_id(4).children, {5:1})
        self.assertEqual(self.d1.get_node_by_id(4).parents, {3:1})
        self.assertTrue(self.d1.is_well_formed())

    def test_iparallele(self):
        self.d1.iparallel([self.d1])
        self.assertEqual(self.d1.get_input_ids(), [0, 3])
        self.assertEqual(self.d1.get_output_ids(), [2, 5])
        self.assertEqual(sorted(self.d1.get_node_ids()), [0, 1, 2, 3, 4, 5])
        self.assertTrue(self.d1.is_well_formed())
    
    def test_paralle_get_connected_components(self):
        a = self.d2.copy()
        b = self.d2.copy()
        c = self.d2.copy()
        d = self.d2.parallel([a,b,c])
        n, dic = d.connected_components()
        self.assertEqual(n,4)
        l = d.get_connected_components()
        for i in range(4):
            self.assertEqual(len(l[i].get_node_ids()),5)
            self.assertEqual(len(l[i].inputs),2)
            self.assertEqual(len(l[i].outputs),1)

    def test_Dijkstra(self):
        d, p = self.g.Dijkstra(4)
        self.assertEqual(d[4], 0)
        self.assertEqual(d[3], 1)
        self.assertEqual(d[0], 2)
        self.assertEqual(d[8], 3)
        self.assertEqual(d[7], 2)
        self.assertEqual(p[3], 4)
        self.assertEqual(p[0], 3)
        self.assertEqual(p[8], 7)
        self.assertEqual(p[7], 3)
        d, p = self.g.Dijkstra(4, direction=1)
        self.assertFalse(0 in d)
        self.assertFalse(1 in d)
        self.assertFalse(1 in p)
        self.assertFalse(2 in p)
        self.assertEqual(d[8], 3)
        self.assertEqual(p[7], 3)
        self.assertFalse(4 in p)
        self.assertFalse(4 in d)
        d, p = self.g.Dijkstra(6, direction=-1)
        self.assertFalse(7 in d)
        self.assertTrue(5 in d)
        self.assertFalse(8 in p)
        self.assertEqual(d[1], 3)
        self.assertEqual(p[2], 5)
        self.assertFalse(6 in p)
        self.assertFalse(6 in d)

    def test_shortest_Path(self):
        p = self.g.shortest_path(1, 8)
        self.assertEqual(p, [1, 4, 3, 7, 8])
        p = self.g.shortest_path(8, 2)
        self.assertEqual(p, [8, 7, 6, 5, 2])

    def test_chemin_plus_cours_ancetre_commun(self):
        p = self.g.chemin_plus_cours_ancetre_commun(6, 3)
        self.assertEqual(p[1], (3, 2))
        self.assertEqual(p[4], (2, 1))
        self.assertEqual(len(p), 2)
        p = self.g.chemin_plus_cours_ancetre_commun(3, 7)
        self.assertEqual(p[0], (1, 2))
        self.assertEqual(p[1], (2, 3))
        self.assertEqual(p[4], (1, 2))
        self.assertEqual(len(p), 3)

    def test_tri_topologique(self):
        t = self.d4.tri_topologique()
        for l in t:
            l.sort()
        self.assertEqual(self.d4.tri_topologique(), [[0,1],[2],[3],[5], [4]])
        t = self.g.tri_topologique()
        for l in t:
            l.sort()
        self.assertEqual(t, [[0, 1, 2], [4], [3, 5], [6], [7], [8]])
    
    def test_profondeur_graph_profondeur_noeud(self):
        d = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1,5:1}),
                    node(1, 'i1', {}, {2:1}),
                    node(2, 'n2', {0:1, 1:1}, {3:2}),
                    node(3, 'n3', {2:2}, {5:1}),
                    node(5, 'n4', {3:1,0:1}, {4:1}),
                    node(4, 'o4', {5: 1}, {})]
                    )
        self.assertEqual(d.profondeur_graph(), 4)
        self.assertEqual(d.profondeur_noeud(4), 4)


    def test_distances_la_plus_longue(self):
        d = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1,5:1}),
                    node(1, 'i1', {}, {2:1}),
                    node(2, 'n2', {0:1, 1:1}, {3:2}),
                    node(3, 'n3', {2:2}, {5:1}),
                    node(5, 'n4', {3:1,0:1}, {4:1}),
                    node(4, 'o4', {5: 1}, {})]
                    )
        a, b = self.d.distances_la_plus_longue(0,4)
        self.assertEqual(a, 4)
        self.assertEqual(b, [0, 2, 3, 5, 4])
        a, b = self.d.distances_la_plus_longue(0,5)
        self.assertEqual(a, 3)
        self.assertEqual(b, [0, 2, 3, 5])

    def test_fusion(self):
        self.d4.fusion_deux_noeud(3,4)
        self.assertEqual(self.d4.get_node_by_id(3).parents, {2:2,5: 1})
        self.assertEqual(self.d4.get_node_by_id(3).children, {5:1})

        
class matriceTest(unittest.TestCase):
    def setUp(self):
        self.strTab = [
            "free",
            "DAG",
            "oriented",
            "loop-free",
            "undirected",
            "loop-free undirected"
        ]
        self.t = [random_int_matrix(10, 4),
        random_oriented_int_matrix(10, 4),
        random_symetric_int_matrix(10, 4),
        random_triangular_int_matrix(10, 4)]

    def test_generated_matrix(self):
        for m in self.t:
            self.assertEqual(len(m), 10)
            for l in m:
                self.assertEqual(len(m), 10)
                for i in l:
                    self.assertTrue(i in [0, 1, 2, 3])
                    
    def test_random(self):
        for s in self.strTab:
            self.assertTrue(open_digraph.random(10, 4, 2, 3, form=s).is_well_formed())

class bool_circTest(unittest.TestCase):
    def setUp(self):
        self.circ = bool_circ(open_digraph([0, 1, 2], [8], [node(0, 'x1', {}, {3:1}),
                             node(1, 'x2', {}, {4:1}),
                             node(2, 'x3', {}, {5:1}),
                             node(3, '&', {0:1, 4:1}, {7:1}),
                             node(4, '', {1:1}, {3:1, 5:1}),
                             node(5, '|', {2:1, 4:1}, {6:1}),
                             node(6, '~', {5:1}, {7:1}),
                             node(7, '|', {3:1, 6:1}, {8:1}),
                             node(8, 'out', {7:1}, {})]))

        self.d3 = bool_circ(open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1}),
                    node(1, 'i1', {}, {3:1}),
                    node(2, '|', {0:1}, {3:2}),
                    node(3, '&', {1:1, 2:3}, {4:1}),
                    node(4, 'o4', {3: 1}, {})]))

        self.add = bool_circ.Adder(1)

    def test_is_well_formed(self):
        self.assertTrue(self.circ.is_well_formed())
        self.assertFalse(self.d3.is_well_formed())
        
    def test_regle_evaluate(self):
        # decommenter pour voir l'affichage
        t = self.add
        t.get_node_by_id(25).set_label("0")
        t.get_node_by_id(26).set_label("1")
        t.display()
        t.evaluate()
        t.display()

    



if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run

#python3 -m unittest discover tests "*_test.py"