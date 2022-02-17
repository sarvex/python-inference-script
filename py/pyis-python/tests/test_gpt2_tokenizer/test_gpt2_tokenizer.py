# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import transformers
import unittest
from pyis.python import ops
import os

class TestBertTokenizer(unittest.TestCase):
    
    def _run_basic_test(self, query):
        self.assertEqual(self.tokenizer.tokenize(query), self.standard.tokenize(query))
    
    def test_tokenize(self):
        self._run_basic_test('hello world')
        self._run_basic_test('a berttokenizer')
        self._run_basic_test('The quick brown fox jumps over the lazy dog.')
        self._run_basic_test('It\'s high noon, isn\'t it?')
        self._run_basic_test('D.Va爱你呦')

    def setUp(self):
        os.makedirs('tmp',511,True)
        self.standard = transformers.GPT2Tokenizer.from_pretrained('gpt2')
        self.standard.save_vocabulary('tmp')
        self.tokenizer = ops.GPT2Tokenizer('tmp/vocab.json', 'tmp/merges.txt')

if __name__ == '__main__':
    unittest.main()