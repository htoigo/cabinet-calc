# job.py    -*- coding: utf-8 -*-

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
from dimension_strs import dimstr, dimstr_col


class Job:
    """A job with name, an optional description, and a run of cabinets."""

    def __init__(self, name, cab_run, desc=''):
        # Job.name is required and must be unique, as it is the job ID.
        self.name = name
        # A description is optional, and by default is the empty string.
        self.description = desc
        # For now, each job only has ONE run of cabinets.
        self.cabs = cab_run

    @property
    def header(self):
        result = []
        result.append('Job Name: ' + self.name)
        if self.description is not '':
            result.append('Description: ' + self.description)
        return result

    @property
    def overview(self):
        result = []
        # result.append('Overview:\n')
        # result.append('Total Wall Space: ' + str(self.cabs.fullwidth) + '"')
        summary = ( str(self.cabs.num_cabinets) + ' cabinets measuring '
                    + dimstr(self.cabs.cabinet_width) + '" '
                    + 'totalling '
                    + dimstr(self.cabs.cabinet_width
                             * self.cabs.num_cabinets) + '"' )
        if self.cabs.num_fillers == 0:
            summary += ( ', with finished end panels on left and right.'
                         ' No filler panels required.' )
        elif self.cabs.num_fillers == 1:
            summary += ', with a ' + dimstr(self.cabs.filler_width) + '" filler.'
        elif self.cabs.num_fillers == 2:
            summary += ( ', with two (2) ' + dimstr(self.cabs.filler_width)
                         + '" fillers.' )
        else:
            # The number of fillers should never be greater than 2
            raise ValueError('number of fillers not 0, 1, or 2')
        result.append(summary)
        result.append('\nNumber of cabinets needed:  '
                      + str(self.cabs.num_cabinets))
        result.append('Single cabinet width:  '
                      + dimstr(self.cabs.cabinet_width) + '"')
        result.append('\nMaterial:  ' + self.cabs.material)
        result.append('Material thickness:  '
                      + dimstr(self.cabs.matl_thickness) + '"')
        return result

    @property
    def partslist(self):
        result = []
        # result.append('Parts List:\n')
        result.append(
            'Back Panels:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_backpanels,
                dimstr_col(self.cabs.back_width) + '"',
                dimstr_col(self.cabs.back_height) + '"',
                dimstr(self.cabs.back_thickness) + '"') )
        result.append(
            'Bottom Panels:   {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_bottompanels,
                dimstr_col(self.cabs.bottom_width) + '"',
                dimstr_col(self.cabs.bottom_depth) + '"',
                dimstr(self.cabs.bottom_thickness) + '"') )
        result.append(
            'Side Panels:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_sidepanels,
                dimstr_col(self.cabs.side_depth) + '"',
                dimstr_col(self.cabs.side_height) + '"',
                dimstr(self.cabs.side_thickness) + '"') )
        result.append(
            'Top Nailers:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_topnailers,
                dimstr_col(self.cabs.topnailer_width) + '"',
                dimstr_col(self.cabs.topnailer_depth) + '"',
                dimstr(self.cabs.topnailer_thickness) + '"') )
        if self.cabs.num_fillers > 0:
            result.append(
                'Fillers:         {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                    self.cabs.num_fillers,
                    dimstr_col(self.cabs.filler_width) + '"',
                    dimstr_col(self.cabs.filler_height) + '"',
                    dimstr(self.cabs.filler_thickness) + '"') )
        result.append(
            'Doors:           {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_doors,
                dimstr_col(self.cabs.door_width) + '"',
                dimstr_col(self.cabs.door_height) + '"',
                dimstr(self.cabs.door_thickness) + '"') )
        return result

    @property
    def specification(self):
        """Return a complete specification of the job as a list of strings."""
        sep = '-' * 60
        result = ( [sep] + self.header + [sep]
                   + ['Overview:\n'] + self.overview + [sep]
                   + ['Parts List:\n'] + self.partslist + [sep] )
        return result


# job.py ends here
