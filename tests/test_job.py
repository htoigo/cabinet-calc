# test_job.py    -*- coding: utf-8 -*-


import pytest
import app.cabinet as C
import app.job as J


@pytest.fixture
def job():
    # No fillers, no legs
    return J.Job('Job 1', C.Run(157.125, 27.875, 24),
                 desc='Test various parts of the job module.')


@pytest.fixture
def job_filler_l():
    return J.Job('Left Filler Job', C.Run(183, 28, 24, fillers=C.Ends.left),
                 desc='Integer dimensions, filler on left, no legs.')


def test_job_header(job):
    assert job.header == ['Job Name: Job 1'
                          , 'Description: Test various parts of the job module.'
                          , 'Total Wall Space: 157.125"']


def test_job_filler_l_header(job_filler_l):
    assert job_filler_l.header == ['Job Name: Left Filler Job'
                          , 'Description: Integer dimensions, filler on left, no legs.'
                          , 'Total Wall Space: 183"']


def test_job_summaryln(job):
    assert job.summaryln == ['5 cabinets measuring 31 7/16" totalling 157 1/8"'
                             ', with finished end panels on left and right.'
                             ' No filler panels required.']


def test_job_filler_l_summaryln(job_filler_l):
    assert job_filler_l.summaryln == ['6 cabinets measuring 30" totalling 180"'
                             ', with a 3" filler on the left.']


def test_job_cabinfo(job):
    assert job.cabinfo == ['Number of cabinets needed:  5'
                           , 'Single cabinet width:  31 7/16"']


def test_job_filler_l_cabinfo(job_filler_l):
    assert job_filler_l.cabinfo == ['Number of cabinets needed:  6'
                           , 'Single cabinet width:  30"']


def test_job_materialinfo(job):
    assert job.materialinfo == ['Primary Material:  3/4" Standard Plywood'
                                , 'Door Material:  3/4" Melamine']


def test_job_filler_l_materialinfo(job_filler_l):
    assert job_filler_l.materialinfo == [
        'Primary Material:  3/4" Standard Plywood'
        , 'Door Material:  3/4" Melamine']


def test_job_overview(job):
    assert job.overview == [
        '5 cabinets measuring 31 7/16" totalling 157 1/8"'
        ', with finished end panels on left and right.'
        ' No filler panels required.'
        , ''
        , 'Number of cabinets needed:  5'
        , 'Single cabinet width:  31 7/16"'
        , ''
        , 'Primary Material:  3/4" Standard Plywood'
        , 'Door Material:  3/4" Melamine']


def test_job_filler_l_overview(job_filler_l):
    assert job_filler_l.overview == [
        '6 cabinets measuring 30" totalling 180"'
        ', with a 3" filler on the left.'
        , ''
        , 'Number of cabinets needed:  6'
        , 'Single cabinet width:  30"'
        , ''
        , 'Primary Material:  3/4" Standard Plywood'
        , 'Door Material:  3/4" Melamine']


def test_job_partslist(job):
    assert job.partslist == [
        'Back Panels:      5  @  31 7/16"    x  27 7/8"     x  3/4"'
        , 'Bottom Panels:    5  @  29 15/16"   x  22 3/8"     x  3/4"'
        , 'Side Panels:     10  @  22 3/8"     x  27 7/8"     x  3/4"'
        , 'Top Nailers:     10  @  29 15/16"   x   4"         x  3/4"'
        , 'Doors:           10  @  15 1/2+"    x  27 3/8"     x  3/4"']


def test_job_filler_l_partslist(job_filler_l):
    assert job_filler_l.partslist == [
        'Back Panels:      6  @  30"         x  28"         x  3/4"'
        , 'Bottom Panels:    6  @  28 1/2+"    x  22 3/8"     x  3/4"'
        , 'Side Panels:     12  @  22 3/8"     x  28"         x  3/4"'
        , 'Top Nailers:     12  @  28 1/2+"    x   4"         x  3/4"'
        , 'Fillers:          1  @   3"         x  28"         x  3/4"'
        , 'Doors:           12  @  14 13/16"   x  27 1/2"     x  3/4"']


def test_job_specification(job):
    assert job.specification == [
        '-' * 65
        , 'Job Name: Job 1'
        , 'Description: Test various parts of the job module.'
        , 'Total Wall Space: 157.125"'
        , '-' * 65
        , 'Overview:'
        , ''
        , '5 cabinets measuring 31 7/16" totalling 157 1/8"'
        ', with finished end panels on left and right.'
        ' No filler panels required.'
        , ''
        , 'Number of cabinets needed:  5'
        , 'Single cabinet width:  31 7/16"'
        , ''
        , 'Primary Material:  3/4" Standard Plywood'
        , 'Door Material:  3/4" Melamine'
        , '-' * 65
        , 'Parts List:'
        , ''
        , 'Back Panels:      5  @  31 7/16"    x  27 7/8"     x  3/4"'
        , 'Bottom Panels:    5  @  29 15/16"   x  22 3/8"     x  3/4"'
        , 'Side Panels:     10  @  22 3/8"     x  27 7/8"     x  3/4"'
        , 'Top Nailers:     10  @  29 15/16"   x   4"         x  3/4"'
        , 'Doors:           10  @  15 1/2+"    x  27 3/8"     x  3/4"'
        , '-' * 65]


def test_job_filler_l_specification(job_filler_l):
    assert job_filler_l.specification == [
        '-' * 65
        , 'Job Name: Left Filler Job'
        , 'Description: Integer dimensions, filler on left, no legs.'
        , 'Total Wall Space: 183"'
        , '-' * 65
        , 'Overview:'
        , ''
        , '6 cabinets measuring 30" totalling 180"'
        ', with a 3" filler on the left.'
        , ''
        , 'Number of cabinets needed:  6'
        , 'Single cabinet width:  30"'
        , ''
        , 'Primary Material:  3/4" Standard Plywood'
        , 'Door Material:  3/4" Melamine'
        , '-' * 65
        , 'Parts List:'
        , ''
        , 'Back Panels:      6  @  30"         x  28"         x  3/4"'
        , 'Bottom Panels:    6  @  28 1/2+"    x  22 3/8"     x  3/4"'
        , 'Side Panels:     12  @  22 3/8"     x  28"         x  3/4"'
        , 'Top Nailers:     12  @  28 1/2+"    x   4"         x  3/4"'
        , 'Fillers:          1  @   3"         x  28"         x  3/4"'
        , 'Doors:           12  @  14 13/16"   x  27 1/2"     x  3/4"'
        , '-' * 65]


# test_job.py  ends here
