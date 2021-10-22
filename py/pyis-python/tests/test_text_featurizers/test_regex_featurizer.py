# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import unittest, os
from pyis.python import ops
from pyis.python import save


class TestRegexFeaturizer(unittest.TestCase):
    def test_run(self):
        featurizer = ops.RegexFeaturizer(['\d+', r'\d+:\d+'])
        features = featurizer.transform(['the', 'answer', 'is', '42'])
        self.assertTrue(len(features), 1)
        self.assertEqual(features[0].id(), 0)
        self.assertEqual(features[0].pos(), (3, 3))

        features = featurizer.transform(['set', 'an', 'alarm', 'at', '7:00', 'tomorrow'])
        self.assertTrue(len(features), 1)
        self.assertEqual(features[0].id(), 1)
        self.assertEqual(features[0].pos(), (4, 4))
        

if __name__ == "__main__":
    unittest.main()