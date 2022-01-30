import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
from modules.open_digraph import *

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


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])
        self.n = node(0, 'a', [], [1])
        self.nn = node(1, 'j', {0:2}, {})
        self.ni = node(0, 'i', {},  {3: 2})
        self.nj = node(2, 'j', {0: 2}, {1: 1})
        self.nk = node(1, 'k', {2:1}, {})
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


class OpenDigraphTest(unittest.TestCase):
    def setUp(self):
        # Noeud mal forme qu'on garde pour les tests
        self.d0 = open_digraph([0], [1], [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {})])
        self.d1 = open_digraph([0], [2], [
            node(0, 'i', {}, {1:1}), 
            node(1, 'j', {0:1}, {2:3}), 
            node(2, 'k', {1:3}, {})])
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
        self.assertEqual(self.d0.inputs, [2])
        self.assertEqual(self.d0.get_node_by_id(2), node(2, 'new', {}, {0:2}))
        self.assertEqual(self.d0.get_node_by_id(0), node(0, 'i', {2:2}, {1:2}))
        self.d0.add_node('new2', {1:7}, {})
        self.assertEqual(self.d0.outputs, [3])
        self.assertEqual(self.d0.get_node_by_id(3), node(3, 'new2', {1:7}, {}))
        self.assertEqual(self.d0.get_node_by_id(1), node(1, 'j', {0:2}, {3:7}))

    def test_remove_edge(self):
        self.d0.remove_edge(0,1)
        self.assertEqual(self.d0.get_node_by_id(0).children, {1:1})
        self.assertEqual(self.d0.get_node_by_id(1).parents, {0:1})
        self.d0.remove_edge(0,1)
        self.assertEqual(self.d0.get_node_by_id(0).children, {})
        self.assertEqual(self.d0.get_node_by_id(1).parents, {})
        self.assertEqual(self.d0.get_input_ids(), [0,1])
        self.assertEqual(self.d0.get_output_ids(), [1,0])

    def test_remove_parallel_edges(self):
        self.d1.remove_parallel_edges(1, 2)
        self.assertEqual(self.d1.get_node_by_id(1).children, {})
        self.assertEqual(self.d1.get_node_by_id(2).parents, {})
        self.assertEqual(self.d1.get_input_ids(), [0, 2])
        self.assertEqual(self.d1.get_output_ids(), [2, 1])
        
    def test_is_well_formed(self):
        self.assertFalse(self.d0.is_well_formed())
        self.assertTrue(self.d2.is_well_formed())
        self.assertFalse(self.d3.is_well_formed())
        



if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run