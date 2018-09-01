# cutlist-platy.py    -*- coding: utf-8 -*-

import math
from functools import reduce

from reportlab.pdfgen import canvas as canv
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, \
                               PageTemplate, Frame, Paragraph, Spacer, \
                               FrameBreak, Table, TableStyle, XPreformatted
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.graphics.shapes import Drawing, Line, Rect, String, Group, \
    PolyLine

import cabinet as cab
import job
from dimension_strs import dimstr, dimstr_col


# Global Variables

debug = False

default_iso_scale = 1 / 16
default_panel_scale = 1 / 32

title = 'Sample Cutlist'
pageinfo = 'Job Name: Toigo Kitchen'

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading3']
styleFxd = ParagraphStyle(name='FixedWidth', fontName='Courier',
                          fontSize=8)


def landscape(pagesize):
    """Return pagesize in landscape mode (with width and height reversed)."""
    w, h = pagesize
    return (h, w)


page_width, page_ht = landscape(letter)


def unlines(lines):
    """Join a list of lines, after appending a newline to each."""
    nlines = map(lambda s: s + '\n', lines)
    str = reduce(lambda s, t: s+t, nlines, '')
    return str


def inches_to_pts(line):
    """Convert a 4-tuple representing a line from inches to points.

    The line is a 4-tuple (x1, y1, x2, y2) with coordinates in inches, and the
    return value is the same line with inches converted to DTP points (1/72").
    """
    return tuple(coord * inch for coord in line)


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
    canvas.drawString(inch, 0.75 * inch, '{}'.format(pageinfo))
    canvas.drawRightString(page_width - inch, 0.75 * inch,
                           'Page {}'.format(doc.page))
    canvas.restoreState()


def build_doc():
    doc = BaseDocTemplate('platy-doc.pdf', showBoundary=0,
                          pagesize=landscape(letter))

    hdr_ht = 60           # pts   6 + 12 + 3 + 12 + 3 + 6
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


def panel_drawing(name, hdim, vdim, scale=default_panel_scale, padding=6,
                  material=None, thickness=None):
    """Create an individual panel Drawing of the named panel."""
    hdim_scaled = hdim * inch * scale
    vdim_scaled = vdim * inch * scale
    # We might need 36 pts of space on left of rectangle to be safe,
    # for a long vdim_str, like 23 13/16-".
    result = Drawing(hdim_scaled + 2 * padding + 36,
                     vdim_scaled + 2 * padding + 14 + 4 + 10)
    # Coordinates of the lower left corner of the rectangle
    rx = padding + 36
    ry = padding + 14
    result.add(Rect(rx, ry, hdim_scaled, vdim_scaled,
                    fillColor=colors.cornsilk))
    result.add(String(rx + hdim_scaled / 2,
                      ry + vdim_scaled + 4,
                      name,
                      textAnchor='middle'))
    hdim_arrow = PolyLine([rx + 7, ry - 11,  rx + 1.5, ry - 9,
                           rx + 7, ry - 7,  rx + 1.5, ry - 9,
                           rx + hdim_scaled - 1.5, ry - 9,
                           rx + hdim_scaled - 1.5 - 5.5, ry - 7,
                           rx + hdim_scaled - 1.5, ry - 9,
                           rx + hdim_scaled - 1.5 - 5.5, ry - 11],
                          strokeWidth=0.6)
    result.add(hdim_arrow)
    result.add(Line(rx, ry - 4,  rx, ry - 14))
    result.add(Line(rx + hdim_scaled, ry - 4,  rx + hdim_scaled, ry - 14))
    hdim_str = String(rx + hdim_scaled / 2, ry - 12,
                      dimstr(hdim) + '"',
                      textAnchor='middle',
                      fontSize=9)
    bnds = hdim_str.getBounds()
    whiteout_r = Rect(bnds[0], bnds[1], bnds[2] - bnds[0], hdim_str.fontSize,
                      fillColor=colors.white, strokeColor=colors.white)
    result.add(whiteout_r)
    result.add(hdim_str)
    vdim_arrow = PolyLine([rx - 11, ry + 1.5 + 5.5,  rx - 9, ry + 1.5,
                           rx - 7, ry + 1.5 + 5.5,  rx - 9, ry + 1.5,
                           rx - 9, ry + vdim_scaled - 1.5,
                           rx - 7, ry + vdim_scaled - 1.5 - 5.5,
                           rx - 9, ry + vdim_scaled - 1.5,
                           rx - 11, ry + vdim_scaled - 1.5 - 5.5],
                          strokeWidth=0.6)
    result.add(vdim_arrow)
    result.add(Line(rx - 4, ry,  rx - 14, ry))
    result.add(Line(rx - 4, ry + vdim_scaled,  rx - 14, ry + vdim_scaled))
    vdim_str = String(rx - 2, ry + vdim_scaled / 2 - 4,
                      dimstr(vdim) + '"',
                      textAnchor='end',
                      fontSize=9)
    bnds = vdim_str.getBounds()
    whiteout_r = Rect(bnds[0], bnds[1], bnds[2] - bnds[0], vdim_str.fontSize,
                      fillColor=colors.white, strokeColor=colors.white)
    result.add(whiteout_r)
    result.add(vdim_str)
    if material is not None and thickness is not None:
        matl_thick_str = String(rx + 6, ry + 8,
                                dimstr(thickness) + '"  ' + material[:3],
                                fontSize=7)
        result.add(matl_thick_str)
    return result


cab_run = cab.Run(139.5, 27.0625, 24.125, num_fillers=0)
j = job.Job('Toigo Kitchen', cab_run, 'Kiosk with built-in espresso bar.')



# Construct a Drawing of the isometric view of a single cabinet.

# Lines for Harry's matrix-rotated isometric view
# isometric_lines=[((-21.213203435596427, 14.084566021003273), (4.242640687119287, -0.6123724356957947)), ((-21.213203435596427, 14.084566021003273), (-21.213203435596427, -9.185586535436919)), ((-21.213203435596427, 14.084566021003273), (-4.242640687119287, 23.882524992135984)), ((4.242640687119287, -0.6123724356957947), (-21.213203435596427, 14.084566021003273)), ((4.242640687119287, -0.6123724356957947), (4.242640687119287, -23.882524992135984)), ((4.242640687119287, -0.6123724356957947), (21.213203435596427, 9.185586535436919)), ((-21.213203435596427, -9.185586535436919), (-21.213203435596427, 14.084566021003273)), ((-21.213203435596427, -9.185586535436919), (4.242640687119287, -23.882524992135984)), ((-21.213203435596427, -9.185586535436919), (-4.242640687119287, 0.6123724356957947)), ((4.242640687119287, -23.882524992135984), (4.242640687119287, -0.6123724356957947)), ((4.242640687119287, -23.882524992135984), (-21.213203435596427, -9.185586535436919)), ((4.242640687119287, -23.882524992135984), (21.213203435596427, -14.084566021003273)), ((-4.242640687119287, 23.882524992135984), (-21.213203435596427, 14.084566021003273)), ((-4.242640687119287, 23.882524992135984), (21.213203435596427, 9.185586535436919)), ((-4.242640687119287, 23.882524992135984), (-4.242640687119287, 0.6123724356957947)), ((21.213203435596427, 9.185586535436919), (4.242640687119287, -0.6123724356957947)), ((21.213203435596427, 9.185586535436919), (-4.242640687119287, 23.882524992135984)), ((21.213203435596427, 9.185586535436919), (21.213203435596427, -14.084566021003273)), ((-4.242640687119287, 0.6123724356957947), (-21.213203435596427, -9.185586535436919)), ((-4.242640687119287, 0.6123724356957947), (-4.242640687119287, 23.882524992135984)), ((-4.242640687119287, 0.6123724356957947), (21.213203435596427, -14.084566021003273)), ((21.213203435596427, -14.084566021003273), (4.242640687119287, -23.882524992135984)), ((21.213203435596427, -14.084566021003273), (21.213203435596427, 9.185586535436919)), ((21.213203435596427, -14.084566021003273), (-4.242640687119287, 0.6123724356957947))]
# for p1, p2 in isometric_lines:
#     isometric_view.add(Line(p1[0], p1[1], p2[0], p2[1], strokeWidth=0.25))

iso45 = (math.sin(45)*j.cabs.cabinet_depth/2)
isoNlr45 = (math.sin(45)*2)
nlr = 2

isoLines = [
    # list of line coordinates in (x1,y1,x2,y2) format
    # horizontal lines--------------------------------------------
    # horizontal bottom inner line
    (j.cabs.matl_thickness, j.cabs.matl_thickness,
     (j.cabs.cabinet_width - j.cabs.matl_thickness),
     j.cabs.matl_thickness),

    # horizontal top inner line - front nailer bottom front edge
    (j.cabs.matl_thickness, j.cabs.cabinet_height - j.cabs.matl_thickness,
     j.cabs.cabinet_width - j.cabs.matl_thickness,
     j.cabs.cabinet_height - j.cabs.matl_thickness),

    # horizontal top back
    (iso45, iso45 + j.cabs.cabinet_height,
     iso45 + j.cabs.cabinet_width, iso45 + j.cabs.cabinet_height),

    # horizontal back bottom inner
    (iso45 - j.cabs.matl_thickness,
     j.cabs.cabinet_height + iso45 - j.cabs.matl_thickness,
     j.cabs.cabinet_width + iso45 - j.cabs.matl_thickness,
     j.cabs.cabinet_height + iso45 - j.cabs.matl_thickness),

    # horizontal inside at bottom back
    (iso45, iso45,
     j.cabs.cabinet_width - j.cabs.matl_thickness, iso45),

    # horizontal front nailer - rear edge
    (isoNlr45 + j.cabs.matl_thickness, j.cabs.cabinet_height + nlr,
     j.cabs.cabinet_width - j.cabs.matl_thickness + isoNlr45,
     j.cabs.cabinet_height + nlr),

    # horizontal back nailer
    (iso45 - isoNlr45,
     j.cabs.cabinet_height + iso45 - isoNlr45 - j.cabs.matl_thickness,
     j.cabs.cabinet_width + iso45 - isoNlr45 - j.cabs.matl_thickness*2,
     j.cabs.cabinet_height + iso45 - isoNlr45 - j.cabs.matl_thickness),

    # horizontal back nailer bottom
    (iso45 - isoNlr45,
     j.cabs.cabinet_height + iso45 - isoNlr45 - j.cabs.matl_thickness*2,
     j.cabs.cabinet_width + iso45 - isoNlr45 - j.cabs.matl_thickness*3,
     j.cabs.cabinet_height + iso45 - isoNlr45 - j.cabs.matl_thickness*2),

    # vertical lines--------------------------------------------------
    # vertical left inner line
    (j.cabs.matl_thickness, 0,
     j.cabs.matl_thickness, j.cabs.cabinet_height),

    # vertical right inner line
    (j.cabs.cabinet_width - j.cabs.matl_thickness, 0,
     j.cabs.cabinet_width - j.cabs.matl_thickness, j.cabs.cabinet_height),

    # vertical right back
    (iso45 + j.cabs.cabinet_width, iso45,
     iso45 + j.cabs.cabinet_width, j.cabs.cabinet_height + iso45),

    # vertical right back inner
    (j.cabs.cabinet_width + iso45 - j.cabs.matl_thickness,
     iso45 - j.cabs.matl_thickness,
     j.cabs.cabinet_width + iso45 - j.cabs.matl_thickness,
     j.cabs.cabinet_height + iso45 - j.cabs.matl_thickness),

    # vertical back nailer small inner line
    (iso45 - isoNlr45,
     j.cabs.cabinet_height + iso45 - isoNlr45 - j.cabs.matl_thickness*2,
     iso45 - isoNlr45,
     j.cabs.cabinet_height + iso45 - isoNlr45 - j.cabs.matl_thickness),

    # vertical inside line between nailers
    (iso45, j.cabs.cabinet_height + nlr,
     iso45, j.cabs.cabinet_height + iso45 - isoNlr45 - j.cabs.matl_thickness*2),

    # vertical inside line at back of left side
    (iso45, iso45,
     iso45, j.cabs.cabinet_height - j.cabs.matl_thickness),

    # angled lines------------------------------------------------------------
    # iso bottom left inner angle
    (j.cabs.matl_thickness, j.cabs.matl_thickness,
     iso45, iso45),

    # iso upper left angle
    (0, j.cabs.cabinet_height,
     iso45, j.cabs.cabinet_height + iso45),

    # iso upper left angle inner
    (j.cabs.matl_thickness, j.cabs.cabinet_height,
     iso45,iso45 + j.cabs.cabinet_height - j.cabs.matl_thickness),          

    # iso upper right angle
    (j.cabs.cabinet_width, j.cabs.cabinet_height,
     iso45 + j.cabs.cabinet_width, iso45 + j.cabs.cabinet_height),

    # iso upper right angle inner
    (j.cabs.cabinet_width - j.cabs.matl_thickness, j.cabs.cabinet_height,
     j.cabs.cabinet_width + iso45 - j.cabs.matl_thickness*2,
     j.cabs.cabinet_height + iso45 - j.cabs.matl_thickness),          

    # iso lower right angle
    (j.cabs.cabinet_width, 0,
     iso45 + j.cabs.cabinet_width, iso45),

    # Front cabinet rectangle lines

    # Horizontal bottom line
    (0, 0, j.cabs.cabinet_width, 0),

    # Horizontal top line
    (0, j.cabs.cabinet_height, j.cabs.cabinet_width, j.cabs.cabinet_height),

    # Vertical left line
    (0, 0, 0, j.cabs.cabinet_height),

    # Vertical right line
    (j.cabs.cabinet_width, 0, j.cabs.cabinet_width, j.cabs.cabinet_height)
]
isoLines_pts = [inches_to_pts(line) for line in isoLines]
isoLines_scaled = [(coord * default_iso_scale for coord in line)
                   for line in isoLines_pts]
# isoLines_flat = []
# for tup in isoLines_pts:
#     isoLines_flat.extend(tup)

isometric_view = Drawing(280, 280)
# isometric_view.add(PolyLine(isoLines_flat, strokeWidth=0.25))
for line in isoLines_scaled:
    isometric_view.add(Line(*line, strokeWidth=0.25))

vdim = j.cabs.cabinet_height
vdim_scaled = vdim * inch * default_iso_scale
# (x,y) of back right bottom, scaled
brb_x_scaled = (j.cabs.cabinet_width + iso45) * inch * default_iso_scale
brb_y_scaled = iso45 * inch * default_iso_scale
isometric_view.add(String(brb_x_scaled + 4, brb_y_scaled + vdim_scaled / 2,
                          dimstr(vdim) + '"',
                          textAnchor='start',
                          fontSize=9))
hdim = j.cabs.cabinet_width
hdim_scaled = hdim * inch * default_iso_scale
# (x,y) of back left top, scaled
blt_x_scaled = iso45 * inch * default_iso_scale
blt_y_scaled = (j.cabs.cabinet_height + iso45) * inch * default_iso_scale
isometric_view.add(String(blt_x_scaled + hdim_scaled / 2, blt_y_scaled + 4,
                          dimstr(hdim) + '"',
                          textAnchor='middle',
                          fontSize=9))
ddim = j.cabs.cabinet_depth
ddim_scaled = ddim * inch * default_iso_scale
# (x,y) of middle right bottom, scaled
mrb_x_scaled = (j.cabs.cabinet_width + iso45 / 2) * inch * default_iso_scale
mrb_y_scaled = iso45 / 2 * inch * default_iso_scale
isometric_view.add(String(mrb_x_scaled + 10, mrb_y_scaled,
                          dimstr(ddim) + '"',
                          textAnchor='start',
                          fontSize=9))

isometric_view.translate(40, 40)


# Construct Drawings of the individual panels

backpanel_dr = panel_drawing('Back', cab_run.back_width, cab_run.back_height,
                             material=j.cabs.material,
                             thickness=j.cabs.matl_thickness)
bottompanel_dr = panel_drawing('Bottom', cab_run.bottom_width,
                               cab_run.bottom_depth,
                               material=j.cabs.material,
                               thickness=j.cabs.matl_thickness)
sidepanel_dr = panel_drawing('Side', cab_run.side_depth, cab_run.side_height,
                             material=j.cabs.material,
                             thickness=j.cabs.matl_thickness)
# Nailer scale may need to be 1/16 for hdim to fit
topnailer_dr = panel_drawing('Nailer', cab_run.topnailer_depth,
                             cab_run.topnailer_width)
# Door scale may need to be 1/20 for hdim to fit
door_dr = panel_drawing('Door', cab_run.door_width, cab_run.door_height,
                        material=j.cabs.material,
                        thickness=j.cabs.matl_thickness)
# Add a filler only if needed:
filler_dr = panel_drawing('Filler', cab_run.filler_width, cab_run.filler_height)

# Create table for layout of the panel drawings

colWidths = (110, 110, 92)    # assumes col_width of 312 pts
                              # (9 * 72 - 24) / 2
rowHeights = (130, 130)       # assumes col_ht of 411 pts
                              # 6.5 * 72 - 45 - 12
if j.cabs.num_fillers == 0:
    pnls_data = ( (backpanel_dr, sidepanel_dr, topnailer_dr),
                  (bottompanel_dr, door_dr) )
else:
    pnls_data = ( (backpanel_dr, sidepanel_dr, topnailer_dr),
                  (bottompanel_dr, door_dr, filler_dr) )
panels_tbl = Table(pnls_data, colWidths, rowHeights)
top_center_style = TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
                               ('ALIGN', (0,0), (-1,-1), 'CENTER')])
panels_tbl.setStyle(top_center_style)

# Create table for layout of header

hdr_data = ( (Paragraph(j.header[0], styleH),
              Paragraph(str(j.cabs.fullwidth) + '" Wide', styleH),
              'Both ends open.'),
             (Paragraph(j.header[1], styleN), '', '') )
hdr_sty = [ ('VALIGN', (0,0), (0,0), 'MIDDLE'),
            ('VALIGN', (1,0), (2,0), 'BOTTOM'),
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('ALIGN', (2,0), (2,0), 'RIGHT'),
            # Job description spans across entire 2nd row.
            ('SPAN', (0,1), (2,1)),
            # Nice colors:  cornsilk, linen
            ('BACKGROUND', (0,0), (-1,-1), colors.wheat)
            # ('LINEBELOW', (0,'splitlast'), (-1,'splitlast'), 1, colors.grey,'butt')
]
hdr_tbl = Table(
    hdr_data, style=hdr_sty, colWidths = ['50%','25%','25%'] )


# Main content
# This is contained in `elements', which is a list of Flowables.
elements = []    # [Spacer(1, 1.5 * inch)]

# elements += [Paragraph(line, styleN) for line in j.header]
elements.append(hdr_tbl)
elements.append(FrameBreak())

# elements.append(Spacer(0.1 * inch, 0.25 * inch))
elements.append(Paragraph('Overview:', styleH))
elements += [Paragraph(line, styleN) for line in j.overview]
elements.append(isometric_view)
elements.append(FrameBreak())

# A Table of panels
elements.append(panels_tbl)

elements.append(Paragraph('Parts List:', styleH))
elements += [XPreformatted(line, styleFxd) for line in j.partslist]

build_doc()


#-------------------------------------------------------------------------------

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

# cutlist-platy.py ends here
