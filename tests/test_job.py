# test_job.py    -*- coding: utf-8 -*-


import pytest
from ..app import cabinet as C
from ..app import job as J


@pytest.fixture
def job():
    # No fillers, no legs
    return J.Job('Job 1', C.Run(157.125, 27.875, 24),
                 desc='A job to test various parts of the job module.')


def test_job_summaryln(job):
    pass    # assert job.summaryln == ['']


def test_job_cabinfo(job):
    assert job.cabinfo == ['Number of cabinets needed:  5'
                           , 'Single cabinet width:  31 7/16"']


# test_job.py  ends here
