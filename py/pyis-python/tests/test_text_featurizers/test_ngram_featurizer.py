# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import unittest, os
from pyis.python import ops
from pyis.python import save


class TestNGramFeaturizer(unittest.TestCase):
    def test_run(self):
        featurizer = ops.NGramFeaturizer(2, True)
        featurizer.fit(['the', 'answer', 'is', '42'])
        features = featurizer.transform(['the', 'answer', 'is', '42'])
        self.assertEqual(len(features), 5)
        self.assertEqual((features[0].id(), features[0].pos()), (0, (0, 1)))
        self.assertEqual((features[1].id(), features[1].pos()), (1, (0, 1)))
        self.assertEqual((features[2].id(), features[2].pos()), (2, (1, 2)))
        self.assertEqual((features[3].id(), features[3].pos()), (3, (2, 3)))
        self.assertEqual((features[4].id(), features[4].pos()), (4, (2, 3)))
        

if __name__ == "__main__":
    unittest.main()