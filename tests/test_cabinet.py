# test_cabinet.py    -*- coding: utf-8 -*-

import sys
import os

# Add the root directory of the project to sys.path so that we can find modules
# in other subtrees (outside of tests dir) for importing.
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import pytest
import app.cabinet as C


@pytest.fixture
def cabrun():
    return C.Run(157.25, 28.5, 24.0)


def test_num_cabinets(cabrun):
    assert cabrun.num_cabinets == 5

def test_cabinet_height(cabrun):
    assert cabrun.cabinet_height == 28.5

def test_cabinet_depth(cabrun):
    assert cabrun.cabinet_depth == 24.0

def test_cabinet_width(cabrun):
    assert cabrun.cabinet_width == 31.45

def test_extra_width(cabrun):
    assert cabrun.extra_width == 0

def test_num_fillers(cabrun):
    assert cabrun.num_fillers == 0

# test_cabinet.py ends here
