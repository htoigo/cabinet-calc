# cabinet.py        -*- coding: utf-8 -*-

# The `cabinet' module for Cabinet Wiz, which computes all cabinet specs.

# Copyright © 2018  Harry H. Toigo II, L33b0

# This file is part of Cabinet Wiz, the custom Euro-style cabinet configurator.

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


"""Cabinet Wiz cabinet module.

This module implements the...

Given the full width, height, depth, material, material thickness, and
which ends will have fillers, (along with job name)...

... calculate the number of cabinets needed, each cabinet's width (whether
integral or not), the space left over to be filled by fillers,
the number and dimensions of:
    - full back panels
    - bottom panels
    - side panels
    - top nailers
    - doors

... and create a cut sheet containing the parts list, diagrams of all parts
to be cut, an isometric view of a single cabinet, with all diagrams to scale.
"""


#__all__ = [max_cabinet_width, door_hinge_gap, cabinet_run, num_cabinets, Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'

import math
from enum import Enum

# Module constants

# All measurements are in inches, unless otherwise specified.

max_cabinet_width = 36

# The gap between the back of the door and the front of the cabinet,
# due to the hinges.
door_hinge_gap = 0.125

# Primary materials list. Does each material have a standard thickness
# associated with it?

materials = ( 'Plywood'
            , 'Melamine'
            , 'Graphite'
            , 'Steel' )


class Ends(Enum):
    """An enumeration of the allowable choices for which end or ends of a
    cabinet run have fillers.

    It must be one of:
        neither - no fillers used
        left - only the left end has a filler
        right - only the right end has a filler
        both - both ends have fillers

    This also determines whether or not the end panels must be finished. If an
    end will have a filler then that end can be left unfinished. On the other
    hand, an end without a filler must have a finished end panel.
    """
    neither = 1
    left = 2
    right = 3
    both = 4

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(str):
        try:
            return Ends[str]
        except KeyError:
            raise ValueError()


def cabinet_run(fullwidth, height, depth, fillers=Ends.neither,
                material='Plywood', matl_thickness=0.75, topnailer_depth=4,
                door_thickness=0.75, doortop_space=0.5, doorside_space_l=0.125,
                doorside_space_m=0.125, doorside_space_r=0.125):
    """Construct a (single) :class:`Run <Run>` of cabinets.

    :param fullwidth: Total wall width for this run of cabinets.
    :param height: The distance from the toe kick to top of cabinets.
    :param depth: The distance from front to back, including door.
    :param fillers: Which ends of the run will have fillers.
    :param material: The primary building material name.
    :param matl_thickness: Building material thickness.
    :return: :class:`Run <Run>` object
    :rtype: cabinet.Run
    """
    return Run(fullwidth, height, depth, fillers, material, matl_thickness,
               topnailer_depth, door_thickness, doortop_space, doorside_space_l,
               doorside_space_m, doorside_space_r)


# Should we expose the following functions for ad hoc use?
#
# def num_cabinets(full_width):
#     return result
#
# def cabinet_width(full_width, num_cabinets):
#     return result
#
# def extra_width(full_width, num_cabinets):
#     return result


class Run:
    """A class representing a single run of cabinets.

    At the moment this class assumes that there are exactly two doors per
    cabinet, as does all code in this module. We may change this later to
    allow single-door cabinets, but that will require a lot of changes.
    """
    def __init__(self, fullwidth, height, depth, fillers=Ends.neither,
                 material='Plywood', matl_thickness=0.75, topnailer_depth=4,
                 door_thickness=0.75, doortop_space=0.5, doorside_space_l=0.125,
                 doorside_space_m=0.125, doorside_space_r=0.125):
        self._fullwidth = fullwidth
        self._height = height
        self._depth = depth
        self._material = material
        self._matl_thickness = matl_thickness
        # fillers must be one of: Ends.neither, .left, .right, or .both.
        self.fillers = fillers
        self.topnailer_depth = topnailer_depth
        self.door_thickness = door_thickness
        # The amount the door is shorter than the cabinet, usually 1/2" or 3/8".
        self.doortop_space = doortop_space
        # The space to the left, in between, and to the right of the doors.
        # These three spaces are usually all 1/8".
        self.doorside_space_l = doorside_space_l
        self.doorside_space_m = doorside_space_m
        self.doorside_space_r = doorside_space_r

    @property
    def material(self):
        """Primary building material name, as a string."""
        return self._material

    @property
    def matl_thickness(self):
        """Primary building material thickness, as a float."""
        return self._matl_thickness

    @property
    def fullwidth(self):
        """The total wall width for this run of cabinets."""
        return self._fullwidth

    @property
    def num_cabinets(self):
        """Compute the number of cabinets needed for the given wall width.

        Return the smallest number of cabinets needed, while not exceeding the
        maximum cabinet width.
        """
        return math.ceil(self.fullwidth / max_cabinet_width)

    @property
    def cabinet_height(self):
        """The overall cabinet height."""
        return self._height

    @property
    def cabinet_depth(self):
        """The overall cabinet depth."""
        return self._depth

    @property
    def cabinet_width(self):
        """The width of each individual cabinet in the run."""
        if self.num_fillers == 0:
            # With no fillers, must accept a fractional number of inches.
            width = self._fullwidth / self.num_cabinets
        else:
            # Restrict cabinet width to a whole number of inches.
            width = self._fullwidth // self.num_cabinets
        return width

    @property
    def extra_width(self):
        """The extra space to be filled by fillers."""
        return self._fullwidth % self.num_cabinets

    @property
    def num_fillers(self):
        if self.fillers is Ends.neither:
            result = 0
        elif self.fillers is Ends.left or self.fillers is Ends.right:
            result = 1
        elif self.fillers is Ends.both:
            result = 2
        else:
            raise valueError('fillers is not neither, left, right, or both')
        return result

    @property
    def filler_width(self):
        """The width of the filler(s) to be used in the run."""
        if self.fillers is Ends.neither:
            width = None
        else:
            width = self.extra_width / self.num_fillers
        return width

    @property
    def filler_height(self):
        """The height of the filler(s) to be used in the run."""
        if self.fillers is Ends.neither:
            height = None
        else:
            height = self.cabinet_height
        return height

    @property
    def filler_thickness(self):
        """The thickness of a filler strip."""
        if self.fillers is Ends.neither:
            thickness = None
        else:
            thickness = self.matl_thickness
        return thickness

    @property
    def num_backpanels(self):
        """The number of back panels needed for this run."""
        return self.num_cabinets

    @property
    def back_width(self):
        """The width of a full back panel.

        Full back panels cover the full width of the cabinet.
        """
        return self.cabinet_width

    @property
    def back_height(self):
        """The height of a full back panel.

        Full back panels cover the full height of the cabinet.
        """
        return self.cabinet_height

    @property
    def back_thickness(self):
        """The thickness of a full back panel."""
        return self.matl_thickness

    @property
    def num_bottompanels(self):
        """The number of bottom panels needed for this run."""
        return self.num_cabinets

    @property
    def bottom_width(self):
        """The width of a bottom panel."""
        width = self.cabinet_width - 2 * self.side_thickness
        return width

    @property
    def bottom_depth(self):
        """The depth (front to back) of a bottom panel."""
        return self.side_depth

    @property
    def bottom_thickness(self):
        """The thickness of a bottom panel."""
        return self.matl_thickness

    @property
    def num_sidepanels(self):
        """The number of side panels needed for this run."""
        return 2 * self.num_cabinets

    @property
    def side_depth(self):
        """The depth (front to back) of a side panel.

        Side panel depth is cabinet depth, less thickness of door and gap, less
        thickness of back panel.
        """
        depth = (self.cabinet_depth - (self.door_thickness + door_hinge_gap)
                 - self.back_thickness)
        return depth

    @property
    def side_height(self):
        """The height of a side panel."""
        return self.cabinet_height

    @property
    def side_thickness(self):
        """The thickness of a side panel."""
        return self.matl_thickness

    @property
    def num_topnailers(self):
        """The number of top nailers needed for this run."""
        return 2 * self.num_cabinets

    @property
    def topnailer_width(self):
        """The width of a top nailer."""
        return self.bottom_width

    @property
    def topnailer_thickness(self):
        """."""
        return self.matl_thickness

    @property
    def num_doors(self):
        """The number of doors needed for this run."""
        return 2 * self.num_cabinets

    @property
    def doorside_space(self):
        """The total space to the left, in between and right of the doors."""
        space = self.doorside_space_l + self.doorside_space_m + self.doorside_space_r
        return space

    @property
    def door_width(self):
        """The width of a single door.

        This function assumes there are exactly 2 doors per cabinet.
        """
        width = (self.cabinet_width - self.doorside_space) / 2
        return width

    @property
    def door_height(self):
        """The height of a single door."""
        height = self.cabinet_height - self.doortop_space
        return height


# cabinet.py ends here
