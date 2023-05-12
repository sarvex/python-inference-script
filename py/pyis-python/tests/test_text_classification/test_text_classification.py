# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import unittest, os
from typing import Iterator, List, Tuple, Dict
from pyis.python import ops
from pyis.python import save
from pyis.python.offline import TextClassification as TextCls

tmp_dir = 'tmp/test_text_classification/'
os.makedirs(tmp_dir, exist_ok=True)

class Model:
    def __init__(self, queries:Iterator[List[str]], labels:Iterator[int]):
        super(Model, self).__init__()
        self.unigram_featurizer = None
        self.bigram_featurizer = None
        self.concat_featurizer = None
        self.linear_svm = None
        self._train(queries, labels)
    
    def forward(self, x:List[str]) -> List[float]:
        unigrams = self.unigram_featurizer.transform(x)
        #self._print_features(unigrams, 'unigrams: ')
        bigrams = self.bigram_featurizer.transform(x)
        #self._print_features(bigrams, 'bigrams: ')
        features = self.concat_featurizer.transform([unigrams, bigrams])
        features_svm = self.text_feature_to_liblinear(features)
        return self.linear_svm.predict(features_svm)
    
    def text_feature_to_liblinear(self, features:List[ops.TextFeature]) -> List[Tuple[int, float]]:
        feature_map: Dict[int, float] = {}
        for f in features:
            fid = f.id()
            fvalue = f.value()
            if fid in feature_map:
                feature_map[fid] += fvalue
            else:
                feature_map[fid] = fvalue
        
        return [(k, feature_map[k]) for k in sorted(feature_map.keys())]

    def _print_features(self, features: List[ops.TextFeature], prefix=""):
        print(prefix, end='')
        for i in features:
            print(f'{i.to_tuple()} ', end='')
        print("")
                   
    def _train(self, xs, ys):
        self.unigram_featurizer = TextCls.create_ngram_featurizer(xs, n=1, boundaries=True)
        self.unigram_featurizer.dump_ngram(os.path.join(tmp_dir, '1gram.txt'))
        unigram_features = [self.unigram_featurizer.transform(q) for q in xs]

        self.bigram_featurizer = TextCls.create_ngram_featurizer(xs, n=2, boundaries=True)
        self.bigram_featurizer.dump_ngram(os.path.join(tmp_dir, '2gram.txt'))     
        bigram_features = [self.bigram_featurizer.transform(q) for q in xs]

        self.concat_featurizer = TextCls.create_text_feature_concat(unigram_features, bigram_features)
        concat_features = [self.concat_featurizer.transform(list(x)) for x in zip(unigram_features, bigram_features)]
        for x in concat_features:
            self._print_features(x)
       
        data_file = os.path.join(tmp_dir, 'svm.data.txt')
        model_file = os.path.join(tmp_dir, 'svm.model.bin')
        self.linear_svm = TextCls.create_linear_svm(concat_features, ys, data_file, model_file)


class TestTextClassification(unittest.TestCase):
    def test_text_classification(self):
        xs = [
            ['this', 'is', 'heaven'],
            ['this', 'is', 'hell']
        ]
        ys = [1, 2]

        m = Model(xs, ys)
        probs = m.forward(['is', 'heaven'])
        print(probs)
        self.assertAlmostEqual(probs[0], 0.5, places=2)
        self.assertAlmostEqual(probs[1], 0.0, places=2)
        
        model_file = os.path.join(tmp_dir, 'model.pkl')
        save(m, model_file)

if __name__ == "__main__":
    unittest.main()