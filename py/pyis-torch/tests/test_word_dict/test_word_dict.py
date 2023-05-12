#################################################################
#              WARNING: Auto-Generated File
#  This file was generated by a tool(py/pyis-torch/code_gen.py)
#  Any changes made to it will be overwritten when regenerated
#################################################################

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import unittest
import os
from pyis.torch import save, load
from pyis.torch import ops
from typing import List

import torch

class Model(torch.nn.Module):
    def __init__(self, dict_data_file: str):
        super().__init__()
        self.dictionary = ops.WordDict(dict_data_file)

    def forward(self, tokens: List[str]) -> List[str]:
        return self.dictionary.translate(tokens)

class TestWordDict(unittest.TestCase):
    dict_data_file = os.path.join(os.path.dirname(__file__), 'data', 'word_dict.data.txt')

    def test_process(self):
        m = Model(TestWordDict.dict_data_file)
        res = m.forward(["life", "in", "suzhou"])
        self.assertEqual(res, ["life", "in", "苏州"])

    def test_serialize(self):       
        m = Model(TestWordDict.dict_data_file)
        save(m, 'tmp/test_word_dict/model.pkl')
        restored_m = load('tmp/test_word_dict/model.pkl')
        res = restored_m.forward(["life", "in", "beijing"])
        self.assertEqual(res, ["life", "in", "北京"])

if __name__ == "__main__":
    unittest.main()
