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

import cabinet


class Job:
    """A customer job."""

    def __init__(self, name, customer, cab_run):
        # Do we need a unique job.ID?
        self.name = name
        self.customer = customer
        self.cabs = cab_run

    def description(self):
        """Create a job description."""

        def header():
            hdr = []
            hdr.append('Job Name: ' + self.name)
            return hdr

        def overview():
            overvw = []
            overvw.append('Overview:\n')
            overvw.append('Total Wall Space: ' + str(self.cabs.fullwidth) + '"')
            overvw.append(str(self.cabs.num_cabinets) + ' cabinets measuring '
                          + str(self.cabs.cabinet_width) + '" totalling '
                          + str(self.cabs.cabinet_width * self.cabs.num_cabinets)
                          + '"')
            if self.cabs.num_fillers == 0:
                overvw.append('With finished end panels on left and right')
                overvw.append('No filler panels required')
            elif self.cabs.num_fillers == 1:
                overvw.append('with a ' + str(self.cabs.filler_width)
                              + '" filler')
            elif self.cabs.num_fillers == 2:
                overvw.append('with two (2) ' + str(self.cabs.filler_width)
                              + '" fillers')
            else:
                # Raise an exceptiong for having fillers in the middle of a run:
                print('Your layout would have filler in the middle of a run.\n')
            overvw.append('\nMaterial thickness: '
                          + str(self.cabs.matl_thickness) + '"')
            return overvw

        def partslist():
            """Create a parts list, including doors."""
            parts = []
            parts.append('Parts List:\n')
            parts.append(str(self.cabs.num_backpanels) + " @ "
                         + str(self.cabs.back_width) + '" x '
                         + str(self.cabs.back_height) + '" x '
                         + str(self.cabs.back_thickness) + '" -- BACK PNLS')
            parts.append(str(self.cabs.num_bottompanels) + " @ "
                         + str(self.cabs.bottom_width) + '" x '
                         + str(self.cabs.bottom_depth) + '" x '
                         + str(self.cabs.bottom_thickness) + '" -- BOTTOM PNLS')
            parts.append(str(self.cabs.num_sidepanels) + " @ "
                         + str(self.cabs.side_depth) + '" x '
                         + str(self.cabs.side_height) + '" x '
                         + str(self.cabs.side_thickness) + '" -- SIDE PNLS')
            parts.append(str(self.cabs.num_topnailers) + " @ "
                         + str(self.cabs.topnailer_width) + '" x '
                         + str(self.cabs.topnailer_depth) + '" x '
                         + str(self.cabs.topnailer_thickness)
                         + '" -- TOP NAILERS')
            if self.cabs.num_fillers > 0:
                parts.append(str(self.cabs.num_fillers) + ' @ '
                             + str(self.cabs.filler_width) + '" x '
                             + str(self.cabs.filler_height) + '" x '
                             + str(self.cabs.filler_thickness) + '" -- FILLERS')
            parts.append('Door Details:')
            parts.append(str(self.cabs.num_doors) + " @ "
                         + str(self.cabs.door_width) + '" x '
                         + str(self.cabs.door_height) + '" x '
                         + str(self.cabs.door_thickness) + '" -- DOORS')
            return parts

        sep = '-' * 60
        desc = ( [sep] + header() + [sep]
                 + overview() + [sep] + partslist() + [sep] )
        return desc
