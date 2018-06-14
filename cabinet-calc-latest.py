#!/usr/bin/env python3

import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("fulldim",
                    help="Full bank measurement for all cabinets combined",
                    type=float)
parser.add_argument("height",
                    help="Height dim from toe kick to top of cabinet",
                    type=float)
parser.add_argument("depth",
                    help="Depth dimension from front to back including door",
                    type=float)
parser.add_argument("-m", "--material",
                    help="Primary building material name",
                    type=str)
parser.add_argument("-th", "--thickness",
                    help="Building material thickness",
                    type=float)
parser.add_argument("-ctl", "--ctopleft",
                    help="Countertop overhang left side",
                    type=float)
parser.add_argument("-ctr", "--ctopright",
                    help="Countertop overhang right side",
                    type=float)
parser.add_argument("-ctf", "--ctopfront",
                    help="Countertop overhang front side",
                    type=float)
args = parser.parse_args()

# The maximum width of a single cabinet is 36"
maxCabWidth = 36
cabCount = math.ceil(args.fulldim / maxCabWidth)

# Determine individual cabinet dimension and chop off the remainder
cabDim = args.fulldim // cabCount
# Determine the remainder only
filler = (float(args.fulldim % cabCount))

print("Number of cabinets needed: " + str(cabCount))
# Prints whole number cabinet dimension
print(str(cabDim) + '"')
# Print filler panel size
print(float(filler))
# Print general breakdown of cabinet bank
print(str(cabCount) + " cabinets measuring " + str(cabDim) + '" totalling '
      + str(cabDim*cabCount) + '" with a ' + str(filler) + '" filler')

# Set part sizes
if args.thickness:
    print("Material thickness: " + str(args.thickness))
else:
    args.thickness = float(0.75)
    print('Material thickness: 0.75"')
# Subtract 0.875 (for the door and gap) and thickness of back panel
sideBottomEdge = (args.depth - 0.875) - args.thickness
bottomFront = cabDim - (args.thickness*2)

# Full back panels
print(str(cabCount) + " @ " + str(cabDim) + '" x ' + str(args.height) + '" x '
      + str(args.thickness) + '" -- BACK PNLS')
# Bottom panels minus thickness*2
print(str(cabCount) + " @ " + str(bottomFront) + '" x ' + str(sideBottomEdge)
      + '" x ' + str(args.thickness) + '" -- BOTTOM PNLS')
# Side panels
print(str(cabCount*2) + " @ " + str(sideBottomEdge) + '" x ' + str(args.height)
      + '" x ' + str(args.thickness) + '" -- SIDE PNLS')
# Top nailers minus thickness*2
print(str(cabCount*2) + " @ " + str(bottomFront) + '" x 4" x '
      + str(args.thickness) + '" -- TOP NAILERS')

print(args.ctopright)
print(args.ctopleft)
print(args.ctopfront)

# Add countertop dimensions here including overhangs
