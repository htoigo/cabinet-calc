# cutlist.py    -*- coding: utf-8 -*-

import math
from functools import reduce
import re

from reportlab.pdfgen import canvas as canv
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, \
                               PageTemplate, Frame, Paragraph, Spacer, \
                               FrameBreak, Table, TableStyle, XPreformatted
from reportlab.rl_config import defaultPageSize, \
                                canvas_basefontname as _baseFontName
from reportlab.lib.fonts import tt2ps
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
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

# Fonts

_baseFontNameB = tt2ps(_baseFontName, 1, 0)
_baseFontNameI = tt2ps(_baseFontName, 0, 1)
_baseFontNameBI = tt2ps(_baseFontName, 1, 1)

# Paragraph styles for text

# Normal text style
normal_style = ParagraphStyle(
    name='Normal',
    fontName=_baseFontName,
    fontSize=10,
    leading=12)

# Right-justified normaltext
rt_style = ParagraphStyle(
    name='RightText',
    parent=normal_style,
    alignment=TA_RIGHT)

# Fixed-width style for parts list so number columns line up
fixed_style = ParagraphStyle(
    name='FixedWidth',
    parent=normal_style,
    fontName='Courier',
    fontSize=10,
    leading=12)

# Title style (the Job Name used this style, as it is the title of the cutlist)
title_style = ParagraphStyle(
    name='Title',
    parent=normal_style,
    fontName = _baseFontNameB,
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=6)

# Total wall width style
wallwidth_style = ParagraphStyle(
    name='WallWidth',
    parent=normal_style,
    fontName=_baseFontNameB,
    fontSize=12,
    leading=14,
    spaceBefore=10,
    spaceAfter=5)

# Heading style for overview & parts list headings
heading_style = ParagraphStyle(
    name='Heading',
    parent=normal_style,
    fontName=_baseFontNameB,
    fontSize=12,
    leading=14,
    spaceBefore=12,
    spaceAfter=6)


def landscape(pagesize):
    """Return pagesize in landscape mode (with width and height reversed)."""
    w, h = pagesize
    return (h, w)


page_width, page_ht = landscape(letter)


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


def pdf_ify(fname):
    """Append `.pdf' to the given filename, only if needed."""
    pdfre = re.compile(r'.+\.[Pp][Dd][Ff]$')
    if re.match(pdfre, fname):
        result = fname
    else:
        result = fname + '.pdf'
    return result


def makeframes(doc):
    """Return (frameHdr, frameL, frameR), given the document template."""
    hdr_ht = 60           # pts
    hdr_spc_after = 12    # pts
    frameHdr = Frame(doc.leftMargin, page_ht - doc.topMargin - hdr_ht,
                     doc.width, hdr_ht,
                     id='hdr')
    # The two columns
    intercol_spc = 24     # pts
    ltcol_width = (doc.width - intercol_spc) * 0.4
    rtcol_width = (doc.width - intercol_spc) * 0.6
    col_ht = doc.height - hdr_ht - hdr_spc_after
    frameL = Frame(doc.leftMargin, doc.bottomMargin,
                   ltcol_width, col_ht,
                   id='col1')
    frameR = Frame(doc.leftMargin + ltcol_width + intercol_spc, doc.bottomMargin,
                   rtcol_width, col_ht,
                   id='col2')
    return (frameHdr, frameL, frameR)


def save_cutlist(fname, job):
    """Generate a cutlist for the job and save in fname.pdf."""
    doc = BaseDocTemplate(pdf_ify(fname), showBoundary=0,
                          pagesize=landscape(letter))
    frameHdr, frameL, frameR = makeframes(doc)
    doc.addPageTemplates(
        [PageTemplate(id='twoCol', frames=[frameHdr, frameL, frameR],
                      onPage=myLaterPages)]
    )
    # Construct the cutlist content--i.e., the `elements' list of Flowables
    elements = content(job)
    # Fill out and layout the document. This saves the pdf file as well.
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
    # linen =     HexColor(0xFAF0E6)
    result.add(Rect(rx, ry, hdim_scaled, vdim_scaled,
                    fillColor=colors.HexColor(0xf8f0e6)))
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
        matl_thick_str = String(rx + hdim_scaled - 6, ry + vdim_scaled - 7 - 8,
                                dimstr(thickness) + '"  ' + material[:3],
                                textAnchor='end',
                                fontSize=7)
        result.add(matl_thick_str)
    return result


def isometric_view(job):
    """Return a Drawing of the isometric view of a single cabinet."""
    iso45 = math.sin(45) * job.cabs.cabinet_depth / 2
    isoNlr45 = math.sin(45) * 2
    nlr = 2

    isoLines = [
        # list of line coordinates in (x1,y1,x2,y2) format
        # horizontal lines--------------------------------------------
        # horizontal bottom inner line
        (job.cabs.matl_thickness, job.cabs.matl_thickness,
         (job.cabs.cabinet_width - job.cabs.matl_thickness),
         job.cabs.matl_thickness),

        # horizontal top inner line - front nailer bottom front edge
        (job.cabs.matl_thickness, job.cabs.cabinet_height - job.cabs.matl_thickness,
         job.cabs.cabinet_width - job.cabs.matl_thickness,
         job.cabs.cabinet_height - job.cabs.matl_thickness),

        # horizontal top back
        (iso45, iso45 + job.cabs.cabinet_height,
         iso45 + job.cabs.cabinet_width, iso45 + job.cabs.cabinet_height),

        # horizontal back bottom inner
        (iso45 - job.cabs.matl_thickness,
         job.cabs.cabinet_height + iso45 - job.cabs.matl_thickness,
         job.cabs.cabinet_width + iso45 - job.cabs.matl_thickness,
         job.cabs.cabinet_height + iso45 - job.cabs.matl_thickness),

        # horizontal inside at bottom back
        (iso45, iso45,
         job.cabs.cabinet_width - job.cabs.matl_thickness, iso45),

        # horizontal front nailer - rear edge
        (isoNlr45 + job.cabs.matl_thickness, job.cabs.cabinet_height + nlr,
         job.cabs.cabinet_width - job.cabs.matl_thickness + isoNlr45,
         job.cabs.cabinet_height + nlr),

        # horizontal back nailer
        (iso45 - isoNlr45,
         job.cabs.cabinet_height + iso45 - isoNlr45 - job.cabs.matl_thickness,
         job.cabs.cabinet_width + iso45 - isoNlr45 - job.cabs.matl_thickness*2,
         job.cabs.cabinet_height + iso45 - isoNlr45 - job.cabs.matl_thickness),

        # horizontal back nailer bottom
        (iso45 - isoNlr45,
         job.cabs.cabinet_height + iso45 - isoNlr45 - job.cabs.matl_thickness*2,
         job.cabs.cabinet_width + iso45 - isoNlr45 - job.cabs.matl_thickness*3,
         job.cabs.cabinet_height + iso45 - isoNlr45 - job.cabs.matl_thickness*2),

        # vertical lines--------------------------------------------------
        # vertical left inner line
        (job.cabs.matl_thickness, 0,
         job.cabs.matl_thickness, job.cabs.cabinet_height),

        # vertical right inner line
        (job.cabs.cabinet_width - job.cabs.matl_thickness, 0,
         job.cabs.cabinet_width - job.cabs.matl_thickness, job.cabs.cabinet_height),

        # vertical right back
        (iso45 + job.cabs.cabinet_width, iso45,
         iso45 + job.cabs.cabinet_width, job.cabs.cabinet_height + iso45),

        # vertical right back inner
        (job.cabs.cabinet_width + iso45 - job.cabs.matl_thickness,
         iso45 - job.cabs.matl_thickness,
         job.cabs.cabinet_width + iso45 - job.cabs.matl_thickness,
         job.cabs.cabinet_height + iso45 - job.cabs.matl_thickness),

        # vertical back nailer small inner line
        (iso45 - isoNlr45,
         job.cabs.cabinet_height + iso45 - isoNlr45 - job.cabs.matl_thickness*2,
         iso45 - isoNlr45,
         job.cabs.cabinet_height + iso45 - isoNlr45 - job.cabs.matl_thickness),

        # vertical inside line between nailers
        (iso45, job.cabs.cabinet_height + nlr,
         iso45, job.cabs.cabinet_height + iso45 - isoNlr45 - job.cabs.matl_thickness*2),

        # vertical inside line at back of left side
        (iso45, iso45,
         iso45, job.cabs.cabinet_height - job.cabs.matl_thickness),

        # angled lines------------------------------------------------------------
        # iso bottom left inner angle
        (job.cabs.matl_thickness, job.cabs.matl_thickness,
         iso45, iso45),

        # iso upper left angle
        (0, job.cabs.cabinet_height,
         iso45, job.cabs.cabinet_height + iso45),

        # iso upper left angle inner
        (job.cabs.matl_thickness, job.cabs.cabinet_height,
         iso45,iso45 + job.cabs.cabinet_height - job.cabs.matl_thickness),          

        # iso upper right angle
        (job.cabs.cabinet_width, job.cabs.cabinet_height,
         iso45 + job.cabs.cabinet_width, iso45 + job.cabs.cabinet_height),

        # iso upper right angle inner
        (job.cabs.cabinet_width - job.cabs.matl_thickness, job.cabs.cabinet_height,
         job.cabs.cabinet_width + iso45 - job.cabs.matl_thickness*2,
         job.cabs.cabinet_height + iso45 - job.cabs.matl_thickness),          

        # iso lower right angle
        (job.cabs.cabinet_width, 0,
         iso45 + job.cabs.cabinet_width, iso45),

        # Front cabinet rectangle lines

        # Horizontal bottom line
        (0, 0, job.cabs.cabinet_width, 0),

        # Horizontal top line
        (0, job.cabs.cabinet_height, job.cabs.cabinet_width, job.cabs.cabinet_height),

        # Vertical left line
        (0, 0, 0, job.cabs.cabinet_height),

        # Vertical right line
        (job.cabs.cabinet_width, 0, job.cabs.cabinet_width, job.cabs.cabinet_height)
    ]
    isoLines_pts = [inches_to_pts(line) for line in isoLines]
    isoLines_scaled = [(coord * default_iso_scale for coord in line)
                       for line in isoLines_pts]

    result = Drawing(260, 210)
    for line in isoLines_scaled:
        result.add(Line(*line, strokeWidth=0.25))

    vdim = job.cabs.cabinet_height
    vdim_scaled = vdim * inch * default_iso_scale
    # (x,y) of back right bottom, scaled
    brb_x_scaled = (job.cabs.cabinet_width + iso45) * inch * default_iso_scale
    brb_y_scaled = iso45 * inch * default_iso_scale
    result.add(String(brb_x_scaled + 4, brb_y_scaled + vdim_scaled / 2,
                      dimstr(vdim) + '"',
                      textAnchor='start',
                      fontSize=9))
    hdim = job.cabs.cabinet_width
    hdim_scaled = hdim * inch * default_iso_scale
    # (x,y) of back left top, scaled
    blt_x_scaled = iso45 * inch * default_iso_scale
    blt_y_scaled = (job.cabs.cabinet_height + iso45) * inch * default_iso_scale
    result.add(String(blt_x_scaled + hdim_scaled / 2, blt_y_scaled + 4,
                      dimstr(hdim) + '"',
                      textAnchor='middle',
                      fontSize=9))
    ddim = job.cabs.cabinet_depth
    ddim_scaled = ddim * inch * default_iso_scale
    # (x,y) of middle right bottom, scaled
    mrb_x_scaled = (job.cabs.cabinet_width + iso45 / 2) * inch * default_iso_scale
    mrb_y_scaled = iso45 / 2 * inch * default_iso_scale
    result.add(String(mrb_x_scaled + 10, mrb_y_scaled,
                      dimstr(ddim) + '"',
                      textAnchor='start',
                      fontSize=9))
    # result.translate(10, 0)
    return result


def panels_table(job):
    """Return a table filled with drawings of the individual panels."""
    backpanel_dr = panel_drawing(
        'Back', job.cabs.back_width, job.cabs.back_height,
        material=job.cabs.material, thickness=job.cabs.matl_thickness)
    bottompanel_dr = panel_drawing(
        'Bottom', job.cabs.bottom_width, job.cabs.bottom_depth,
        material=job.cabs.material, thickness=job.cabs.matl_thickness)
    sidepanel_dr = panel_drawing(
        'Side', job.cabs.side_depth, job.cabs.side_height,
        material=job.cabs.material, thickness=job.cabs.matl_thickness)
    # Nailer scale may need to be 1/16 for hdim to fit
    topnailer_dr = panel_drawing(
        'Nailer', job.cabs.topnailer_depth, job.cabs.topnailer_width)
    # Door scale may need to be 1/20 for hdim to fit
    door_dr = panel_drawing(
        'Door', job.cabs.door_width, job.cabs.door_height,
        material=job.cabs.material, thickness=job.cabs.matl_thickness)
    # Add a filler only if needed:
    filler_dr = panel_drawing(
        'Filler', job.cabs.filler_width, job.cabs.filler_height)

    # Create table for layout of the panel drawings
    colWidths = ('35%', '35%', '30%')
    rowHeights = (130, 130)       # assumes col_ht of 411 pts
                                  # 6.5 * 72 - 45 - 12
    if job.cabs.num_fillers == 0:
        data = ( (backpanel_dr, sidepanel_dr, topnailer_dr),
                 (bottompanel_dr, door_dr) )
    else:
        data = ( (backpanel_dr, sidepanel_dr, topnailer_dr),
                 (bottompanel_dr, door_dr, filler_dr) )
    top_center_style = [ ('VALIGN', (0,0), (-1,-1), 'TOP'),
                         ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]
    return Table(data, colWidths, rowHeights, style=top_center_style)


def hdr_table(job):
    """Return a table layout of the job header."""
    if job.description != '':
        desc = 'Description: ' + job.description
    else:
        desc = ''
    # Endedness indicates whether the cabinet run is open-ended or closed-ended
    # on each side. It can be: 'Both ends open.', 'Both ends closed.',
    # 'Left end closed,  right end open.', etc.
    endedness = 'Both ends open.'
    data = ( ( Paragraph('Job Name: ' + job.name, title_style),
               Paragraph(str(job.cabs.fullwidth) + '" wide', wallwidth_style),
               Paragraph(endedness, rt_style)),
             (Paragraph(desc, normal_style), '', '') )
    styleHdr = [ ('VALIGN', (0,0), (0,0), 'MIDDLE'),
                 ('VALIGN', (1,0), (2,0), 'BOTTOM'),
                 ('ALIGN', (1,0), (1,0), 'CENTER'),
                 ('ALIGN', (2,0), (2,0), 'RIGHT'),
                 # Job description spans across entire 2nd row.
                 ('SPAN', (0,1), (2,1)),
                 # Nice colors:  cornsilk, linen
                 # lightslategrey = HexColor(0x778899) , 0xc8d8e6
                 ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(0xe0e4e2))
                 # ('LINEBELOW', (0,'splitlast'), (-1,'splitlast'), 1, colors.grey,'butt')
    ]
    return Table(data, style=styleHdr, colWidths = ['50%','25%','25%'])


def content(job):
    """Create a list of flowables with all the content for the given job."""
    result = []
    result.append(hdr_table(job))
    result.append(FrameBreak())

    result.append(Paragraph('Overview:', heading_style))
    result.append(Paragraph(job.summaryln, normal_style))
    result.append(Spacer(1, 10))
    for line in job.cabinfo:
        result.append(Paragraph(line, normal_style))
    result.append(Spacer(1, 10))
    for line in job.materialinfo:
        result.append(Paragraph(line, normal_style))
    result.append(isometric_view(job))
    result.append(FrameBreak())

    result.append(panels_table(job))
    result.append(Paragraph('Parts List:', heading_style))
    for line in job.partslist:
        result.append(XPreformatted(line, fixed_style))
    return result


# cutlist.py ends here
