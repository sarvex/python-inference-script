#################################################################
#              WARNING: Auto-Generated File
#  This file was generated by a tool(py/pyis-torch/code_gen.py)
#  Any changes made to it will be overwritten when regenerated
#################################################################

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import io
from typing import Dict, Iterator, List
from pyis.torch import ops

class TextClassification:
    def __init__(self):
        pass

    @staticmethod
    def create_ngram_featurizer(
            xs: Iterator[List[str]], 
            n:int=1, 
            boundaries:bool=True) -> ops.NGramFeaturizer:
        featurizer = ops.NGramFeaturizer(n, boundaries)
        for x in xs:
            featurizer.fit(x)
        return featurizer

    @staticmethod
    # variadic_xs: Iterator[List[TextFeature]], Iterator[List[TextFeature]], ...
    def create_text_feature_concat(*variadic_xs, start_id=1) -> ops.TextFeatureConcat:
        tf_concat = ops.TextFeatureConcat(start_id)
        for x in zip(*variadic_xs):
            tf_concat.fit(list(x))
        return tf_concat
    
    @staticmethod
    def create_linear_svm(
            xs:Iterator[List[ops.TextFeature]],
            ys:Iterator[int], 
            data_file:str, 
            model_file:str, 
            solver_type = 5,
            eps = 0.1, 
            C = 1.0, 
            p = 0.5,
            bias =1.0) -> ops.LinearSVM:
        # generate liblinear training data from text_features and ys.
        TextClassification.text_features_to_libsvm(xs, ys, data_file)
        ops.LinearSVM.train(data_file, model_file, solver_type, eps, C, p, bias)
        return ops.LinearSVM(model_file)

    @staticmethod
    def _transform_single_input(featurizer, xs):
        for x in xs:
            yield featurizer.transform(x)

    @staticmethod
    def _transform_multiple_inputs(featurizer, *variadic_xs):
        for x in zip(*variadic_xs):
            yield featurizer.transform(list(x))

    @staticmethod
    def text_features_to_libsvm(
            xs: Iterator[List[ops.TextFeature]],
            ys: Iterator[int], 
            libsvm_file:str):        
        with io.open(libsvm_file, 'w', newline='\n') as f:
            for x, label in zip(xs, ys):
                if label <= 0:
                    raise RuntimeError(f'{label} is not a valid label id in liblinear')
                features: Dict[int, float] = {}
                for feature in x:
                    fid = feature.id()
                    if fid <= 0:
                        raise RuntimeError(f'{fid} is not a valid feature id in liblinear')
                    if fid not in features:
                        features[fid] = 0.0
                    features[fid] += feature.value()
                print(label, file=f, end='')
                for k in sorted(features):
                    print(f" {k}:{features[k]}", file=f, end='')
                print("", file=f) 
