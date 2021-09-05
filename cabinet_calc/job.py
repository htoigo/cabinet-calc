# job.py                              -*- coding: utf-8; -*-

"""The job module for Cabinet Calc.

Copyright © 2018-2021 Harry H. Toigo II, L33b0

This file is part of Cabinet Calc.

Cabinet Calc is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cabinet Calc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cabinet Calc.  If not, see <https://www.gnu.org/licenses/>.

This module implements all the job-related facilities of Cabinet Calc,
encapsulated in the Job class. A Job object represents a one-off cabinet job
and holds all of its specifications, i.e. its name (which is its unique
identifier), its description and a cabinet Run object holding all the parameters
of its cabinet run, such as dimensions, etc.
"""


__all__ = ['Job']


from cabinet_calc.cabinet import Ends
from cabinet_calc.dimension_strs import dimstr, dimstr_col, thickness_str


def all_equal(lst):
    """Return True iff all elements in the given list are equal."""
    return lst[1:] == lst[:-1]


class Job(object):
    """A job with name, an optional description, and a run of cabinets."""

    def __init__(self, name, cab_run, desc=''):
        """Set the unique Job name, optional description and its Run object."""
        # Job.name is required and must be unique, as it is the job ID.
        self.name = name
        # A description is optional, and by default is the empty string.
        self.description = desc
        # For now, each job only has ONE run of cabinets.
        self.cabs = cab_run

    @property
    def header(self):
        """Return the header of the job specification as a list of strings.

        Includes job name, job description (if provided), and total wall space.
        """
        result = []
        result.append('Job Name: ' + self.name)
        if self.description != '':
            result.append('Description: ' + self.description)
        result.append('Total Wall Space: ' + str(self.cabs.fullwidth) + '"')
        return result

    @property
    def summaryln(self):
        """Return a very brief summary of the job as a list of strings."""
        numcabs = self.cabs.num_cabinets
        cabwidth = self.cabs.cabinet_width
        summary = (str(numcabs) + (' cabinet' if numcabs == 1 else ' cabinets') +
                   ' measuring ' + dimstr(cabwidth) + '" ' + 'totalling ' +
                   dimstr(cabwidth * numcabs) + '"')
        if self.cabs.fillers is Ends.NEITHER:
            summary += (', with finished end panels on left and right.'
                        ' No filler panels required.')
        elif self.cabs.fillers is Ends.LEFT:
            summary += (', with a ' + dimstr(self.cabs.filler_width) +
                        '" filler on the left.')
        elif self.cabs.fillers is Ends.RIGHT:
            summary += (', with a ' + dimstr(self.cabs.filler_width) +
                        '" filler on the right.')
        elif self.cabs.fillers is Ends.BOTH:
            summary += (', with two (2) ' + dimstr(self.cabs.filler_width) +
                        '" fillers.')
        else:
            raise TypeError('fillers is not Ends.NEITHER, .LEFT, .RIGHT,'
                            ' or .BOTH')
        if self.cabs.has_legs:
            summary += (' To be mounted on legs.')
        return [summary]

    @property
    def cabinfo(self):
        """Return number of cabinets needed and cabinet width as list of strings."""
        result = []
        result.append('Number of cabinets needed:  ' + str(self.cabs.num_cabinets))
        result.append('Single cabinet width:  ' + dimstr(self.cabs.cabinet_width) +
                      '"')
        return result

    @property
    def materialinfo(self):
        """Return the materials needed for the job as a list of strings."""
        result = []
        result.append('Primary Material:  ' +
                      thickness_str(self.cabs.prim_thickness) + '" ' +
                      self.cabs.prim_material)
        result.append('Door Material:  ' + thickness_str(self.cabs.door_thickness) +
                      '" ' + self.cabs.door_material)
        if self.cabs.has_legs:
            if self.cabs.bottom_stacked:
                mat_thick_strs = list(
                    map(thickness_str, self.cabs.btmpanel_thicknesses))
                if not all_equal(mat_thick_strs):
                    raise ValueError('stacked bottom panels have different'
                                     ' thicknesses')
                mat_thick_str = mat_thick_strs[0]
                btm_mat_str = ('Bottom Material:  ' + mat_thick_str + '" ' +
                               self.cabs.prim_material + ', stacked x ' +
                               str(self.cabs.btmpanels_per_cab))
            else:
                mat_thick_str = thickness_str(self.cabs.bottom_thickness)
                btm_mat_str = ('Bottom Material:  ' + mat_thick_str + '" ' +
                               self.cabs.prim_material)
            result.append(btm_mat_str)
        return result

    @property
    def overview(self):
        """Return an overview of the job specification as a list of strings."""
        result = []
        result.extend(self.summaryln)
        result.append('')
        result.extend(self.cabinfo)
        result.append('')
        result.extend(self.materialinfo)
        return result

    @property
    def partslist(self):
        """Return a list of parts needed for the job as a list of strings."""
        result = []
        result.append('Back Panels:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
            self.cabs.num_backpanels,
            dimstr_col(self.cabs.back_width) + '"',
            dimstr_col(self.cabs.back_height) + '"',
            thickness_str(self.cabs.back_thickness) + '"'))
        result.append('Bottom Panels:   {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
            self.cabs.num_bottompanels,
            dimstr_col(self.cabs.bottom_width) + '"',
            dimstr_col(self.cabs.bottom_depth) + '"',
            (thickness_str(self.cabs.bottom_thickness /
                           2) if thickness_str(self.cabs.bottom_thickness)
             == '1 1/2' else thickness_str(self.cabs.bottom_thickness)) + '"'))
        result.append('Side Panels:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
            self.cabs.num_sidepanels,
            dimstr_col(self.cabs.side_depth) + '"',
            dimstr_col(self.cabs.side_height) + '"',
            thickness_str(self.cabs.side_thickness) + '"'))
        result.append('Top Nailers:     {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
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
        result.append('Doors:           {:2d}  @  {:10s}  x  {:10s}  x  {}'.format(
            self.cabs.num_doors,
            dimstr_col(self.cabs.door_width) + '"',
            dimstr_col(self.cabs.door_height) + '"',
            thickness_str(self.cabs.door_thickness) + '"'))
        return result

    @property
    def specification(self):
        """Return a complete specification of the job as a list of strings."""
        sep = '-' * 65
        result = ([sep] + self.header + [sep] + ['Overview:', ''] + self.overview +
                  [sep] + ['Parts List:', ''] + self.partslist + [sep])
        return result

# job.py  ends here
