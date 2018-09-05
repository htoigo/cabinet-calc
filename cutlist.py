# cutlist.py    -*- coding: utf-8 -*-


import math
import re

from reportlab.pdfgen import canvas as canv
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, FrameBreak,
    Table, TableStyle, XPreformatted
    )
from reportlab.graphics.shapes import (
    Drawing, Line, Rect, String, Group
    )

import cabinet as cab
import job
from dimension_strs import dimstr, dimstr_col
from text import (
    normal_style, rt_style, title_style, wallwidth_style, heading_style,
    fixed_style
    )


# Global Constants

debug = False

default_iso_scale = 1 / 16
default_panel_scale = 1 / 32


def landscape(pagesize):
    """Return pagesize in landscape mode (with width and height reversed)."""
    w, h = pagesize
    return (h, w)


page_width, page_ht = landscape(letter)


def save_cutlist(fname, job):
    """Generate a cutlist for the job and save in fname.pdf."""
    doc = BaseDocTemplate(pdf_ify(fname),
                          pagesize=landscape(letter),
                          title='Cutlist for ' + job.name,
                          #TODO: author='',
                          subject='Cabinet Calc Cutlist Report',
                          #TODO: Get version below from program source
                          creator='Cabinet Calc version 0.1',
                          showBoundary=0
                          )
    frameHdr, frameL, frameR = makeframes(doc)
    doc.addPageTemplates(
        [PageTemplate(id='twoCol', frames=[frameHdr, frameL, frameR],
                      onPage=all_pages
                      )
        ]
    )
    # Construct the cutlist content--i.e., the `elements' list of Flowables
    elements = content(job)
    # Fill out and layout the document. This saves the pdf file as well.
    doc.build(elements)


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
                     doc.width, hdr_ht, id='hdr'
                     )
    # The two side-by-side columns
    intercol_spc = 24     # pts
    ltcol_width = (doc.width - intercol_spc) * 0.4
    rtcol_width = (doc.width - intercol_spc) * 0.6
    col_ht = doc.height - hdr_ht - hdr_spc_after
    frameL = Frame(doc.leftMargin, doc.bottomMargin, ltcol_width, col_ht,
                   id='col1'
                   )
    frameR = Frame(doc.leftMargin + ltcol_width + intercol_spc, doc.bottomMargin,
                   rtcol_width, col_ht, id='col2'
                   )
    return (frameHdr, frameL, frameR)


def all_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    # canvas.drawString(inch, 0.5 * inch, '{}'.format(pageinfo))
    canvas.drawRightString(
        page_width - inch, 0.5 * inch, 'Page {}'.format(doc.page)
        )
    canvas.restoreState()


def content(job):
    """Create a list of flowables with all the content for the cutlist."""
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
    data = (
        ( Paragraph('Job Name: ' + job.name, title_style),
          Paragraph(str(job.cabs.fullwidth) + '" wide', wallwidth_style),
          Paragraph(endedness, rt_style)
          ),
        ( Paragraph(desc, normal_style), '', '')
    )
    styleHdr = [
        ('VALIGN', (0,0), (0,0), 'MIDDLE'),
        ('VALIGN', (1,0), (2,0), 'BOTTOM'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        # Job description spans across entire 2nd row.
        ('SPAN', (0,1), (2,1)),
        # Nice colors:  cornsilk (0xfff8dc), linen (0xfaf0e6),
        #     lightslategrey (0x778899), 0xc8d8e6.
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(0xe0e4e2))
    ]
    return Table(data, style=styleHdr, colWidths = ['50%','25%','25%'])


def inches_to_pts(line):
    """Convert a 4-tuple representing a line from inches to points.

    The line is a 4-tuple (x1, y1, x2, y2) with coordinates in inches, and the
    return value is the same line with inches converted to DTP points (1/72").
    """
    return tuple(coord * inch for coord in line)


def isometric_view(job):
    """Return a Drawing of the isometric view of a single cabinet."""
    iso45 = math.sin(45) * job.cabs.cabinet_depth / 2
    isoNlr45 = math.sin(45) * 2
    nlr = 2

    isoLines = [    # list of line coordinates in (x1,y1,x2,y2) format
        # horizontal lines------------------------------------------------------

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

        # vertical lines--------------------------------------------------------

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

        # angled lines----------------------------------------------------------

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

        # Front cabinet rectangle lines (originally drawn as a Rect)

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
    isoLines_scaled = [
        (coord * default_iso_scale for coord in line) for line in isoLines_pts
        ]

    result = Drawing(260, 210)
    for line in isoLines_scaled:
        result.add(Line(*line, strokeWidth=0.5))

    # Height dimension arrow
    vdim = job.cabs.cabinet_height
    # (x,y) of back right bottom of cabinet, scaled
    brb_x_scaled = (job.cabs.cabinet_width + iso45) * inch * default_iso_scale
    brb_y_scaled = iso45 * inch * default_iso_scale
    arr_off = 12.7    # sqrt(18^2 / 2), an angled distance of 18 pts
    arr = vdimarrow_iso_str(
        vdim, default_iso_scale, brb_x_scaled + arr_off, brb_y_scaled + arr_off,
        0.67, boundsln_len=14
        )
    result.add(arr)

    # Width dimension arrow
    hdim = job.cabs.cabinet_width
    # (x,y) of back left top of cabinet, scaled
    blt_x_scaled = iso45 * inch * default_iso_scale
    blt_y_scaled = (job.cabs.cabinet_height + iso45) * inch * default_iso_scale
    arr = hdimarrow_iso_str(
        hdim, default_iso_scale, blt_x_scaled + arr_off, blt_y_scaled + arr_off,
        0.67, boundsln_len=14
        )
    result.add(arr)

    # Depth dimension arrow
    ddim = job.cabs.cabinet_depth
    cabwidth_scaled = job.cabs.cabinet_width * inch * default_iso_scale
    arr = ddimarrow_iso_str(
        ddim, default_iso_scale, cabwidth_scaled + 5 + 12, 0,
        0.67, boundsln_len=14
        )
    result.add(arr)
    return result


def hdimarrow(dim, scale, x, y, strwid, boundsln_len=10):
    """Return a Group representing a horizontal dimension arrow.

    x and y  are the coordinates of the left end of the arrow.
    dim      is the dimension measurement.
    strwid   is the stroke width of the lines.
    """
    x2, y2 = x + dim * inch * scale, y
    result = Group(
        # Arrow
        Line(x, y, x2, y2, strokeWidth=strwid),
        # Left arrowhead
        Line(x, y, x + 5.5, y + 2, strokeWidth=strwid),
        Line(x, y, x + 5.5, y - 2, strokeWidth=strwid),
        # Right arrowhead
        Line(x2 - 5.5, y2 + 2, x2, y2, strokeWidth=strwid),
        Line(x2 - 5.5, y2 - 2, x2, y2, strokeWidth=strwid),
        # Boundary lines
        Line(x, y - boundsln_len/2, x, y + boundsln_len/2, strokeWidth=strwid),
        Line(x2, y2 - boundsln_len/2, x2, y2 + boundsln_len/2, strokeWidth=strwid)
        )
    return result


def hdimarrow_iso(dim, scale, x, y, strwid, boundsln_len=10):
    """Return a horizontal dimension arrow for the isometric drawing.

    The isometric version of the dimension arrow has angled boundary lines
    and arrowheads.

    x and y  are the coordinates of the left end of the arrow.
    dim      is the dimension measurement.
    strwid   is the stroke width of the lines.
    """
    x2, y2 = x + dim * inch * scale, y
    off = math.sqrt((boundsln_len / 2) ** 2 / 2)
    result = Group(
        # Arrow
        Line(x, y, x2, y2, strokeWidth=strwid),
        # Left arrowhead
        Line(x, y, x + 5.5 + 1.25, y + 1.25, strokeWidth=strwid),
        Line(x, y, x + 5.5 - 1.25, y - 1.25, strokeWidth=strwid),
        # Right arrowhead
        Line(x2 - 5.5 + 1.25, y2 + 1.25, x2, y2, strokeWidth=strwid),
        Line(x2 - 5.5 - 1.25, y2 - 1.25, x2, y2, strokeWidth=strwid),
        # Boundary lines
        Line(x - off, y - off, x + off, y + off, strokeWidth=strwid),
        Line(x2 - off, y2 - off, x2 + off, y2 + off, strokeWidth=strwid)
        )
    return result


def hdimarrow_str(dim, scale, x, y, strwid, boundsln_len=10):
    """Return a horizontal dimension arrow with labeled measurement."""
    result = hdimarrow(dim, scale, x, y, strwid, boundsln_len)
    add_hdimstr(result, dim, scale, x, y)
    return result


def hdimarrow_iso_str(dim, scale, x, y, strwid, boundsln_len=10):
    """Return an isometric horiz dimension arrow with labeled measurement."""
    result = hdimarrow_iso(dim, scale, x, y, strwid, boundsln_len)
    add_hdimstr(result, dim, scale, x, y)
    return result


def add_hdimstr(arrow, dim, scale, x, y):
    """Add a measurement label to the given horizontal dimension arrow."""
    dim_scaled = dim * inch * scale
    dim_str = String(x + dim_scaled / 2, y - 3,
                     dimstr(dim) + '"',
                     textAnchor='middle',
                     fontSize=9
                     )
    bnds = dim_str.getBounds()
    whiteout_r = Rect(
        bnds[0], bnds[1], bnds[2] - bnds[0], dim_str.fontSize,
        fillColor=colors.white, strokeColor=colors.white
        )
    arrow.add(whiteout_r)
    arrow.add(dim_str)
    return arrow


def vdimarrow(dim, scale, x, y, strwid, boundsln_len=10):
    """Return a Group representing a vertical dimension arrow.

    x and y  are the coordinates of the bottom end of the arrow.
    dim      is the dimension measurement.
    strwid   is the stroke width of the lines.
    """
    x2, y2 = x, y + dim * inch * scale
    result = Group(
        # Arrow
        Line(x, y, x2, y2, strokeWidth=strwid),
        # Bottom arrowhead
        Line(x, y, x - 2, y + 5.5, strokeWidth=strwid),
        Line(x, y, x + 2, y + 5.5, strokeWidth=strwid),
        # Top arrowhead
        Line(x2, y2, x2 - 2, y2 - 5.5, strokeWidth=strwid),
        Line(x2, y2, x2 + 2, y2 - 5.5, strokeWidth=strwid),
        # Boundary lines
        Line(x - boundsln_len/2, y, x + boundsln_len/2, y, strokeWidth=strwid),
        Line(x2 - boundsln_len/2, y2, x2 + boundsln_len/2, y2, strokeWidth=strwid)
        )
    return result


def vdimarrow_iso(dim, scale, x, y, strwid, boundsln_len=10):
    """Return a vertical dimension arrow for the isometric drawing.

    The isometric version of the dimension arrow has angled boundary lines
    and arrowheads.

    x and y  are the coordinates of the bottom end of the arrow.
    dim      is the dimension measurement.
    strwid   is the stroke width of the lines.
    """
    x2, y2 = x, y + dim * inch * scale
    off = math.sqrt((boundsln_len / 2) ** 2 / 2)
    result = Group(
        # Arrow
        Line(x, y, x2, y2, strokeWidth=strwid),
        # Bottom arrowhead
        Line(x, y, x - 1.25, y + 5.5 - 1.25, strokeWidth=strwid),
        Line(x, y, x + 1.25, y + 5.5 + 1.25, strokeWidth=strwid),
        # Top arrowhead
        Line(x2 - 1.25, y2 - 5.5 - 1.25, x2, y2, strokeWidth=strwid),
        Line(x2 + 1.25, y2 - 5.5 + 1.25, x2, y2, strokeWidth=strwid),
        # Boundary lines
        Line(x - off, y - off, x + off, y + off, strokeWidth=strwid),
        Line(x2 - off, y2 - off, x2 + off, y2 + off, strokeWidth=strwid)
        )
    return result


def vdimarrow_str(dim, scale, x, y, strwid, boundsln_len=10):
    """Return a vertical dimension arrow with labeled measurement."""
    result = vdimarrow(dim, scale, x, y, strwid, boundsln_len)
    add_vdimstr(result, dim, scale, x, y, boundsln_len)
    return result


def vdimarrow_iso_str(dim, scale, x, y, strwid, boundsln_len=10):
    """Return an isometric vert dimension arrow with labeled measurement."""
    result = vdimarrow_iso(dim, scale, x, y, strwid, boundsln_len)
    add_vdimstr_iso(result, dim, scale, x, y, boundsln_len)
    return result


def add_vdimstr(arrow, dim, scale, x, y, boundsln_len):
    """Add a measurement label to the given vertical dimension arrow."""
    dim_scaled = dim * inch * scale
    dim_str = String(x + boundsln_len / 2 + 2, y + dim_scaled / 2 - 4,
                     dimstr(dim) + '"',
                     textAnchor='end',
                     fontSize=9
                     )
    bnds = dim_str.getBounds()
    whiteout_r = Rect(
        bnds[0], bnds[1], bnds[2] - bnds[0], dim_str.fontSize,
        fillColor=colors.white, strokeColor=colors.white
        )
    arrow.add(whiteout_r)
    arrow.add(dim_str)
    return arrow


def add_vdimstr_iso(arrow, dim, scale, x, y, boundsln_len):
    """Add a measurement label to the given isometric vert dimension arrow."""
    dim_scaled = dim * inch * scale
    off = math.sqrt((boundsln_len / 2) ** 2 / 2)
    dim_str = String(x - off - 2, y + dim_scaled / 2 - 4,
                     dimstr(dim) + '"',
                     textAnchor='start',
                     fontSize=9
                     )
    bnds = dim_str.getBounds()
    whiteout_r = Rect(
        bnds[0], bnds[1], bnds[2] - bnds[0], dim_str.fontSize,
        fillColor=colors.white, strokeColor=colors.white
        )
    arrow.add(whiteout_r)
    arrow.add(dim_str)
    return arrow


def ddimarrow_iso(dim, scale, x, y, strwid, boundsln_len=10):
    """Return a depth dimension arrow for the isometric drawing.

    The isometric version of the dimension arrow has angled boundary lines
    and arrowheads.

    x and y  are the coordinates of the lower left end of the arrow.
    dim      is the dimension measurement.
    strwid   is the stroke width of the lines.
    """
    dim_scaled = dim * inch * scale
    # `iso45' is divided by 2 below because that is how it's calculated
    # in the isometric_view, above.
    iso45 = math.sin(45) * dim_scaled / 2
    x2, y2 = x + iso45, y + iso45
    result = Group(
        # Arrow
        Line(x, y, x2, y2, strokeWidth=strwid),
        # Lower left arrowhead
        Line(x, y, x + (5.5 - 1.25) - 2.5, y + 5.5 - 1.25, strokeWidth=strwid),
        Line(x, y, x + (5.5 - 1.25) + 3, y + 5.5 - 1.25, strokeWidth=strwid),
        # Upper right arrowhead
        Line(x2 - (5.5 - 1.25) - 2.5, y2 - 5.5 + 1.25, x2, y2, strokeWidth=strwid),
        Line(x2 - (5.5 - 1.25) + 2.75, y2 - 5.5 + 1.25, x2, y2, strokeWidth=strwid),
        # Boundary lines
        Line(x - boundsln_len/2, y, x + boundsln_len/2, y, strokeWidth=strwid),
        Line(x2 - boundsln_len/2, y2, x2 + boundsln_len/2, y2, strokeWidth=strwid)
        )
    return result


def ddimarrow_iso_str(dim, scale, x, y, strwid, boundsln_len=10):
    """Return an isometric depth dimension arrow with labeled measurement."""
    result = ddimarrow_iso(dim, scale, x, y, strwid, boundsln_len)
    add_ddimstr_iso(result, dim, scale, x, y, boundsln_len)
    return result


def add_ddimstr_iso(arrow, dim, scale, x, y, boundsln_len):
    """Add a measurement label to the given isometric depth dimension arrow."""
    dim_scaled = dim * inch * scale
    # `iso45' is divided by 2 below because that is how it's calculated
    # in the isometric_view, above.
    iso45 = math.sin(45) * dim_scaled / 2
    xmid, ymid = x + iso45 / 2, y + iso45 / 2
    dim_str = String(xmid - boundsln_len/2 - 4, ymid - 4,
                     dimstr(dim) + '"',
                     textAnchor='start',
                     fontSize=9
                     )
    bnds = dim_str.getBounds()
    whiteout_r = Rect(
        bnds[0], bnds[1], bnds[2] - bnds[0], dim_str.fontSize,
        fillColor=colors.white, strokeColor=colors.white
        )
    arrow.add(whiteout_r)
    arrow.add(dim_str)
    return arrow


def panels_table(job):
    """Return a table filled with drawings of the individual panels."""
    backpanel_dr = panel_drawing(
        'Back', job.cabs.back_width, job.cabs.back_height,
        material=job.cabs.material, thickness=job.cabs.matl_thickness
        )
    bottompanel_dr = panel_drawing(
        'Bottom', job.cabs.bottom_width, job.cabs.bottom_depth,
        material=job.cabs.material, thickness=job.cabs.matl_thickness
        )
    sidepanel_dr = panel_drawing(
        'Side', job.cabs.side_depth, job.cabs.side_height,
        material=job.cabs.material, thickness=job.cabs.matl_thickness
        )
    # Nailer scale may need to be 1/16 for hdim to fit
    topnailer_dr = panel_drawing(
        'Nailer', job.cabs.topnailer_depth, job.cabs.topnailer_width
        )
    # Door scale may need to be 1/20 for hdim to fit
    door_dr = panel_drawing(
        'Door', job.cabs.door_width, job.cabs.door_height,
        material=job.cabs.material, thickness=job.cabs.matl_thickness
        )
    # The filler will be used only if needed (see below):
    filler_dr = panel_drawing(
        'Filler', job.cabs.filler_width, job.cabs.filler_height
        )

    # Create table for layout of the panel drawings
    colWidths = ('35%', '35%', '30%')
    rowHeights = (130, 130)       # assumes col_ht of 411 pts
                                  # 6.5 * 72 - 45 - 12
    if job.cabs.num_fillers == 0:
        data = ( (backpanel_dr, sidepanel_dr, topnailer_dr),
                 (bottompanel_dr, door_dr)
                 )
    else:
        data = ( (backpanel_dr, sidepanel_dr, topnailer_dr),
                 (bottompanel_dr, door_dr, filler_dr)
                 )
    top_center_style = [
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
        ]
    return Table(data, colWidths, rowHeights, style=top_center_style)


def panel_drawing(name, hdim, vdim, scale=default_panel_scale, padding=6,
                  material=None, thickness=None):
    """Create an individual panel Drawing of the named panel."""
    hdim_scaled = hdim * inch * scale
    vdim_scaled = vdim * inch * scale
    # We might need 36 pts of space on left of rectangle to be safe,
    # for a long vdim_str, like 23 13/16-".
    result = Drawing(hdim_scaled + 2 * padding + 36,
                     vdim_scaled + 2 * padding + 14 + 4 + 10
                     )
    # Coordinates of the lower left corner of the rectangle
    rx = padding + 36
    ry = padding + 14
    # For the background color, use a little less red variation of
    # linen (0xfaf0e6).
    background_clr = colors.HexColor(0xf8f0e6)
    result.add(
        Rect(rx, ry, hdim_scaled, vdim_scaled, fillColor=background_clr,
             strokeWidth=0.75
             )
        )
    result.add(
        String(rx + hdim_scaled / 2,
               ry + vdim_scaled + 4,
               name,
               textAnchor='middle'
               )
        )
    result.add(hdimarrow_str(hdim, scale, rx, ry - 9, 0.67))
    result.add(vdimarrow_str(vdim, scale, rx - 9, ry, 0.67))
    if material is not None and thickness is not None:
        matl_thick_str = String(
            rx + hdim_scaled - 6, ry + vdim_scaled - 7 - 8,
            dimstr(thickness) + '"  ' + material[:3],
            textAnchor='end',
            fontSize=7
            )
        result.add(matl_thick_str)
    return result


# cutlist.py ends here
