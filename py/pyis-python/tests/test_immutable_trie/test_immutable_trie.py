# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import os
import unittest
from pyis.python import ops

class TestImmutableTrie(unittest.TestCase):
    def setUp(self) -> None:
        os.makedirs('tmp', exist_ok=True)

    def test_basic(self):
        data = [('Alpha', 1), ('Beta', 2), ('Delta', 3), ('AlphaBeta', 4)]
        ops.ImmutableTrie.compile(data, 'tmp/trie.bin')
        trie = ops.ImmutableTrie()
        trie.load('tmp/trie.bin')
        self.assertSetEqual(set(data), set(trie.items()))
        self.assertEqual(1, trie.lookup('Alpha'))
        self.assertEqual(2, trie.lookup('Beta'))
        self.assertEqual(4, trie.lookup('AlphaBeta'))
        with self.assertRaises(RuntimeError):
            trie.lookup('NonExists')

if __name__ == "__main__":
    unittest.main()
