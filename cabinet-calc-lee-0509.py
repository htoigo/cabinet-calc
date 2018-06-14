#!/usr/bin/env python3

import argparse

from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Spacer
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

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
parser.add_argument("-m", "--material" ,
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

story = []
draw = []

draw.append(Paragraph("This text is generated in the 'draw' [list].", styleN))
story.append(Paragraph("This text is generated in the 'story' [list].", styleN))

cabCount = 1
#set max width of cabinets to 36" each
while (args.fulldim) / cabCount > 36:
     cabCount += 1
#determine individual cabinet dimention and chops off the remainder
cabDim = int(args.fulldim / cabCount)
#determine the remainder only
filler = (float(args.fulldim % cabCount))

print("Number of cabinets needed: " + str(cabCount))

# Print general breakdown of cabinet bank
print(str(cabCount) + " cabinets measuring " + str(cabDim) + '" totalling '
      + str(cabDim*cabCount) + '" with a ' + str(filler) + '" filler')
draw.append(Paragraph(str(cabCount) + " cabinets measuring " + str(cabDim)
                      + '" totalling ' + str(cabDim*cabCount) + '" with a '
                      + str(filler) + '" filler', styleN))

draw.append(Spacer(1,0.1*inch))

draw.append(Paragraph("Number of cabinets needed: " + str(cabCount), styleN))
draw.append(Paragraph("Each cabinet width: " + str(cabDim) + '"', styleN))

# Set part sizes
if args.thickness:
     print("Material thickness: " + str(args.thickness))
     draw.append(Paragraph("Material thickness: " + str(args.thickness) + '"', styleN))
else:
     args.thickness = float(0.75)
     print('Material thickness: 0.75"')
     draw.append(Paragraph('Material thickness: 0.75"', styleN))
     
# Subtract 0.875 (for the door and gap) and thickness of back panel
sideBottomEdge = (args.depth - 0.875) - args.thickness
bottomFront = cabDim - (args.thickness*2)

draw.append(Spacer(1,0.1*inch))
draw.append(Paragraph("PARTS LIST: ", styleH))

# Full back panels
print(str(cabCount) + " @ " + str(cabDim) + '" x ' + str(args.height) + '" x '
      + str(args.thickness) + '" -- BACK PNLS')
draw.append(Paragraph(str(cabCount) + " @ " + str(cabDim) + '" x '
                      + str(args.height) + '" x ' + str(args.thickness)
                      + '" -- BACK PNLS', styleN))
# Bottom panels minus thickness*2
print(str(cabCount) + " @ " + str(bottomFront) + '" x ' + str(sideBottomEdge)
      + '" x ' + str(args.thickness) + '" -- BOTTOM PNLS')
draw.append(Paragraph(str(cabCount) + " @ " + str(bottomFront) + '" x '
                      + str(sideBottomEdge) + '" x ' + str(args.thickness)
                      + '" -- BOTTOM PNLS', styleN))
# Side panels
print(str(cabCount*2) + " @ " + str(sideBottomEdge) + '" x ' + str(args.height)
      + '" x ' + str(args.thickness) + '" -- SIDE PNLS')
draw.append(Paragraph(str(cabCount*2) + " @ " + str(sideBottomEdge) + '" x '
                      + str(args.height) + '" x ' + str(args.thickness)
                      + '" -- SIDE PNLS', styleN))
# Top nailers minus thickness*2
print(str(cabCount*2) + " @ " + str(bottomFront) + '" x 4" x '
      + str(args.thickness) + '" -- TOP NAILERS')
draw.append(Paragraph(str(cabCount*2) + " @ " + str(bottomFront) + '" x 4" x '
      + str(args.thickness) + '" -- TOP NAILERS', styleN))

print(args.ctopright)
print(args.ctopleft)
print(args.ctopfront)

# Add countertop dimensions here including overhangs

# incorporate reportlab.pdfgen canvas definitions for parts
from reportlab.pdfgen import canvas
def back(c):
     from reportlab.lib.units import inch
     c.translate(inch,inch)
     c.setFont("Helvetica", 14)
     c.setStrokeColorRGB(0.1,0.1,0.1)
     c.setFillColorRGB(0.9,0.9,0.9)
     c.rect(0.1*inch,1*inch,cabDim*(inch*0.0625),args.height*(inch*0.0625), fill=1)
     c.drawString(0.1*inch,0.1*inch, (str(cabCount) + " Back Panels"))
c = canvas.Canvas("out3.pdf")
back(c)
c.showPage()
c.save()

#add some flowables
story.append(Paragraph(str(cabCount),styleH))
story.append(Paragraph("This is a paragraph in <i>Normal</i> style.",
                       styleN))
c  = Canvas('mydoc.pdf')
f = Frame(4*inch, inch, 4*inch, 4*inch, showBoundary=1)
f2 = Frame(inch, inch, 6.5*inch, 6.5*inch, showBoundary=1)
f.addFromList(story,c)
f2.addFromList(draw,c)
c.save()

