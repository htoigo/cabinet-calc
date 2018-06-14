#!/usr/bin/env python3

import math


def cab_count(full_width):
    result = 1
    while full_width / result > 36:
        result += 1
    return result


def cab_count2(full_width):
    result = math.ceil(full_width / 36)
    return result


print('Dim\t\tcab_count()\tcab_count2()')
dim = 34.0
while dim <= 275:
    print(str(dim) + '\t\t' + str(cab_count(dim)) + '\t\t'
          + str(cab_count2(dim)))
    dim = round(dim + 0.1, 1)
