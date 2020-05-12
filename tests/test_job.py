# test_job.py    -*- coding: utf-8 -*-


import pytest
import app.cabinet as C
import app.job as J


@pytest.fixture
def job():
    # No fillers, no legs
    return J.Job('Job 1', C.Run(157.125, 27.875, 24),
                 desc='Test various parts of the job module.')


def test_job_header(job):
    assert job.header == ['Job Name: Job 1'
                          , 'Description: Test various parts of the job module.'
                          , 'Total Wall Space: 157.125"']


def test_job_summaryln(job):
    assert job.summaryln == ['5 cabinets measuring 31 7/16" totalling 157 1/8"'
                             ', with finished end panels on left and right.'
                             ' No filler panels required.']


def test_job_cabinfo(job):
    assert job.cabinfo == ['Number of cabinets needed:  5'
                           , 'Single cabinet width:  31 7/16"']


def test_job_materialinfo(job):
    assert job.materialinfo == ['Primary Material:  3/4" Standard Plywood'
                                , 'Door Material:  3/4" Melamine']


def test_job_overview(job):
    assert job.overview == ['5 cabinets measuring 31 7/16" totalling 157 1/8"'
                            ', with finished end panels on left and right.'
                            ' No filler panels required.'
                            , ''
                            , 'Number of cabinets needed:  5'
                            , 'Single cabinet width:  31 7/16"'
                            , ''
                            , 'Primary Material:  3/4" Standard Plywood'
                            , 'Door Material:  3/4" Melamine']


def test_job_partslist(job):
    assert job.partslist == [  'Back Panels:      5  @  31 7/16"    x  27 7/8"     x  3/4"'
                             , 'Bottom Panels:    5  @  29 15/16"   x  24          x  3/4"'
                             , 'Side Panels:     10  @              x  27 7/8"     x  3/4"'
                             , 'Top Nailers:     10  @  '
                             , 'Doors:           10  @  ']


def test_job_specification(job):
    assert 
# test_job.py  ends here
