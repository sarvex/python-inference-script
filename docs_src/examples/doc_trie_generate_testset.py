# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

#! /bin/usr/env python3
# -*- encoding: ascii -*-
import random

def randstr():
    lst = [chr(i + ord('a')) for i in range(26)] + \
          [chr(i + ord('A')) for i in range(26)] + [chr(i + ord('0')) for i in range(10)]
    length = random.randint(5,20)
    return "".join(random.choice(lst) for _ in range(length))

with open('dict.txt', 'w') as f:
    for _ in range(5000000):
        f.write(randstr() + '\n')
