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


# __all__ = [max_cabinet_width, door_hinge_gap, cabinet_run, num_cabinets,
#            Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'


import math
from enum import Enum


# Module constants
# All measurements are in inches, unless otherwise specified.


max_cabinet_width = 36.0
min_filler_width = 1.0
max_filler_width = 4.0

# The gap between the back of the door and the front of the cabinet,
# due to the hinges.
door_hinge_gap = 0.125

# The default space to the left, to the right, and between the cabinet doors.
doortop_space_default = 0.5
doorside_space_l_default = 0.125
doorside_space_m_default = 0.125
doorside_space_r_default = 0.125

# Most common countertop overhang dimensions and thickness.
ctop_ovrhang_l_default = 2.0
ctop_ovrhang_r_default = 2.0
ctop_ovrhang_f_default = 2.0
ctop_thickness_default = 1.5

# Most common toe kick height and style.
toekick_ht_default = 6.0
toekick_style_default = 'box_frame'

# Top nailer default depth.
topnailer_depth_default = 4.0


# List of materials

# The list order is the order they will appear in the selection list.
# The default primary material is Standard Plywood, if none is specified.
materials = ['Standard Plywood',
             'Marine-Grade Plywood',
             'Melamine']

# Material abbreviations to be used where full names will not fit.
matl_abbrevs = {'Standard Plywood': 'PLY',
                'Marine-Grade Plywood': 'MarPLY',
                'Melamine': 'MEL'}

# Primary material defaults to Standard Plywood.
prim_mat_default = 0

# Door material defaults to Melamine.
door_mat_default = 2

# Dictionary of materials with default thicknesses for each in inches.

# Each material has two default thicknesses: the default thickness generally
# used for cabinet panels, and the default thickness for bottom panels when
# legs will be attached, which need to be thicker than 3/4" so that the leg
# screws can grab.

# Note: these thicknesses must still be changeable to something else, as lots
# do vary in thickness. For example, gray melamine lots are often 0.74" thick.

matl_thicknesses = {'Standard Plywood': (0.74, [0.74, 0.74]),
                    'Marine-Grade Plywood': (0.75, [0.75, 0.75]),
                    'Melamine': (0.76, [1.0])}


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


def cabinet_run(
        fullwidth, height, depth, fillers=Ends.neither,
        prim_material=materials[prim_mat_default],
        prim_thickness=matl_thicknesses[materials[prim_mat_default]][0],
        door_material=materials[door_mat_default],
        door_thickness=matl_thicknesses[materials[door_mat_default]][0],
        bottom_thickness=None,
        has_legs=False,
        ctop_ovr_l=ctop_ovrhang_l_default,
        ctop_ovr_r=ctop_ovrhang_r_default,
        ctop_ovr_f=ctop_ovrhang_f_default,
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
    :param has_legs: True if the cabinet run will have legs.
    :type has_legs: bool
    :param ctop_ovr_l: Length of countertop overhang on left.
    :type ctop_ovr_l: float
    :param ctop_ovr_r: Length of countertop overhang on right.
    :type ctop_ovr_r: float
    :param ctop_ovr_f: Length of countertop overhang in front.
    :type ctop_ovr_f: float
    :return: :class:`Run <Run>` object
    :rtype: cabinet.Run
    """
    return Run(fullwidth, height, depth, fillers,
               prim_material, prim_thickness,
               door_material, door_thickness,
               bottom_thickness, has_legs,
               ctop_ovr_l, ctop_ovr_r, ctop_ovr_f,
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


# At the moment the Run class assumes that there are exactly two doors per
# cabinet, as does all code in this module. We may change this later to
# allow single-door cabinets, but that will require a lot of changes.

class Run(object):
    """A class representing a single run (bank) of cabinets.

    :param dimension_base: What the given dimensions are based on.
        Either 'countertop' or 'cab_bank'.
    :type dimension_base: str
    :param fullwidth: Full bank width available for all cabinets combined,
        including countertop.
    :type fullwidth: float
    :param height: The height from toe kick to top of cabinets.
    :type height: float
    :param depth: Depth from front to back of the countertop, which extends
        past the front of the door by the overhang amount.
    :type depth: float
    :param ctop_ovr_l: Length of countertop overhang on left.
    :type ctop_ovr_l: float
    :param ctop_ovr_r: Length of countertop overhang on right.
    :type ctop_ovr_r: float
    :param ctop_ovr_f: Length of countertop overhang in front.
    :type ctop_ovr_f: float
    :param ctop_thickness: The countertop thickness.
    :type ctop_thickness: float
    :param fillers: Which ends will have filler panels.
    :type fillers: Ends
    :param prim_material: Primary material name.
    :type prim_material: str
    :param prim_thickness: Primary material thickness.
    :type prim_thickness: float
    :param door_material: Door material name.
    :type door_material: str
    :param door_thickness: Door material thickness.
    :type door_thickness: float
    :param toekick_style: The style of toe kick, either plywood 'box_frame' or
        stainless 'steel_legs'.
    :type toekick_style: str
    :param toekick_ht: The height of the toe kick.
    :type toekick_ht: float
    :param btmpanel_thicknesses: List of bottom panel thicknesses, in order
        from top to bottom. Defaults to a singleton list containing the primary
        material thickness, if the cabinets will not have legs attached, or if
        they will, to the list of stacked panels for the primary material.
    :type btmpanel_thicknesses: list[>0](float)
    :param topnailer_depth: The depth of the top nailers.
    :type topnailer_depth: float
    :param doortop_space: The space between top of cabinet and top of door.
    :type doortop_space: float
    :param doorside_space_l: The space to the left of the doors.
    :type doorside_space_l: float
    :param doorside_space_m: The space in the middle between the doors.
    :type doorside_space_m: float
    :param doorside_space_r: The space to the right of the doors.
    :type doorside_space_r: float
    """
    def __init__(self, dimension_base,
                 fullwidth, height, depth,
                 ctop_ovr_l=ctop_ovrhang_l_default,
                 ctop_ovr_f=ctop_ovrhang_f_default,
                 ctop_ovr_r=ctop_ovrhang_r_default,
                 ctop_thickness=ctop_thickness_default,
                 fillers=Ends.neither,
                 prim_material=materials[prim_mat_default],
                 prim_thickness=None,
                 door_material=materials[door_mat_default],
                 door_thickness=None,
                 toekick_style=toekick_style_default,
                 toekick_ht=toekick_ht_default,
                 btmpanel_thicknesses=None,
                 topnailer_depth=topnailer_depth_default,
                 doortop_space=doortop_space_default,
                 doorside_space_l=doorside_space_l_default,
                 doorside_space_m=doorside_space_m_default,
                 doorside_space_r=doorside_space_r_default):
        self._fullwidth = fullwidth
        self._height = height
        self._depth = depth
        self._ctop_ovr_l = ctop_ovr_l
        self._ctop_ovr_r = ctop_ovr_r
        self._ctop_ovr_f = ctop_ovr_f
        # fillers must be one of: Ends.neither, Ends.left, Ends.right, or
        # Ends.both.
        self.fillers = fillers
        self.prim_material = prim_material
        if prim_thickness is not None:
            self.prim_thickness = prim_thickness
        else:
            self.prim_thickness = matl_thicknesses[self.prim_material][0]
        self.door_material = door_material
        if door_thickness is not None:
            self.door_thickness = door_thickness
        else:
            self.door_thickness = matl_thicknesses[self.door_material][0]
        self._has_legs = has_legs
        if btmpanel_thicknesses is not None:
            self.btmpanel_thicknesses = btmpanel_thicknesses
        else:
            if self.has_legs:
                self.btmpanel_thicknesses = matl_thicknesses[
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
    def height(self):
        return self._height

    @property
    def depth(self):
        """The overall depth, usually the depth of the countertop."""
        return self._depth

    @property
    def ctop_ovr_l(self):
        return self._ctop_ovr_l

    @property
    def ctop_ovr_r(self):
        return self._ctop_ovr_r

    @property
    def ctop_ovr_f(self):
        return self._ctop_ovr_f

    @property
    def num_cabinets(self):
        """Compute the number of cabinets needed for the given wall width.

        The countertop overhang on left and right reduces the available width
        for cabinet boxes.
        Return the smallest number of cabinets needed, while not exceeding the
        maximum cabinet width.
        """
        overhang = self._ctop_ovr_l + self._ctop_ovr_r
        return int(math.ceil((self._fullwidth - overhang) / max_cabinet_width))

    @property
    def cabinet_height(self):
        """The overall cabinet height."""
        return self._height

    @property
    def cabinet_depth(self):
        """The depth of the cabinets, including doors."""
        return self._depth - self._ctop_ovr_f

    @property
    def cabinet_width(self):
        """The width of each individual cabinet in this run."""
        all_cabs_width = self._fullwidth - self._ctop_ovr_l - self._ctop_ovr_r
        if self.num_fillers == 0:
            # With no fillers, we have no choice about the cabinet width.
            width = (all_cabs_width) / self.num_cabinets
        else:
            # Restrict cabinet width to an easy-to-cut value, if possible,
            # while keeping filler widths within allowable range. We start with
            # integral values for the cabinet width.
            width = all_cabs_width // self.num_cabinets
            filler_w = ((all_cabs_width - width * self.num_cabinets)
                        / self.num_fillers)
            delta = 1.0
            while filler_w < min_filler_width:
                width -= delta
                filler_w = ((all_cabs_width - width * self.num_cabinets)
                            / self.num_fillers)
            while filler_w > max_filler_width:
                delta /= 2
                width += delta
                filler_w = ((all_cabs_width - width * self.num_cabinets)
                            / self.num_fillers)
        return width

    @property
    def extra_width(self):
        """The extra space beside the cabinets, to be filled by fillers."""
        return self._fullwidth - self.cabinet_width * self.num_cabinets

    @property
    def num_fillers(self):
        if self.fillers is Ends.neither:
            result = 0
        elif self.fillers is Ends.left or self.fillers is Ends.right:
            result = 1
        elif self.fillers is Ends.both:
            result = 2
        else:
            raise TypeError('fillers is not one of Ends.neither, Ends.left,'
                            'Ends.right, or Ends.both')
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
                self.btmpanel_thicknesses = matl_thicknesses[
                    self.prim_material][1]
            else:
                # Just removed legs; bottom thickness can be same as primary
                # material thickness (still a list).
                self.btmpanel_thicknesses = [self.prim_thickness]

    @has_legs.deleter
    def has_legs(self):
        del self._has_legs

    @property
    def btmpanels_per_cab(self):
        return len(self.btmpanel_thicknesses)

    @property
    def bottom_stacked(self):
        return (self.btmpanels_per_cab > 1)

    @property
    def num_bottompanels(self):
        """The number of bottom panels needed for the entire run."""
        return (self.btmpanels_per_cab * self.num_cabinets)

    @property
    def bottom_thickness(self):
        """The total thickness of all bottom panels in a single cabinet."""
        return sum(self.btmpanel_thicknesses)

    @bottom_thickness.setter
    def bottom_thickness(self, value):
        if value > 0.375 and value < 1.375:
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
