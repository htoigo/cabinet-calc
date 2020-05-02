# test_cabinet.py    -*- coding: utf-8 -*-

import sys
import os

# Add the root directory of the project to sys.path so that we can find modules
# in other subtrees (outside of tests dir) for importing.
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import app.cabinet as C

def test_num_cabinets():
    cr = C.Run(157.25, 28.5, 24.0)
    assert cr.num_cabinets == 5

def test_cabinet_height():
    cr = C.Run(157.25, 28.5, 24.0)
    assert cr.cabinet_height == 28.5

def test_cabinet_depth():
    cr = C.Run(157.25, 28.5, 24.0)
    assert cr.cabinet_depth == 24.0

# test_cabinet.py ends here
