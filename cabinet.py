# -*- coding: utf-8 -*-

"""
cabinet.api
~~~~~~~~~~~

This module implements the Cabinet module API.

:copyright: (c) 2018 by Lee Bernard, Harry H. Toigo II.
:license: MIT, see LICENSE file for more details.

Given the full width, height, depth, material, material thickness, and
number of fillers to use, (along with job name)...

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

# Module constants

# All measurements are in inches, unless otherwise specified.

max_cabinet_width = 36

# The gap between the back of the door and the front of the cabinet,
# due to the hinges.
door_hinge_gap = 0.125


def cabinet_run(fullwidth, height, depth, num_fillers=0, material='Plywood',
                matl_thickness=0.75, topnailer_depth=4, door_thickness=0.75,
                doortop_space=0.5, doorside_space_l=0.125,
                doorside_space_m=0.125, doorside_space_r=0.125):
    """Construct a (single) :class:`Run <Run>` of cabinets.

    :param fullwidth: Total wall width for this run of cabinets.
    :param height: The distance from the toe kick to top of cabinets.
    :param depth: The distance from front to back, including door.
    :param num_fillers: The number of fillers to use in this run.
    :param material: The primary building material name.
    :param matl_thickness: Building material thickness.
    :return: :class:`Run <Run>` object
    :rtype: cabinet.Run
    """
    return Run(fullwidth, height, depth, num_fillers, material, matl_thickness,
               topnailer_depth, door_thickness, doortop_space, doorside_space_l,
               doorside_space_m, doorside_space_r)


# Should we expose the following functions for ad hoc use?


def num_cabinets(full_width):
    """Compute the number of cabinets needed for the given wall width.

    Return the smallest number of cabinets needed, while not exceeding the
    maximum cabinet width.
    """
    return math.ceil(full_width / max_cabinet_width)


# def cabinet_width(full_width, num_cabinets):
#     result = 0
#     return result

# def extra_width(full_width, num_cabinets):
#     result = 0
#     return result


class Run:
    """A single run of cabinets (lower or upper)."""

    def __init__(self, fullwidth, height, depth, num_fillers=0,
                 material='Plywood', matl_thickness=0.75, topnailer_depth=4,
                 door_thickness=0.75, doortop_space=0.5, doorside_space_l=0.125,
                 doorside_space_m=0.125, doorside_space_r=0.125):
        self._fullwidth = fullwidth
        self._height = height
        self._depth = depth
        self._num_fillers = num_fillers
        self._material = material
        self._matl_thickness = matl_thickness
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
        """The number of cabinets needed for the run.

        This function uses the module global function `num_cabinets', to avoid
        duplication of code.
        """
        return num_cabinets(self._fullwidth)

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
        if self._num_fillers == 0:
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
        """The number of fillers to be used in this run."""
        return self._num_fillers

    @property
    def filler_width(self):
        """The width of the filler(s) to be used in the run."""
        if self._num_fillers == 0:
            width = 0    # or raise exception here?
        else:
            # Should we raise an exception if more than 2 fillers?
            width = self.extra_width / self.num_fillers
        return width

    @property
    def filler_height(self):
        """The height of the filler(s) to be used in the run."""
        if self._num_fillers == 0:
            height = 0    # or raise exception here?
        else:
            # Should we raise an exception if more than 2 fillers?
            height = self.cabinet_height
        return height

    @property
    def filler_thickness(self):
        """The thickness of a filler strip."""
        if self._num_fillers == 0:
            thickness = 0    # or raise exception here?
        else:
            # Should we raise an exception if more than 2 fillers?
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


class Job:
    """A customer job."""

    def __init__(self, name):
        self.name = name
