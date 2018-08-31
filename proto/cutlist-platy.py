# cutlist-platy.py    -*- coding: utf-8 -*-

import math
from functools import reduce

from reportlab.pdfgen import canvas as canv
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, \
                               PageTemplate, Frame, Paragraph, Spacer, \
                               FrameBreak
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

import cabinet as cab
import job


def unlines(lines):
    """Join a list of lines, after appending a newline to each."""
    nlines = map(lambda s: s + '\n', lines)
    str = reduce(lambda s, t: s+t, nlines, '')
    return str


def landscape(pagesize):
    """Return pagesize in landscape mode (with width and height reversed)."""
    w, h = pagesize
    return (h, w)


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 16)
    canvas.drawCentredString(page_width / 2.0, page_ht - inch, title)
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, 'First Page / {}'.format(pageinfo))
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, 'Page {} {}'.format(doc.page, pageinfo))
    canvas.restoreState()


def go():
    doc = BaseDocTemplate('platy-doc.pdf', showBoundary=1,
                          pagesize=landscape(letter))

    hdr_ht = 45           # pts   6 + 12 + 3 + 12 + 3 + 6
    spc_after_hdr = 12    # pts
    frameHdr = Frame(doc.leftMargin, page_ht - doc.topMargin - hdr_ht,
                     doc.width, hdr_ht,
                     id='hdr')
    # Two columns
    intercol_spc = 24     # pts
    col_width = (doc.width - intercol_spc) / 2
    col_ht = doc.height - hdr_ht - spc_after_hdr
    frameL = Frame(doc.leftMargin, doc.bottomMargin,
                   col_width, col_ht,
                   id='col1')
    frameR = Frame(doc.leftMargin + col_width + intercol_spc, doc.bottomMargin,
                   col_width, col_ht,
                   id='col2')
    doc.addPageTemplates(
        [PageTemplate(id='twoCol', frames=[frameHdr, frameL, frameR],
                      onPage=myLaterPages)]
    )
    # Pass a list of Flowables to the doc's `build' method:
    doc.build(elements)
    # onFirstPage=myFirstPage, onLaterPages=myLaterPages


title = 'Sample Cutlist'
pageinfo = 'Job Name: Toigo Kitchen'
page_width, page_ht = landscape(letter)


# Main content is contained in `elements', which is a list of Flowables.
elements = []    # [Spacer(1, 1.5 * inch)]

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading3']
styleFxd = ParagraphStyle(name='FixedWidth', fontName='Courier')

cab_run = cab.Run(247.0, 28.0, 24.0, num_fillers=0)
j = job.Job('Toigo Kitchen', cab_run, 'Kiosk with built-in espresso bar.')

elements += [Paragraph(line, styleN) for line in j.header]
elements.append(FrameBreak())

# elements.append(Spacer(0.1 * inch, 0.25 * inch))
elements.append(Paragraph('Overview:', styleH))
elements += [Paragraph(line, styleN) for line in j.overview]
# TODO: Append isoview drawing to elements, here.
elements.append(FrameBreak())

# TODO: Append panel drawings to elements, here.
elements.append(Paragraph('Parts List:', styleH))
elements += [Paragraph(line, styleFxd) for line in j.partslist]

go()


#------------------------------------------------------------------------------

# Interface

# Global variables

lWidth, lHeight = letter
scale = 1 / 16


def to_scale(x):
    """Scale the argument by the global scale value."""
    return (x * scale)


def save_cutlist(fname, job):
    """Generate a cutlist for the job and save in fname."""
    c = canv.Canvas(fname + ".pdf", pagesize=letter)
    # TODO: Set landscape mode...is now set in "Global variables" above
    draw_isoview(c, job.cabs)
    drawtxt_jobheader(c)
    drawtxt_overview(c)
    drawtxt_partslist(c)
    draw_panels(c)
    c.setPageSize((lHeight, lWidth))
    c.showPage()
    c.save()


# Implementation


def inches_to_pts(line):
    """Convert a 4-tuple representing a line from inches to points.

    The line is a 4-tuple (x1, y1, x2, y2) with coordinates in inches, and the
    return value is the same line with inches converted to DTP points (1/72").
    """
    return tuple(coord * inch for coord in line)


def draw_isoview(canvas, cabs):
    iso45 = (math.sin(45)*cabs.cabinet_depth/2)    #*scale
    isoNlr45 = (math.sin(45)*2)    #*scale
    nlr = 2    #*scale

    isoLines = [
          # list of line coordinates in (x1,y1,x2,y2) format
        # horizontal lines--------------------------------------------
          # horizontal bottom inner line
          (cabs.matl_thickness, cabs.matl_thickness,
           (cabs.cabinet_width - cabs.matl_thickness),
           cabs.matl_thickness),

          # horizontal top inner line - front nailer bottom front edge
          (cabs.matl_thickness, cabs.cabinet_height - cabs.matl_thickness,
           cabs.cabinet_width - cabs.matl_thickness,
           cabs.cabinet_height - cabs.matl_thickness),

          # horizontal top back
          (iso45, iso45 + cabs.cabinet_height,
          iso45 + cabs.cabinet_width, iso45 + cabs.cabinet_height),

          # horizontal back bottom inner
          (iso45 - cabs.matl_thickness,
          cabs.cabinet_height + iso45 - cabs.matl_thickness,
          cabs.cabinet_width + iso45 - cabs.matl_thickness,
          cabs.cabinet_height + iso45 - cabs.matl_thickness),

          # horizontal inside at bottom back
          (iso45, iso45,
          cabs.cabinet_width - cabs.matl_thickness, iso45),

          # horizontal front nailer - rear edge
          (isoNlr45 + cabs.matl_thickness, cabs.cabinet_height + nlr,
          cabs.cabinet_width - cabs.matl_thickness + isoNlr45,
          cabs.cabinet_height + nlr),

          # horizontal back nailer
          (iso45 - isoNlr45,
          cabs.cabinet_height + iso45 - isoNlr45 - cabs.matl_thickness,
          cabs.cabinet_width + iso45 - isoNlr45 - cabs.matl_thickness*2,
          cabs.cabinet_height + iso45 - isoNlr45 - cabs.matl_thickness),

          # horizontal back nailer bottom
          (iso45 - isoNlr45,
          cabs.cabinet_height + iso45 - isoNlr45 - cabs.matl_thickness*2,
          cabs.cabinet_width + iso45 - isoNlr45 - cabs.matl_thickness*3,
          cabs.cabinet_height + iso45 - isoNlr45 - cabs.matl_thickness*2),

        # vertical lines--------------------------------------------------
          # vertical left inner line
          (cabs.matl_thickness, 0,
           cabs.matl_thickness, cabs.cabinet_height),

          # vertical right inner line
          (cabs.cabinet_width - cabs.matl_thickness, 0,
          cabs.cabinet_width - cabs.matl_thickness, cabs.cabinet_height),

          # vertical right back
          (iso45 + cabs.cabinet_width, iso45,
          iso45 + cabs.cabinet_width, cabs.cabinet_height + iso45),

          # vertical right back inner
          (cabs.cabinet_width + iso45 - cabs.matl_thickness,
          iso45 - cabs.matl_thickness,
          cabs.cabinet_width + iso45 - cabs.matl_thickness,
          cabs.cabinet_height + iso45 - cabs.matl_thickness),

          # vertical back nailer small inner line
          (iso45 - isoNlr45,
          cabs.cabinet_height + iso45 - isoNlr45 - cabs.matl_thickness*2,
          iso45 - isoNlr45,
          cabs.cabinet_height + iso45 - isoNlr45 - cabs.matl_thickness),

          # vertical inside line between nailers
          (iso45, cabs.cabinet_height + nlr,
          iso45, cabs.cabinet_height + iso45 - isoNlr45 - cabs.matl_thickness*2),

          # vertical inside line at back of left side
          (iso45, iso45,
          iso45, cabs.cabinet_height - cabs.matl_thickness),

        # angled lines------------------------------------------------------------
          # iso bottom left inner angle
          (cabs.matl_thickness, cabs.matl_thickness,
          iso45, iso45),

          # iso upper left angle
          (0, cabs.cabinet_height,
          iso45, cabs.cabinet_height + iso45),

          # iso upper left angle inner
          (cabs.matl_thickness, cabs.cabinet_height,
          iso45,iso45 + cabs.cabinet_height - cabs.matl_thickness),          

          # iso upper right angle
          (cabs.cabinet_width, cabs.cabinet_height,
          iso45 + cabs.cabinet_width, iso45 + cabs.cabinet_height),

          # iso upper right angle inner
          (cabs.cabinet_width - cabs.matl_thickness, cabs.cabinet_height,
          cabs.cabinet_width + iso45 - cabs.matl_thickness*2,
          cabs.cabinet_height + iso45 - cabs.matl_thickness),          

          # iso lower right angle
          (cabs.cabinet_width, 0,
          iso45 + cabs.cabinet_width, iso45),
          ]
    
    isoLines_pts = [inches_to_pts(line) for line in isoLines]
    
    canvas.translate(1*inch,1*inch)#lHeight - cabs.cabinet_height*scale*3 + iso45/2)
    canvas.setLineWidth(1)
    canvas.setStrokeColor(colors.black)
    canvas.setFillColor(colors.black)
    canvas.drawString(-0.5 * inch, (cabs.cabinet_height / 2 * scale * inch),
                       str(cabs.cabinet_height) + '"')
    
    canvas.scale(scale, scale)
    canvas.rect(0, 0, cabs.cabinet_width * inch, cabs.cabinet_height * inch)
    canvas.lines(isoLines_pts)


def drawtxt_jobheader(canvas):
    pass


def drawtxt_overview(canvas):
    pass


def drawtxt_partslist(canvas):
    pass


def draw_panels(canvas):
    pass

# cutlist-platy.py ends here
