# job.py        -*- coding: utf-8 -*-

# Job module for Cabinet Wiz.

# Copyright © 2018  Harry H. Toigo II, L33b0

# This file is part of Cabinet Wiz.
# Cabinet Wiz is the custom Euro-style cabinet configurator.

# Cabinet Wiz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Cabinet Wiz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Cabinet Wiz.  If not, see <https://www.gnu.org/licenses/>.

# To contact us:
#
# Email:       hhtpub@gmail.com
#
# Snail mail:  433 Buena Vista Ave. #310
#              Alameda CA  94501


"""Cabinet Wiz job module.

This module implements the job facilities of Cabinet Wiz.
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
        result.append('Total Wall Space: ' + str(self.cabs.fullwidth) + '"')
        return result

    @property
    def summaryln(self):
        """Return a single string summary of the job."""
        result = ( str(self.cabs.num_cabinets) + ' cabinets measuring '
                   + dimstr(self.cabs.cabinet_width) + '" '
                   + 'totalling '
                   + dimstr(self.cabs.cabinet_width
                            * self.cabs.num_cabinets) + '"' )
        if self.cabs.num_fillers == 0:
            result += ( ', with finished end panels on left and right.'
                        ' No filler panels required.\n' )
        elif self.cabs.num_fillers == 1:
            result += ( ', with a ' + dimstr(self.cabs.filler_width)
                        + '" filler.\n' )
        elif self.cabs.num_fillers == 2:
            result += ( ', with two (2) ' + dimstr(self.cabs.filler_width)
                        + '" fillers.\n' )
        else:
            # The number of fillers should never be greater than 2.
            raise ValueError('number of fillers not 0, 1, or 2')
        return result

    @property
    def cabinfo(self):
        """A list of strings."""
        result = []
        result.append('Number of cabinets needed:  '
                      + str(self.cabs.num_cabinets))
        result.append('Single cabinet width:  '
                      + dimstr(self.cabs.cabinet_width) + '"\n')
        return result

    @property
    def materialinfo(self):
        """A list of strings."""
        result = []
        result.append('Material:  ' + self.cabs.material)
        result.append('Material thickness:  '
                      + dimstr(self.cabs.matl_thickness) + '"')
        return result

    @property
    def overview(self):
        result = []
        # result.append('Overview:\n')
        result.append(self.summaryln)
        result.extend(self.cabinfo)
        result.extend(self.materialinfo)
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
