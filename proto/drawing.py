#!/usr/bin/env python3

from reportlab.graphics.shapes import Drawing, Rect, Group, Line
from reportlab.lib import colors
from reportlab.graphics import renderPDF

import numpy as np

import cabinet

# Angle for isometric depth lines (in degrees)
iso_angle = 45

d = Drawing()

bottom_width = 33.5
bottom_depth = 22.375
bottom_thickness = 0.75
side_depth = 24
side_height = 28.5
side_thickness = 0.75

btmfront = Group(Rect(0, 0, bottom_width, bottom_thickness, strokeWidth=0.02,
                      fillColor=colors.white))
btmtop = Group(Rect(0, 0, bottom_width, bottom_depth,
                    strokeWidth=0.02, fillColor=colors.white))
btmtop.translate(0, bottom_thickness)
btmtop.shift(0, bottom_thickness)
btmtop.skew(iso_angle, 0)
btmright = Group(Rect(0, 0, bottom_depth, bottom_thickness,
                      strokeWidth=0.02, fillColor=colors.white))
btmright.translate(bottom_width, 0)
btmright.shift(bottom_width, 0)
btmright.skew(0, 90 - iso_angle)

d.add(btmfront)
d.add(btmtop)
d.add(btmright)

rightsidefront = Group(Rect(0, 0, side_thickness, side_height,
                            strokeWidth=0.02, fillColor=colors.white))
rightsidefront.translate(bottom_width, 0)
rightoutside = Group(Rect(0, 0, side_depth, side_height,
                          strokeWidth=0.02, fillColor=colors.white))
rightoutside.translate(bottom_width + side_thickness, 0)
rightoutside.shift(bottom_width + side_thickness, 0)
rightoutside.skew(0, 90 - iso_angle)
rightsidetop = Group(Rect(0, 0, side_thickness, side_depth,
                            strokeWidth=0.02, fillColor=colors.white))
rightsidetop.translate(bottom_width, side_height)
rightsidetop.shift(bottom_width, side_height)
rightsidetop.skew(iso_angle, 0)

# Comment out the following 3 lines to see the full bottom panel, which
# is partially hidden behind the side panel when it is drawn on top.
d.add(rightsidefront)
d.add(rightoutside)
d.add(rightsidetop)

d.translate(20, 20)

renderPDF.drawToFile(d, 'out/drawing.pdf', 'My first drawing')


cabs = cabinet.Run(247, 28.5, 24)

# 3D model of a cabinet is a graph of points (vertices), some of which are
# connected by lines (edges).

# Points (vertices) are numbered 0, 1, 2,..., in order from left to right, top
# to bottom, front to back. A point's number is its position in the list.

# Start with a cube:

#       +z
#        |
#        |
#        4---------5
#       /|        /|
#      / |       / |
#     0---------1  |
#     |  |      |  |
#     |  6------|--7----- +y
#     | /       | /
#     |/        |/
#     2---------3
#    /
#   /
#  +x

# The set of points is a list of triples.
cab_pts = [ (cabs.cabinet_depth, 0, cabs.cabinet_height)
            , (cabs.cabinet_depth, cabs.cabinet_width, cabs.cabinet_height)
            , (cabs.cabinet_depth, 0, 0)
            , (cabs.cabinet_depth, cabs.cabinet_width, 0)
            , (0, 0, cabs.cabinet_height)
            , (0, cabs.cabinet_width, cabs.cabinet_height)
            , (0, 0, 0)
            , (0, cabs.cabinet_width, 0)
          ]

# The set of edges is a list of adjacency lists containing the numbers of the
# points connected to the given point by lines.
cab_edges = [ [1, 2, 4]
              , [0, 3, 5]
              , [0, 3, 6]
              , [1, 2, 7]
              , [0, 5, 6]
              , [1, 4, 7]
              , [2, 4, 7]
              , [3, 5, 6]
            ]


def isometric_transform(pt_3D):
    """Isometrically transform a point in 3D space to one in 2D space."""
    pt_2D = (0, 0)
    return pt_2D


def isometric_view(obj):
    """Project a 3D object (a list of points) onto the yz-plane isometrically."""
    pts_2D = [isometric_transform(pt) for pt in obj]
    return pts_2D


def dedupBy(eq, items):
    """Remove duplicates from the list using the provided equality function."""
    if items == []:
        result = []
    else:
        result = [items[0]] + dedupBy(
            eq, list(filter(lambda x: not eq(items[0], x), items[1:])) )
    return result


def eq_lines(line1, line2):
    """Return True if two lines are equal, otherwise return False.

    Each line must be a pair of numbered vertices, e.g. (0, 1) indicating the
    line from vertex 0 to vertex 1, or (5, 3) indicating the line from vertex
    5 to vertex 3.
    """
    result = ( line1[0] == line2[0] and line1[1] == line2[1]
               or line1[0] == line2[1] and line1[1] == line2[0] )
    return result


d2 = Drawing()
# Construct a list of lines from the graph model of the cabinet:
lines = [(p1, p2) for p1 in range(len(cab_pts)) for p2 in cab_edges[p1]]
# Remove duplicate lines--e.g. (0, 1) and (1, 0) are the same line.
lines = dedupBy(eq_lines, lines)

# Change from vertex numbers to coordinates in 3D space
lines_3D = [(cab_pts[p1], cab_pts[p2]) for p1, p2 in lines]
print('lines_3D=' + str(lines_3D))

# Rotate


# Add all the lines to the drawing.
for p1, p2 in lines:
    d2.add(Line(cab_pts[p1][0], cab_pts[p1][1],
                cab_pts[p2][0], cab_pts[p2][1], strokeWidth=1))

# Move the cabinet away from the lower-left corner
d2.translate(40, 40)

renderPDF.drawToFile(d2, 'out/isoview.pdf', 'Isometric View of Cabinet')
