#!/usr/bin/env python3

from reportlab.graphics.shapes import Drawing, Rect, Group
from reportlab.lib import colors
from reportlab.graphics import renderPDF

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
