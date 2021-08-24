# test_cabinet.py    -*- coding: utf-8 -*-


import pytest

from cabinet-calc import cabinet as C


@pytest.fixture
def cabrun():
    return C.Run(157.25, 28.5, 24.0)


def test_num_cabinets(cabrun):
    assert cabrun.num_cabinets == 5

def test_fullwidth(cabrun):
    assert cabrun.fullwidth == 157.25

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

def test_filler_width(cabrun):
    assert cabrun.filler_width == None

def test_filler_height(cabrun):
    assert cabrun.filler_height == None

def test_filler_thickness(cabrun):
    assert cabrun.filler_thickness == None

def test_num_backpanels(cabrun):
    assert cabrun.num_backpanels == 5

def test_back_width(cabrun):
    assert cabrun.back_width == 31.45

def test_back_height(cabrun):
    assert cabrun.back_height == 28.5

def test_back_thickness(cabrun):
    assert cabrun.back_thickness == 0.74

def test_has_legs(cabrun):
    assert cabrun.has_legs == False

def test_setting_has_legs(cabrun):
    assert cabrun.has_legs == False
    cabrun.has_legs = True
    assert cabrun.has_legs == True
    assert cabrun.btmpanel_thicknesses == [0.74, 0.74]

def test_setting_fullwidth(cabrun):
    assert cabrun.fullwidth == 157.25
    cabrun.fullwidth = 142.375
    assert cabrun.fullwidth == 142.375

def test_btmpanels_per_cab(cabrun):
    assert cabrun.btmpanels_per_cab == 1

def test_bottom_stacked(cabrun):
    assert cabrun.bottom_stacked == False

def test_num_bottompanels(cabrun):
    assert cabrun.num_bottompanels == 5

def test_bottom_thickness(cabrun):
    assert cabrun.bottom_thickness == 0.74

def test_setting_bottom_thickness(cabrun):
    assert cabrun.bottom_thickness == 0.74
    cabrun.bottom_thickness = 1.61
    assert cabrun.bottom_thickness == 1.5

def test_bottom_width(cabrun):
    assert cabrun.bottom_width == 29.97     # 31.45 - 2 * 0.74

def test_bottom_depth(cabrun):
    assert cabrun.bottom_depth == 22.375

def test_num_sidepanels(cabrun):
    assert cabrun.num_sidepanels == 10

def test_side_depth(cabrun):
    assert cabrun.side_depth == 22.375      # 24.0 - (0.76 + 0.125) - 0.74

def test_side_height(cabrun):
    assert cabrun.side_height == 28.5

def test_side_thickness(cabrun):
    assert cabrun.side_thickness == 0.74

def test_num_topnailers(cabrun):
    assert cabrun.num_topnailers == 10

def test_topnailer_width(cabrun):
    assert cabrun.topnailer_width == 29.97

def test_topnailer_thickness(cabrun):
    assert cabrun.topnailer_thickness == 0.74

def test_num_doors(cabrun):
    assert cabrun.num_doors == 10

def test_doorside_space(cabrun):
    assert cabrun.doorside_space == 0.375

def test_door_width(cabrun):
    assert cabrun.door_width == 15.5375     # (31.45 - 0.375) / 2

def test_door_height(cabrun):
    assert cabrun.door_height == 28.0


# test_cabinet.py  ends here
