# -*- coding: utf-8 -*-

"""
job.py
~~~~~~

This module implements the job facilities of cabcalc.

:copyright: (c) 2018 by Lee Bernard, Harry H. Toigo II.
:license: MIT, see LICENSE file for more details.


"""

#__all__ = [max_cabinet_width, door_hinge_gap, cabinet_run, num_cabinets, Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'


class Job:
    """A customer job."""

    def __init__(self, name, customer, cab_banks=[], ):
        # job.ID?
        self.name = name
        self.customer = customer
        self.cab_banks = cab_banks
