# matrix_ops.py

from math import sin, cos, atan, pi, sqrt
import numpy as np

from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib import colors
from reportlab.graphics import renderPDF

import cabinet

debug = True

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

# A rotation of -45 degrees (negative means clockwise) around the vertical z-axis,
# followed by a 35.264 degrees (arctan (1/sqrt(2))) rotation around the horizontal
# y-axis, followed by an orthographic projection to the yz-plane.

z_rot = np.array( [[cos(-pi/4), -sin(-pi/4), 0],
                   [sin(-pi/4),  cos(-pi/4), 0],
                   [0,           0,          1]] )

theta = atan(1 / sqrt(2))
y_rot = np.array( [[ cos(theta),  0,  sin(theta)],
                   [ 0,           1,  0         ],
                   [-sin(theta),  0,  cos(theta)]] )

cabs = cabinet.Run(180, 28.5, 24)

cab_pts = [ (cabs.cabinet_depth/2, -cabs.cabinet_width/2, cabs.cabinet_height/2)
            , (cabs.cabinet_depth/2, cabs.cabinet_width/2, cabs.cabinet_height/2)
            , (cabs.cabinet_depth/2, -cabs.cabinet_width/2, -cabs.cabinet_height/2)
            , (cabs.cabinet_depth/2, cabs.cabinet_width/2, -cabs.cabinet_height/2)
            , (-cabs.cabinet_depth/2, -cabs.cabinet_width/2, cabs.cabinet_height/2)
            , (-cabs.cabinet_depth/2, cabs.cabinet_width/2, cabs.cabinet_height/2)
            , (-cabs.cabinet_depth/2, -cabs.cabinet_width/2, -cabs.cabinet_height/2)
            , (-cabs.cabinet_depth/2, cabs.cabinet_width/2, -cabs.cabinet_height/2)
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

# Construct a list of lines from the graph model of the cabinet:
lines = [(p1, p2) for p1 in range(len(cab_pts)) for p2 in cab_edges[p1]]

# Change from vertex numbers to coordinates in 3D space
lines_3D = [(cab_pts[p1], cab_pts[p2]) for p1, p2 in lines]
if debug:
    print('lines_3D=' + str(lines_3D))

# Rotate & project
isometric_lines = [
    (tuple(np.matmul(y_rot, np.matmul(z_rot, p1))[1:].tolist())
     , tuple(np.matmul(y_rot, np.matmul(z_rot, p2))[1:].tolist()))
    for p1, p2 in lines_3D ]

if debug:
    print('isometric_lines=' + str(isometric_lines))

d2 = Drawing()

# Add all the lines to the drawing.
for p1, p2 in isometric_lines:
    d2.add(Line(p1[0], p1[1], p2[0], p2[1], strokeWidth=0.3))

# Move the cabinet away from the lower-left corner
d2.translate(40, 40)

renderPDF.drawToFile(d2, 'rotated.pdf', 'Rotated View of Cabinet')

# matrix_ops.py ends here
