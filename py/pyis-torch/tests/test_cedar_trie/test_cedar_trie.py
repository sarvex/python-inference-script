#################################################################
#              WARNING: Auto-Generated File
#  This file was generated by a tool(py/pyis-torch/code_gen.py)
#  Any changes made to it will be overwritten when regenerated
#################################################################

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import unittest
from pyis.torch import ops
import os

class TestCedarTrie(unittest.TestCase):
    def test_basic(self):
        trie = ops.CedarTrie()
        trie.insert("Alpha", 1)
        trie.insert("Beta", 2)
        trie.insert("Delta", 3)
        trie.insert("AlphaBeta", 4)
        self.assertEqual(len(trie.predict("Alpha")),2)
        self.assertEqual(len(trie.predict("Gamma")), 0)
        self.assertEqual(trie.numkeys(), 4)
        self.assertEqual(trie.lookup("Alpha"), 1)
        self.assertEqual(trie.lookup("Beta"), 2)
        self.assertEqual(trie.lookup("Delta"), 3)
        self.assertEqual(trie.lookup("AlphaBeta"), 4)
        
        self.assertRaises(RuntimeError, trie.lookup, "Gamma")

        trie.insert("Gamma", 5)
        trie.insert("Lambda", 6)
        trie.insert("Alpha", 7)
        
        self.assertEqual(trie.numkeys(), 6)
        self.assertEqual(trie.lookup("Alpha"), 7)
        
        trie.erase("Gamma")
        
        self.assertRaises(RuntimeError, trie.lookup, "Gamma")

        self.assertEqual(trie.lookup("Lambda"), 6)

        trie.insert('Sentence with Space and\tTabs', 8)
        self.assertEqual(trie.lookup('Sentence with Space and\tTabs'), 8)
        self.assertEqual(len(trie.predict("Sentence ")),1)
        
        trie.insert("   ", 9)
        trie.insert("  \t", 10)
        trie.insert("\t ", 11)
        self.assertEqual(len(trie.predict(" ")),2)
        self.assertEqual(trie.lookup("\t "), 11)

        os.makedirs('tmp',511,True)

        trie.save('tmp/trie.bin')

        trie2 = ops.CedarTrie()
        trie2.load('tmp/trie.bin')
        
        self.assertEqual(trie.items(), trie2.items())


if __name__ == "__main__":
    unittest.main()
