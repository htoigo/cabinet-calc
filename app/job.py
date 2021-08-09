# job.py        -*- coding: utf-8 -*-

# Job module for Cabinet Calc.

# Copyright © 2018  Harry H. Toigo II, L33b0

# This file is part of Cabinet Calc.
# Cabinet Calc is the custom Euro-style cabinet configurator.

# Cabinet Calc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Cabinet Calc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Cabinet Calc.  If not, see <https://www.gnu.org/licenses/>.

# To contact us:
#
# Email:       hhtpub@gmail.com
#
# Snail mail:  433 Buena Vista Ave. #310
#              Alameda CA  94501


"""Cabinet Calc job module.

This module implements the job facilities of Cabinet Calc.
"""

# __all__ = [max_cabinet_width, door_hinge_gap, cabinet_run, num_cabinets,
#            Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'


from contracts import contract

from app.cabinet import Ends
from app.dimension_strs import dimstr, dimstr_col, thickness_str


def all_equal(lst):
    return lst[1:] == lst[:-1]


class Job(object):
    """A job with name, an optional description, and a run of cabinets."""

    def __init__(self, name, cab_run, desc=''):
        # Job.name is required and must be unique, as it is the job ID.
        self.name = name
        # A description is optional, and by default is the empty string.
        self.description = desc
        # For now, each job only has ONE run of cabinets.
        self.cabs = cab_run

    @property
    @contract
    def header(self):
        """Header of the job specification.

        Includes job name, job description (if provided), and total wall space.

           :rtype: list[>0](str)
        """
        result = []
        result.append('Job Name: ' + self.name)
        if self.description != '':
            result.append('Description: ' + self.description)
        result.append('Total Wall Space: ' + str(self.cabs.fullwidth) + '"')
        return result

    @property
    @contract
    def summaryln(self):
        """A very brief summary of the job.

           :rtype: list[>0](str)
        """
        numcabs = self.cabs.num_cabinets
        cabwidth = self.cabs.cabinet_width
        summary = (str(numcabs) + (' cabinet' if numcabs == 1 else ' cabinets')
                   + ' measuring ' + dimstr(cabwidth) + '" ' + 'totalling '
                   + dimstr(cabwidth * numcabs) + '"')
        if self.cabs.fillers is Ends.NEITHER:
            summary += (', with finished end panels on left and right.'
                          ' No filler panels required.')
        elif self.cabs.fillers is Ends.LEFT:
            summary += (', with a ' + dimstr(self.cabs.filler_width)
                          + '" filler on the left.')
        elif self.cabs.fillers is Ends.RIGHT:
            summary += (', with a ' + dimstr(self.cabs.filler_width)
                          + '" filler on the right.')
        elif self.cabs.fillers is Ends.BOTH:
            summary += (', with two (2) ' + dimstr(self.cabs.filler_width)
                          + '" fillers.')
        else:
            raise TypeError('fillers is not Ends.NEITHER, .LEFT, .RIGHT,'
                            ' or .BOTH')
        if self.cabs.has_legs:
            summary += (' To be mounted on legs.')
        return [summary]

    @property
    @contract
    def cabinfo(self):
        """Description of the number of cabinets needed and cabinet width.

           :rtype: list[>0](str)
        """
        result = []
        result.append('Number of cabinets needed:  '
                      + str(self.cabs.num_cabinets))
        result.append('Single cabinet width:  '
                      + dimstr(self.cabs.cabinet_width) + '"')
        return result

    @property
    @contract
    def materialinfo(self):
        """Description of the materials needed for the job.

           :rtype: list[>0](str)
        """
        result = []
        result.append('Primary Material:  '
                      + thickness_str(self.cabs.prim_thickness)
                      + '" ' + self.cabs.prim_material)
        result.append('Door Material:  '
                      + thickness_str(self.cabs.door_thickness)
                      + '" ' + self.cabs.door_material)
        if self.cabs.has_legs:
            if self.cabs.bottom_stacked:
                mat_thick_strs = list(map(
                    thickness_str, self.cabs.btmpanel_thicknesses))
                if not all_equal(mat_thick_strs):
                    raise ValueError('stacked bottom panels have different'
                                     ' thicknesses')
                mat_thick_str = mat_thick_strs[0]
                btm_mat_str = (
                    'Bottom Material:  ' + mat_thick_str + '" '
                    + self.cabs.prim_material
                    + ', stacked x ' + str(self.cabs.btmpanels_per_cab))
            else:
                mat_thick_str = thickness_str(self.cabs.bottom_thickness)
                btm_mat_str = (
                    'Bottom Material:  ' + mat_thick_str + '" '
                    + self.cabs.prim_material)
            result.append(btm_mat_str)
        return result

    @property
    @contract
    def overview(self):
        """Overview of the job specification.

           :rtype: list[>0](str)
        """
        result = []
        result.extend(self.summaryln)
        result.append('')
        result.extend(self.cabinfo)
        result.append('')
        result.extend(self.materialinfo)
        return result

    @property
    @contract
    def partslist(self):
        """Detailed list of parts needed for the job.

           :rtype: list[>0](str)
        """
        result = []
        result.append(
            'Back Panels:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_backpanels,
                dimstr_col(self.cabs.back_width) + '"',
                dimstr_col(self.cabs.back_height) + '"',
                thickness_str(self.cabs.back_thickness) + '"'))
        result.append(
            'Bottom Panels:   {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_bottompanels,
                dimstr_col(self.cabs.bottom_width) + '"',
                dimstr_col(self.cabs.bottom_depth) + '"',
                (thickness_str(self.cabs.bottom_thickness / 2)
                 if thickness_str(self.cabs.bottom_thickness) == '1 1/2'
                 else thickness_str(self.cabs.bottom_thickness)) + '"'))
        result.append(
            'Side Panels:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_sidepanels,
                dimstr_col(self.cabs.side_depth) + '"',
                dimstr_col(self.cabs.side_height) + '"',
                thickness_str(self.cabs.side_thickness) + '"'))
        result.append(
            'Top Nailers:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_topnailers,
                dimstr_col(self.cabs.topnailer_width) + '"',
                dimstr_col(self.cabs.topnailer_depth) + '"',
                thickness_str(self.cabs.topnailer_thickness) + '"'))
        if self.cabs.num_fillers > 0:
            result.append(
                'Fillers:         {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                    self.cabs.num_fillers,
                    dimstr_col(self.cabs.filler_width) + '"',
                    dimstr_col(self.cabs.filler_height) + '"',
                    thickness_str(self.cabs.filler_thickness) + '"'))
        result.append(
            'Doors:           {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
                self.cabs.num_doors,
                dimstr_col(self.cabs.door_width) + '"',
                dimstr_col(self.cabs.door_height) + '"',
                thickness_str(self.cabs.door_thickness) + '"'))
        return result

    @property
    @contract
    def specification(self):
        """Return a complete specification of the job as a list of strings.

           :rtype: list[>0](str)
        """
        sep = '-' * 65
        result = ([sep] + self.header + [sep]
                  + ['Overview:', ''] + self.overview + [sep]
                  + ['Parts List:', ''] + self.partslist + [sep])
        return result


# job.py  ends here
