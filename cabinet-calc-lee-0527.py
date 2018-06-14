#!/usr/bin/env python3

import argparse
import math
from fractions import Fraction
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.pdfgen import pathobject
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import Color, red

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

# set to landscape orientation
lWidth, lHeight = letter

# ask for the job name
jobName = input('Enter a job name: ')

# ask if fillers are needed and how many
fillReq = int(input('How many fillers are needed? '))
print()
print('--------------------------------------------------------------')
print()
     
# let us set the scale for the drawn elements
i = inch
sc = 1/16

# set cabnet counter to starting point of 1
cabCount = 1
#set max width of cabinets to 36" each
while (args.fulldim) / cabCount > 36:
     cabCount += 1
#determine individual cabinet dimention and chops off the remainder
cabDim = float(args.fulldim / cabCount)
#determine the remainder only
filler = (float(args.fulldim % cabCount))
sideBottomEdge = (args.depth - 0.875) - args.thickness
bottomFrontEdge = int(cabDim) - (args.thickness*2)
# Doors
doorWDim = (int(cabDim) - 0.375) / 2
doorWWhole = int(doorWDim)
doorHDim = args.height - 0.5
details = []

print('OVERVIEW:')

def fillerDetail(frog):
     cabDim = float(args.fulldim / cabCount)
     fillSplit = float(filler/2)
     details.append('JOB NAME: ' + str(jobName))
     details.append('---------------------------------------')
     details.append('TOTAL WALL SPACE: ' + str(args.fulldim) + '"')
     if fillReq == 0:
          details.append(str(cabCount) + " CABINETS MEASURING " + str(cabDim)
                + '" TOTALING ' + str(cabDim*cabCount) + '"')
          details.append('WITH FINISHED END PANELS ON LEFT AND RIGHT')
          details.append('NO FILLER PANEL REQUIRED')
          # Full back panels
          details.append(str(cabCount) + " @ " + str(cabDim) + '" x ' 
                         + str(args.height) + '" x ' + str(args.thickness) 
                         + '" -- BACK PNLS')
          # Bottom panels minus thickness*2
          details.append(str(cabCount) + " @ " + str(bottomFrontEdge) + '" x '
                + str(sideBottomEdge) + '" x ' + str(args.thickness)
                + '" -- BOTTOM PNLS')
          # Side panels
          details.append(str(cabCount*2) + " @ " + str(sideBottomEdge) 
                         + '" x ' + str(args.height) + '" x ' 
                         + str(args.thickness) + '" -- SIDE PNLS')
          # Top nailers minus thickness*2
          details.append(str(cabCount*2) + " @ " + str(bottomFrontEdge) 
                         + '" x 4" x ' + str(args.thickness) 
                         + '" -- TOP NAILERS')
          for x in details:
               return x
          return details
     elif fillReq == 1:
          cabDim = int(cabDim)
          details.append(str(cabCount) + " CABINETS MEASURING " + str(cabDim) 
                         + '" TOTALLING ' + str(cabDim*cabCount) + '"')
          details.append('WITH A ' + str(filler) + '" FILLER')
          # Full back panels
          details.append(str(cabCount) + " @ " + str(cabDim) + '" x ' 
                         + str(args.height) + '" x ' + str(args.thickness) 
                         + '" -- BACK PNLS')
          # Bottom panels minus thickness*2
          details.append(str(cabCount) + " @ " + str(bottomFrontEdge) + '" x '
                + str(sideBottomEdge) + '" x ' + str(args.thickness)
                + '" -- BOTTOM PNLS')
          # Side panels
          details.append(str(cabCount*2) + " @ " + str(sideBottomEdge) + '" x '
                + str(args.height) + '" x ' + str(args.thickness)
                + '" -- SIDE PNLS')
          # Top nailers minus thickness*2
          details.append(str(cabCount*2) + " @ " + str(bottomFrontEdge) + '" x 4" x '
                + str(args.thickness) + '" -- TOP NAILERS')
          #return str(cabCount) + " cabinets @ " + str(cabDim) + '" totalling ' + str(cabDim*cabCount) + '" with a ' + str(filler) + '" filler'
          for x in details:
               return x
          return details
     elif fillReq == 2:
          cabDim = int(cabDim)
          details.append(str(cabCount) + " CABINETS MEASURING " + str(cabDim) + '" TOTALLING '
                + str(cabDim*cabCount) + '"')
          details.append('WITH TWO (2) ' + str(fillSplit) + '" FILLERS')
          # Full back panels
          details.append(str(cabCount) + " @ " + str(cabDim) + '" x ' + str(args.height)
                + '" x ' + str(args.thickness) + '" -- BACK PNLS')
          # Bottom panels minus thickness*2
          details.append(str(cabCount) + " @ " + str(bottomFrontEdge) + '" x '
                + str(sideBottomEdge) + '" x ' + str(args.thickness)
                + '" -- BOTTOM PNLS')
          # Side panels
          details.append(str(cabCount*2) + " @ " + str(sideBottomEdge) + '" x '
                + str(args.height) + '" x ' + str(args.thickness)
                + '" -- SIDE PNLS')
          # Top nailers minus thickness*2
          details.append(str(cabCount*2) + " @ " + str(bottomFrontEdge) + '" x 4" x '
                + str(args.thickness) + '" -- TOP NAILERS')
          for x in details:
               return x
          return details
     else:
          print('Your layout is complete dog shit.')
          print('Why would you have fillers in the middle of the run?')
          print('See Greg imediately...')
          print()
          print('On second thought, here\'s your cabinet run with NO fillers.')
          print('Zero!, Nada!, None! Take that...')
     return frog

# Print general breakdown of cabinet bank
print('--------------------------------------------------------------')

# Set part sizes
if args.thickness:
     print("Material thickness: " + str(args.thickness) + '"')
else:
     args.thickness = float(0.75)
     print('Material thickness: 0.75"')

print('--------------------------------------------------------------')
print('PARTS:')
print()

fillerDetail(fillReq)
for x in details:
     print(x)
     
# Subtract 0.875 (for the door and gap) and thickness of back panel
sideBottomEdge = (args.depth - 0.875) - args.thickness
bottomFrontEdge = cabDim - (args.thickness*2)


#***************** FIX THIS FRACTIONAL ISSUE************************** 
# Doors
doorWDim = (int(cabDim) - 0.375) / 2
doorWWhole = int(doorWDim)
doorHDim = args.height - 0.5

#***************** FIX THIS FRACTIONAL ISSUE**************************

doors = []
fillSplit = float(filler/2)
def doorDetail(toad):
     doors.append('DOOR DETAILS:')
     doors.append(str(cabCount*2) + " @ " + str(doorWDim) + '" x ' + str(doorHDim)
      + '" x ' + str(args.thickness) + '" -- DOORS ***FRACTION-('
      + str(doorWWhole) + '-' + str(Fraction(doorWDim % 1)) + '")')
     if fillReq == 0:
          doors.append('NO FILLER STRIPS')
     elif fillReq == 1:
          doors.append(str(fillReq) + " @ " + str(filler) + '" x '
           + str(args.height) + '" x ' + str(args.thickness) + '" -- FILLER')
     elif fillReq == 2:
          doors.append(str(fillReq) + " @ " + str(fillSplit) + '" x '
           + str(args.height) + '" x ' + str(args.thickness) + '" -- FILLERS')
     else:
          print('?')
     return doors
doorDetail(fillReq)
for z in doors:
     print(z)
print()
print('--------------------------------------------------------------')
print('COUNTERTOP DETAILS')
print(args.ctopright)
print(args.ctopleft)
print(args.ctopfront)


# Add countertop dimensions here including overhangs

# incorporate reportlab.pdfgen canvas definitions for parts
from reportlab.pdfgen import canvas

u = inch/16
iso45 = (math.sin(45)*args.depth/2)*u
isoNlr45 = (math.sin(45)*2)*u
nlr = 2*u

def isocab(c):
     from reportlab.lib.units import inch

     cabDim = float(args.fulldim / cabCount)
     
     if fillReq >= 1:
          cabDim = int(cabDim)
     else:
          cabDim = float(cabDim)
          
     u = inch/16
     isoLines = [
          # list of line coordinates in (x1,y1,x2,y2) format
          
          (args.thickness*u,args.thickness*u,
          (cabDim-(args.thickness))*u,args.thickness*u), #bottom inner line
          
          (args.thickness*u,0,
           args.thickness*u,args.height*u), #left inner line
          
          ((cabDim-args.thickness)*u,0,
          (cabDim-args.thickness)*u, (args.height)*u), #right inner line
          
          (args.thickness*u,(args.height-args.thickness)*u,
          (cabDim-args.thickness)*u,(args.height-args.thickness)*u), #top inner
          
          (args.thickness*u,args.thickness*u,
           iso45,iso45), #bottom left inner angle
          
          (0,args.height*u,
           iso45,(args.height*u + iso45)), #upper left angle

          (args.thickness*u,args.height*u,
           iso45,args.height*u + iso45 - args.thickness*u),#upperleft angle inner
           
          (iso45,args.height*u + iso45,
           cabDim*u + iso45,args.height*u + iso45), #horizontal top back
          
          (cabDim*u,args.height*u,
           cabDim*u + iso45,args.height*u + iso45), #upper right angle

          (cabDim*u - args.thickness*u,args.height*u,
           cabDim*u + iso45 - args.thickness*2*u,
           args.height*u + iso45 - args.thickness*u), #upper right angle inner
          
          (iso45,iso45,
           iso45,args.height*u-args.thickness*u), #inside vertical

          (cabDim*u,0,
           cabDim*u + iso45,iso45), #lower right angle

          (cabDim*u + iso45, iso45,
           cabDim*u + iso45, args.height*u + iso45), #vertical right back

          (cabDim*u + iso45 - args.thickness*u, iso45 - args.thickness*u,
           cabDim*u + iso45 - args.thickness*u,
           args.height*u + iso45 - args.thickness*u), #vertical right back inner

          (iso45 - args.thickness*u, args.height*u + iso45 - args.thickness*u,
           cabDim*u + iso45 - args.thickness*u,
           args.height*u + iso45 - args.thickness*u), #back bottom inner
          
          (iso45, iso45,
           cabDim*u - args.thickness*u, iso45), #inside horizontal

          (isoNlr45 + args.thickness*u, args.height*u + nlr,
           cabDim*u - args.thickness*u + isoNlr45,
           args.height*u + nlr), #front nailer horizontal

          (iso45 - isoNlr45,
           args.height*u + iso45 - isoNlr45 - args.thickness*u,
           cabDim*u + iso45 - isoNlr45 - args.thickness*2*u,
           args.height*u + iso45 - isoNlr45 - args.thickness*u),
          #horizontal back nailer

          (iso45 - isoNlr45,
           args.height*u + iso45 - isoNlr45 - args.thickness*2*u,
           cabDim*u + iso45 - isoNlr45 - args.thickness*3*u,
           args.height*u + iso45 - isoNlr45 - args.thickness*2*u),
          #horizontal back bottom nailer

          (iso45 - isoNlr45,
           args.height*u + iso45 - isoNlr45 - args.thickness*2*u,
           iso45 - isoNlr45,
           args.height*u + iso45 - isoNlr45 - args.thickness*u),
          #horizontal back nailer small upright
          
          (iso45,
           args.height*u + nlr,
           iso45,
           args.height*u + iso45 - isoNlr45 - args.thickness*2*u),
          # inside upper vertical
           
          ]
     
     c.translate(1*inch,lHeight - (args.height*u*3 + iso45/2))
     c.setLineWidth(1)
     c.setStrokeColor(colors.black)
     c.setFillColor(colors.black)
     # draw doors overprint
     red50transparent = Color( 100, 0, 0, alpha=0.5)
     c.setFillColor(red50transparent)
     c.setStrokeColor(red)
#     c.rect(-args.thickness*u,-args.thickness*u,doorWDim*u - 0.125*u,doorHDim*u,
#           fill=True, stroke=True)
#     c.rect(doorWDim*u - args.thickness*u + 0.125*u,-args.thickness*u,doorWDim*u - 0.25*u,
#           doorHDim*u, fill=True, stroke=True)
#     c.rect(0.125*u,0,doorWDim*u,doorHDim*u, fill=False, stroke=True)
#     c.rect(doorWDim*u + 0.125*u,0,doorWDim*u,doorHDim*u, fill=False, stroke=True)
     # dims on the drawing
     c.setFillColor(colors.black)
     c.setStrokeColor(colors.black)
     c.drawString(-0.5*inch, args.height*u/2, str(args.height) + '"')
     c.drawString(cabDim*u/2 - 0.1875*inch, -0.25*inch, str(cabDim) + '"')
     c.drawString(-15, args.height*u + iso45*u/8, str(args.depth) + '"')
     # main rect defining front of cabinet w,h
     c.rect(0,0,cabDim*u,args.height*u)
     # all secondary lines from isoLines [LIST] in isoCab function
     c.lines(isoLines)
     
def isoLables(f):
     f.translate(0.5*inch,lWidth/2 - 0.5*inch)
     f.setFont("Helvetica", 10)
     f.setStrokeColorRGB(0.1,0.1,0.1)
     f.setFillColorRGB(0.5,0.5,0.5)
     #f.drawString(2*inch,2*inch,"Number of cabinets needed: " + str(cabCount))
     #f.drawString(2*inch,2*inch, str(fillerDetail(fillReq)))
     #f.drawString(2*inch,1.75*inch,(str(cabCount) + " cabinets measuring "
                                    #+ str(cabDim) + '" totalling '
                                    #+ str(cabDim*cabCount) + '" with a '
                                    #+ str(filler) + '" filler'))
     x = 0.5*inch
     y = 0.5*inch
     for line in details:
          f.drawString(x,y, line)
          y = y - 0.25*inch

     for dline in doors:
          f.drawString(x,y, dline)
          y = y - 0.25*inch
     #f.drawString(2*inch,1.5*inch,"Number of cabinets needed: " + str(cabCount))
     #f.drawString(2*inch,1.25*inch,"Each cabinet width: " + str(cabDim) + '"')
     return f

     
# figuring angle lengths for iso-lines would incorporate a**2 + b**2 = c**2
     
def parts(c):
     from reportlab.lib.units import inch
     cabDim = float(args.fulldim / cabCount)
     if fillReq >= 1:
          cabDim = int(cabDim)
          bottomFrontEdge = cabDim - (args.thickness*2)
     else:
          cabDim = float(cabDim)
          bottomFrontEdge = cabDim - (args.thickness*2)
     xM = 4.75*inch
     c.translate(inch,inch)
     c.setFont("Helvetica", 12)
     c.setStrokeColor(colors.black)
     c.setFillColorRGB(0.5,0.5,0.5)
     # back panel
     c.rect(xM, 5*inch, cabDim*u, args.height*u,
            fill=0)
     c.drawString(xM + 0.125*inch, 5.125*inch, (str(cabCount)
                  + " Back Panels"))
     c.drawString(xM + cabDim*u + 0.1875*inch, 5*inch + args.height*u/2,
                  str(args.height) + '"')
     c.drawString(xM + (cabDim*u/2 - 0.1875*inch), 5*inch - 0.25*inch,
                  str(cabDim) + '"')
     # bottom panel
     c.rect(xM, 3*inch, bottomFrontEdge*u, sideBottomEdge*u, fill=0)
     c.drawString(xM + 0.125*inch, 3.125*inch, (str(cabCount)
                  + " Bottom Panels"))
     c.drawString(xM + bottomFrontEdge*u + 0.1875*inch, 3*inch
                  + sideBottomEdge*u/2, str(sideBottomEdge) + '"')
     c.drawString(xM + (bottomFrontEdge*u/2 - 0.1875*inch), 3*inch - 0.25*inch,
                  str(bottomFrontEdge) + '"')
     # side panel
     c.rect(xM, 1*inch, sideBottomEdge*u, args.height*u, fill=0)
     c.drawString(xM + 0.125*inch, 1.125*inch, (str(cabCount)
                  + " Side Panels"))
     c.drawString(xM + sideBottomEdge*u + 0.1875*inch, 1*inch
                  + args.height*u/2, str(sideBottomEdge) + '"')
     c.drawString(xM + (sideBottomEdge*u/2 - 0.1875*inch), 1*inch - 0.25*inch,
                  str(sideBottomEdge) + '"')
     # top nailers
     return c
print('--------------------------------------------------------------')
print('--------------------------------------------------------------')

c = canvas.Canvas("CabPARTS-" + jobName + ".pdf", pagesize=(letter))
c.setPageSize((lHeight, lWidth))
c.saveState()
isocab(c)
c.restoreState()
c.saveState()
isoLables(c)
c.restoreState()
parts(c)
#fillerDetail(c)
c.showPage()
c.save()
