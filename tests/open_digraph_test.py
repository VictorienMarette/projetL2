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
        d0 = open_digraph([2, 3, 1], [4, 9, 0], [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {})])
        self.assertEqual(d0.inputs, [2, 3, 1])
        self.assertEqual(d0.outputs, [4, 9, 0])
        self.assertEqual(d0.nodes, {0: node(0, 'i', {}, {1:2}), 1: node(1, 'j', {0:2}, {})})
        self.assertIsInstance(d0, open_digraph)


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')
    def test_copy(self):
        n = node(0, 'a', [], [1])
        nn = node(1, 'j', {0:2}, {})
        self.assertIsNot(n.copy(), n)
        self.assertIsNot(nn.copy(), nn)


class OpenDigraphTest(unittest.TestCase):
    def setUp(self):
        self.d0 = open_digraph([2, 3, 1], [4, 9, 0], [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {})])
    def test_get_inputs(self):
        self.assertEqual(self.d0.inputs, [2, 3, 1],)
    def test_get_outputs(self):
        self.assertEqual(self.d0.outputs, [4, 9, 0])
        
        
    def test_copy(self):
        d = open_digraph([0], [2], [node(0, 'i0', {}, {2:1}), node(2, 's', {0:1}, {})])
        self.assertIsNot(d.copy(), d)


if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run