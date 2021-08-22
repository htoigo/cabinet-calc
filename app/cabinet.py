# cabinet.py        -*- coding: utf-8 -*-

# The `cabinet' module for Cabinet Calc, which computes all cabinet specs.

# Copyright © 2018  Harry H. Toigo II, L33b0

# This file is part of Cabinet Calc, the custom Euro-style cabinet configurator.

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


"""Cabinet Calc cabinet module.

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


# __all__ = [MAX_CABINET_WIDTH, DOOR_HINGE_GAP, cabinet_run, num_cabinets,
#            Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'


import math
from enum import Enum


# Module constants

# All measurements are in inches, unless otherwise specified.

MAX_CABINET_WIDTH = 36.0
MIN_FILLER_WIDTH = 1.0
MAX_FILLER_WIDTH = 4.0

# The gap between the back of the door and the front of the cabinet,
# due to the hinges.
DOOR_HINGE_GAP = 0.125

# List of materials

# The list order is the order they will appear in the selection list.
# The default primary material is Standard Plywood, if none is specified.
MATERIALS = ['Standard Plywood',
             'Marine-Grade Plywood',
             'Melamine']

# Material abbreviations to be used where full names will not fit.
MATL_ABBREVS = {'Standard Plywood': 'PLY',
                'Marine-Grade Plywood': 'MarPLY',
                'Melamine': 'MEL'}

# Primary material defaults to Standard Plywood.
PRIM_MAT_DEFAULT = 0

# Door material defaults to Melamine.
DOOR_MAT_DEFAULT = 2

# Dictionary of materials with default thicknesses for each in inches.

# Each material has two default thicknesses: the default thickness generally
# used for cabinet panels, and the default thickness for bottom panels when
# legs will be attached, which need to be thicker than 3/4" so that the leg
# screws can grab.

# Note: these thicknesses must still be changeable to something else, as lots
# do vary in thickness. For example, gray melamine lots are often 0.74" thick.

MATL_THICKNESSES = {'Standard Plywood': (0.74, [0.74, 0.74]),
                    'Marine-Grade Plywood': (0.75, [0.75, 0.75]),
                    'Melamine': (0.76, [1.0])}


class Ends(Enum):
    """An enumeration of the allowable choices for which end or ends of a
    cabinet run have fillers.

    It must be one of:
        NEITHER - no fillers used
        LEFT - only the left end has a filler
        RIGHT - only the right end has a filler
        BOTH - both ends have fillers

    This also determines whether or not the end panels must be finished. If an
    end will have a filler then that end can be left unfinished. On the other
    hand, an end without a filler must have a finished end panel.
    """
    NEITHER = 1
    LEFT = 2
    RIGHT = 3
    BOTH = 4

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(string):
        """Convert the given string to the appropriate Ends value."""
        try:
            return Ends[string]
        except KeyError as exc:
            raise ValueError('Failed to convert string to Ends value') from exc


def cabinet_run(
        fullwidth, height, depth, fillers=Ends.NEITHER,
        prim_material=MATERIALS[PRIM_MAT_DEFAULT],
        prim_thickness=MATL_THICKNESSES[MATERIALS[PRIM_MAT_DEFAULT]][0],
        door_material=MATERIALS[DOOR_MAT_DEFAULT],
        door_thickness=MATL_THICKNESSES[MATERIALS[DOOR_MAT_DEFAULT]][0],
        bottom_thickness=None,
        has_legs=False,
        topnailer_depth=4,
        doortop_space=0.5, doorside_space_l=0.125,
        doorside_space_m=0.125, doorside_space_r=0.125):
    """Construct a (single) :class:`Run <Run>` of cabinets.

    :param fullwidth: Total wall width for this run of cabinets.
    :param height: The distance from the toe kick to top of cabinets.
    :param depth: The distance from front to back, including door.
    :param fillers: Which ends of the run will have fillers.
    :param prim_material: The primary building material name.
    :param prim_thickness: Primary building material thickness.
    :param door_material: The door material name.
    :param door_thickness: The door material thickness.
    :param bottom_thickness: The bottom may be thicker and stacked.
    :return: :class:`Run <Run>` object
    :rtype: cabinet.Run
    """
    return Run(fullwidth, height, depth, fillers,
               prim_material, prim_thickness,
               door_material, door_thickness,
               bottom_thickness, has_legs,
               topnailer_depth, doortop_space, doorside_space_l,
               doorside_space_m, doorside_space_r)


# Should we expose the following functions for ad hoc use?
#
# def num_cabinets(full_width, fillers):
#     return result
#
# def cabinet_width(full_width, fillers):
#     return result
#
# def extra_width(full_width, fillers):
#     return result


class Run():
    """A class representing a single run of cabinets.

    Args:
        fullwidth: Full bank width available for all cabinets combined.
        height: The height from toe kick to top of cabinets.
        depth: Depth from front to back, including the door.
        fillers: Which ends will have filler panels.
        prim_material: Primary material name.
        prim_thickness: Primary material thickness (float).
            Defaults to the standard thickness of the primary material.
        door_material: Door material name.
        door_thickness: Door material thickness (float).
            Defaults to standard thickness of the chosen door material.
        btmpanel_thicknesses: List of bottom panel thicknesses, in order from
            top to bottom. Defaults to a singleton list containing the primary
            material thickness, if the cabinets will not have legs attached, or
            if they will, to the list of stacked panels for the primary
            material.
        has_legs: True if the cabinets will have legs.

    At the moment this class assumes that there are exactly two doors per
    cabinet, as does all code in this module. We may change this later to
    allow single-door cabinets, but that will require a lot of changes.
    """
    def __init__(self, fullwidth, height, depth, fillers=Ends.NEITHER,
                 prim_material=MATERIALS[PRIM_MAT_DEFAULT],
                 prim_thickness=None,
                 door_material=MATERIALS[DOOR_MAT_DEFAULT],
                 door_thickness=None,
                 btmpanel_thicknesses=None,
                 has_legs=False,
                 topnailer_depth=4,
                 doortop_space=0.5, doorside_space_l=0.125,
                 doorside_space_m=0.125, doorside_space_r=0.125):
        self._fullwidth = fullwidth
        self._height = height
        self._depth = depth
        # fillers must be one of: Ends.NEITHER, Ends.LEFT, Ends.RIGHT, or
        # Ends.BOTH.
        self.fillers = fillers
        self.prim_material = prim_material
        if prim_thickness is not None:
            self.prim_thickness = prim_thickness
        else:
            self.prim_thickness = MATL_THICKNESSES[self.prim_material][0]
        self.door_material = door_material
        if door_thickness is not None:
            self.door_thickness = door_thickness
        else:
            self.door_thickness = MATL_THICKNESSES[self.door_material][0]
        self._has_legs = has_legs
        if btmpanel_thicknesses is not None:
            self.btmpanel_thicknesses = btmpanel_thicknesses
        else:
            if self.has_legs:
                self.btmpanel_thicknesses = MATL_THICKNESSES[
                    self.prim_material][1]
            else:
                self.btmpanel_thicknesses = [self.prim_thickness]
        self.topnailer_depth = topnailer_depth
        # How much the door is shorter than the cabinet, usually 1/2" or 3/8".
        self.doortop_space = doortop_space
        # The space to the left, in between, and to the right of the doors.
        # These three spaces are usually all 1/8".
        self.doorside_space_l = doorside_space_l
        self.doorside_space_m = doorside_space_m
        self.doorside_space_r = doorside_space_r

    @property
    def fullwidth(self):
        """The total wall width for this run of cabinets."""
        return self._fullwidth

    @fullwidth.setter
    def fullwidth(self, value):
        self._fullwidth = value

    @fullwidth.deleter
    def fullwidth(self):
        del self._fullwidth

    @property
    def num_cabinets(self):
        """Compute the number of cabinets needed for the given wall width.

        Return the smallest number of cabinets needed, while not exceeding the
        maximum cabinet width.
        """
        return int(math.ceil(self.fullwidth / MAX_CABINET_WIDTH))

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
        """The width of each individual cabinet in this run."""
        if self.num_fillers == 0:
            # With no fillers, we have no choice about the cabinet width.
            width = self._fullwidth / self.num_cabinets
        else:
            # Restrict cabinet width to an easy-to-cut value, if possible,
            # while keeping filler widths within allowable range. We start with
            # integral values for the cabinet width.
            width = self._fullwidth // self.num_cabinets
            filler_w = ((self._fullwidth - width * self.num_cabinets)
                        / self.num_fillers)
            delta = 1.0
            while filler_w < MIN_FILLER_WIDTH:
                width -= delta
                filler_w = ((self._fullwidth - width * self.num_cabinets)
                            / self.num_fillers)
            while filler_w > MAX_FILLER_WIDTH:
                delta /= 2
                width += delta
                filler_w = ((self._fullwidth - width * self.num_cabinets)
                            / self.num_fillers)
        return width

    @property
    def extra_width(self):
        """The extra space beside the cabinets, to be filled by fillers."""
        # return self._fullwidth % self.num_cabinets
        return self._fullwidth - self.num_cabinets * self.cabinet_width

    @property
    def num_fillers(self):
        """The number of fillers to be used in this run of cabinets."""
        if self.fillers is Ends.NEITHER:
            result = 0
        elif self.fillers is Ends.LEFT or self.fillers is Ends.RIGHT:
            result = 1
        elif self.fillers is Ends.BOTH:
            result = 2
        else:
            raise TypeError('fillers is not one of Ends.neither, Ends.left,'
                            'Ends.right, or Ends.both')
        return result

    @property
    def filler_width(self):
        """The width of the filler(s) to be used in the run."""
        if self.fillers is Ends.NEITHER:
            width = None
        else:
            width = self.extra_width / self.num_fillers
        return width

    @property
    def filler_height(self):
        """The height of the filler(s) to be used in the run."""
        if self.fillers is Ends.NEITHER:
            height = None
        else:
            height = self.cabinet_height
        return height

    @property
    def filler_thickness(self):
        """The thickness of a filler strip."""
        if self.fillers is Ends.NEITHER:
            thickness = None
        else:
            thickness = self.prim_thickness
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
        return self.prim_thickness

    @property
    def has_legs(self):
        """True if the cabinet run will have legs, False otherwise."""
        return self._has_legs

    @has_legs.setter
    def has_legs(self, value):
        if self._has_legs != value:
            self._has_legs = value
            if self._has_legs:
                # Just added legs; this requires a thicker bottom, which may be
                # stacked panels depending on the material, so use a list.
                self.btmpanel_thicknesses = MATL_THICKNESSES[self.prim_material][1]
            else:
                # Just removed legs; bottom thickness can be same as primary
                # material thickness (still a list).
                self.btmpanel_thicknesses = [self.prim_thickness]

    @has_legs.deleter
    def has_legs(self):
        del self._has_legs

    @property
    def btmpanels_per_cab(self):
        """Return the number of bottom panels per cabinet."""
        return len(self.btmpanel_thicknesses)

    @property
    def bottom_stacked(self):
        """Return True if the run will have stacked bottom panels."""
        return self.btmpanels_per_cab > 1

    @property
    def num_bottompanels(self):
        """The number of bottom panels needed for the entire run."""
        return self.btmpanels_per_cab * self.num_cabinets

    @property
    def bottom_thickness(self):
        """The total thickness of all bottom panels in a single cabinet."""
        return sum(self.btmpanel_thicknesses)

    @bottom_thickness.setter
    def bottom_thickness(self, value):
        if 0.375 < value < 1.375:
            self.btmpanel_thicknesses = [value]
        elif value < 1.625:
            self.btmpanel_thicknesses = [0.75, 0.75]
        elif value < 1.875:
            self.btmpanel_thicknesses = [0.75, 1.0]
        elif value < 2.125:
            self.btmpanel_thicknesses = [1.0, 1.0]
        else:
            raise ValueError('bottom thickness is not between 1/2" and 2"')

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
    def num_sidepanels(self):
        """The number of side panels needed for this run."""
        return 2 * self.num_cabinets

    @property
    def side_depth(self):
        """The depth (front to back) of a side panel.

        Side panel depth is cabinet depth, less thickness of door and gap, less
        thickness of back panel.
        """
        depth = (self.cabinet_depth - (self.door_thickness + DOOR_HINGE_GAP)
                 - self.back_thickness)
        return depth

    @property
    def side_height(self):
        """The height of a side panel."""
        return self.cabinet_height

    @property
    def side_thickness(self):
        """The thickness of a side panel."""
        return self.prim_thickness

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
        """The thickness of a top nailer panel."""
        return self.prim_thickness

    @property
    def num_doors(self):
        """The number of doors needed for this run.

        This function assumes there are exactly 2 doors per cabinet. This may
        change later.
        """
        return 2 * self.num_cabinets

    @property
    def doorside_space(self):
        """The total space to the left, in between and right of the doors."""
        space = (self.doorside_space_l + self.doorside_space_m
                 + self.doorside_space_r)
        return space

    @property
    def door_width(self):
        """The width of a single door.

        This function assumes there are exactly 2 doors per cabinet. This may
        change later.
        """
        width = (self.cabinet_width - self.doorside_space) / 2
        return width

    @property
    def door_height(self):
        """The height of a single door."""
        height = self.cabinet_height - self.doortop_space
        return height


# cabinet.py ends here
