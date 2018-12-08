# cutlist.py        -*- coding: utf-8 -*-

# Cutlist generation module for Cabinet Wiz.

# Copyright © 2018  Harry H. Toigo II, L33b0

# This file is part of Cabinet Wiz.
# Cabinet Wiz is the custom Euro-style cabinet configurator.

# Cabinet Wiz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Cabinet Wiz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Cabinet Wiz.  If not, see <https://www.gnu.org/licenses/>.

# To contact us:
#
# Email:       hhtpub@gmail.com
#
# Snail mail:  433 Buena Vista Ave. #310
#              Alameda CA  94501


"""Cabinet Wiz cutlist generation module.
"""

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
from reportlab.pdfbase.pdfmetrics import stringWidth

from cabinet import Ends, door_hinge_gap, materials, matl_abbrevs
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
                          leftMargin=0.5 * inch,
                          rightMargin=0.5 * inch,
                          topMargin=0.5 * inch,
                          bottomMargin=0.5 * inch,
                          title='Cutlist for ' + job.name,
                          #TODO: author='',
                          subject='Cabinet Wiz Cutlist Report',
                          #TODO: Get version below from program source
                          creator='Cabinet Wiz version 0.1',
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
    hdr_ht = 70           # pts
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
    result.append(Spacer(1, 24))
    result.append(isometric_view(job))
    result.append(FrameBreak())

    result.append(panels_table(job))
    result.append(Paragraph('Parts List:', heading_style))
    for line in job.partslist:
        result.append(XPreformatted(line, fixed_style))
    return result


def finished_ends(fillers):
    if fillers is Ends.neither:
        result = 'Both end panels finished.'
    elif fillers is Ends.left:
        result = 'Left end unfinished.<br/>Right end panel finished.'
    elif fillers is Ends.right:
        result = 'Left end panel finished.<br/>Right end unfinished.'
    elif fillers is Ends.both:
        result = 'Both ends unfinished.'
    return result


def hdr_table(job):
    """Return a table layout of the job header."""
    if job.description != '':
        desc = 'Description: ' + job.description
    else:
        desc = ''
    data = (
        ( Paragraph('Job Name: ' + job.name, title_style),
          Paragraph(str(job.cabs.fullwidth) + '" Wide', wallwidth_style),
          Paragraph(finished_ends(job.cabs.fillers), rt_style)
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
        ('TOPPADDING', (0,1), (2,1), 9),
        # Nice colors:  cornsilk (0xfff8dc), linen (0xfaf0e6),
        #     lightslategrey (0x778899), 0xc8d8e6.
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(0xe0e4e2))
    ]
    return Table(data, style=styleHdr, colWidths = ['50%','20%','30%'])


def inches_to_pts(line):
    """Convert a 4-tuple representing a line from inches to points.

    The line is a 4-tuple (x1, y1, x2, y2) with coordinates in inches, and the
    return value is the same line with inches converted to DTP points (1/72").
    """
    return tuple(coord * inch for coord in line)


def isometric_view(job):
    """Return a Drawing of the isometric view of a single cabinet."""

    # Determine the width and height required for the drawing.

    # The below distances are all in points, unless noted otherwise.

    # Extra space at top of drawing, for separation from text above.
    top_margin = 10
    # Extra width added so long vdim text doesn't go past right edge.
    long_vdimtxt_margin = 30
    # The length of the dimension bounds lines.
    boundsln_len = 14
    # If the bounds line is angled, half of its vertical projection.
    half_boundsln_vert = math.sqrt((boundsln_len / 2) ** 2 / 2)
    # The separation of the arrowhead from the nearest cabinet corner.
    arrow_sep = 18
    # If the arrow separation is angled, its vertical projection.
    arrow_sep_vert = math.sqrt(arrow_sep ** 2 / 2)
    # The horizontal projection is the same, since the angle is 45 degrees.
    arrow_sep_horiz = arrow_sep_vert

    # The horizontal (or vertical, since they are equal) projection of the
    # angled cabinet depth lines -- in inches, unscaled.
    iso45 = math.sin(math.radians(45)) * job.cabs.cabinet_depth / 2

    d_width = ( (job.cabs.cabinet_width + iso45) * inch * default_iso_scale
                + arrow_sep + boundsln_len/2 + long_vdimtxt_margin )
    d_ht = ( (job.cabs.cabinet_height + iso45) * inch * default_iso_scale
             + arrow_sep_vert + half_boundsln_vert + top_margin )

    result = Drawing(d_width, d_ht)
    result.hAlign = 'CENTER'

    # The horizontal (or vertical, since they are equal) projection of the
    # angled topnailer depth lines -- in inches, unscaled.
    isoNlr45 = job.cabs.topnailer_depth * math.sin(math.radians(45)) / 2

    # Construct a list of the lines that make up the isometric view of a single
    # cabinet. Each line is a tuple in (x1, y1, x2, y2) format, and all
    # coordinates are in inches, unscaled. These are converted to points and
    # then scaled, below.

    isoLines = [
        # horizontal lines------------------------------------------------------

        # horizontal bottom inner line
        (job.cabs.side_thickness, job.cabs.bottom_thickness,
         job.cabs.cabinet_width - job.cabs.side_thickness,
         job.cabs.bottom_thickness),

        # Front nailer - front edge bottom
        (job.cabs.side_thickness,
         job.cabs.cabinet_height - job.cabs.topnailer_thickness,
         job.cabs.cabinet_width - job.cabs.side_thickness,
         job.cabs.cabinet_height - job.cabs.topnailer_thickness),

        # Back panel top rear edge
        (iso45, job.cabs.cabinet_height + iso45,
         iso45 + job.cabs.cabinet_width, iso45 + job.cabs.cabinet_height),

        # Back panel top front edge
        (iso45 - job.cabs.back_thickness * math.sin(math.radians(45)),
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)),
         job.cabs.cabinet_width + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)),
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45))),

        # horizontal inside at bottom back
        (iso45, iso45,
         job.cabs.cabinet_width - job.cabs.side_thickness, iso45),

        # Front nailer - top rear edge
        (job.cabs.side_thickness + isoNlr45, job.cabs.cabinet_height + isoNlr45,
         job.cabs.cabinet_width - job.cabs.side_thickness + isoNlr45,
         job.cabs.cabinet_height + isoNlr45),

        # Back nailer - top front edge
        (job.cabs.side_thickness + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45,
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45,
         job.cabs.cabinet_width - job.cabs.side_thickness + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45,
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45),

        # Back nailer - bottom front edge
        (job.cabs.side_thickness + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45,
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45
             - job.cabs.topnailer_thickness,
         job.cabs.cabinet_width - job.cabs.side_thickness + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45
             - job.cabs.topnailer_thickness,
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45
             - job.cabs.topnailer_thickness),

        # Vertical lines--------------------------------------------------------

        # Vertical left inner line
        (job.cabs.side_thickness, 0,
         job.cabs.side_thickness, job.cabs.cabinet_height),

        # Vertical right inner line
        (job.cabs.cabinet_width - job.cabs.side_thickness, 0,
         job.cabs.cabinet_width - job.cabs.side_thickness, job.cabs.cabinet_height),

        # Vertical right back
        (job.cabs.cabinet_width + iso45, iso45,
         job.cabs.cabinet_width + iso45, job.cabs.cabinet_height + iso45),

        # Vertical right back inner
        (job.cabs.cabinet_width + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)),
         iso45 - job.cabs.back_thickness * math.sin(math.radians(45)),
         job.cabs.cabinet_width + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)),
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45))),

        # Back nailer - front left edge
        (job.cabs.side_thickness + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45,
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45
             - job.cabs.topnailer_thickness,
         job.cabs.side_thickness + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45,
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45),

        # Vertical inside line between nailers
        (iso45, job.cabs.cabinet_height + isoNlr45,
         iso45, job.cabs.cabinet_height + iso45
                - job.cabs.back_thickness * math.sin(math.radians(45)) - isoNlr45
                - job.cabs.topnailer_thickness),

        # Vertical inside line at back of left side
        (iso45, iso45,
         iso45, job.cabs.cabinet_height - job.cabs.topnailer_thickness),

        # Angled lines----------------------------------------------------------

        # Iso bottom left inner angle
        (job.cabs.side_thickness, job.cabs.bottom_thickness,
         iso45, iso45),

        # Iso upper left angle
        (0, job.cabs.cabinet_height,
         iso45, job.cabs.cabinet_height + iso45),

        # Iso upper left angle inner
        (job.cabs.side_thickness, job.cabs.cabinet_height,
         job.cabs.side_thickness + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)),
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45))),

        # Iso upper right angle
        (job.cabs.cabinet_width, job.cabs.cabinet_height,
         job.cabs.cabinet_width + iso45, job.cabs.cabinet_height + iso45),

        # Iso upper right angle inner
        (job.cabs.cabinet_width - job.cabs.side_thickness,
         job.cabs.cabinet_height,
         job.cabs.cabinet_width - job.cabs.side_thickness + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45)),
         job.cabs.cabinet_height + iso45
             - job.cabs.back_thickness * math.sin(math.radians(45))),

        # Iso lower right angle
        (job.cabs.cabinet_width, 0,
         job.cabs.cabinet_width + iso45, iso45),

        # Front cabinet rectangle lines (originally drawn as a Rect)

        # Horizontal bottom line
        (0, 0, job.cabs.cabinet_width, 0),

        # Horizontal top line
        (0, job.cabs.cabinet_height,
         job.cabs.cabinet_width, job.cabs.cabinet_height),

        # Vertical left line
        (0, 0, 0, job.cabs.cabinet_height),

        # Vertical right line
        (job.cabs.cabinet_width, 0,
         job.cabs.cabinet_width, job.cabs.cabinet_height)
    ]
    isoLines_pts = [inches_to_pts(line) for line in isoLines]
    isoLines_scaled = [
        (coord * default_iso_scale for coord in line) for line in isoLines_pts
        ]

    for line in isoLines_scaled:
        result.add(Line(*line, strokeWidth=0.5))

    # Height dimension arrow
    vdim = job.cabs.cabinet_height
    # (x,y) of back right bottom of cabinet, scaled
    brb_x_scaled = (job.cabs.cabinet_width + iso45) * inch * default_iso_scale
    brb_y_scaled = iso45 * inch * default_iso_scale
    arr = vdimarrow_iso_str(
        vdim, default_iso_scale,
        brb_x_scaled + arrow_sep_horiz, brb_y_scaled + arrow_sep_vert,
        0.67, boundsln_len
        )
    result.add(arr)

    # Width dimension arrow
    hdim = job.cabs.cabinet_width
    # (x,y) of back left top of cabinet, scaled
    blt_x_scaled = iso45 * inch * default_iso_scale
    blt_y_scaled = (job.cabs.cabinet_height + iso45) * inch * default_iso_scale
    arr = hdimarrow_iso_str(
        hdim, default_iso_scale,
        blt_x_scaled + arrow_sep_horiz, blt_y_scaled + arrow_sep_vert,
        0.67, boundsln_len
        )
    result.add(arr)

    # Depth dimension arrow
    ddim = job.cabs.cabinet_depth - job.cabs.door_thickness - door_hinge_gap
    cabwidth_scaled = job.cabs.cabinet_width * inch * default_iso_scale
    arr = ddimarrow_iso_str(
        ddim, default_iso_scale,
        cabwidth_scaled + arrow_sep, 0,
        0.67, boundsln_len
        )
    result.add(arr)
    return result


def hdimarrow(dim, scale, x, y, strwid, boundsln_len):
    """Return a horizontal dimension arrow for a flat panel drawing.

    The return value is a Group.

    dim           is the dimension measurement.
    scale         is the scale of the drawing.
    x, y          are the coordinates of the left end of the arrow.
    strwid        is the stroke width of the lines.
    boundsln_len  is the length of the dimension bounds lines.
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


def hdimarrow_iso(dim, scale, x, y, strwid, boundsln_len):
    """Return a horizontal dimension arrow for the isometric drawing.

    The isometric version of the dimension arrow has angled boundary lines
    and arrowheads.

    dim           is the dimension measurement.
    scale         is the scale of the drawing.
    x, y          are the coordinates of the left end of the arrow.
    strwid        is the stroke width of the lines.
    boundsln_len  is the length of the dimension bounds lines.
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


def hdimarrow_str(dim, scale, x, y, strwid, boundsln_len):
    """Return a horizontal dimension arrow with labeled measurement."""
    result = hdimarrow(dim, scale, x, y, strwid, boundsln_len)
    add_hdimstr(result, dim, scale, x, y)
    return result


def hdimarrow_iso_str(dim, scale, x, y, strwid, boundsln_len):
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


def vdimarrow(dim, scale, x, y, strwid, boundsln_len):
    """Return a vertical dimension arrow for a flat panel drawing.

    The return value is a Group.

    dim           is the dimension measurement.
    scale         is the scale of the drawing.
    x, y          are the coordinates of the bottom end of the arrow.
    strwid        is the stroke width of the lines.
    boundsln_len  is the length of the dimension bounds lines.
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


def vdimarrow_iso(dim, scale, x, y, strwid, boundsln_len):
    """Return a vertical dimension arrow for the isometric drawing.

    The isometric version of the dimension arrow has angled boundary lines
    and arrowheads.

    dim           is the dimension measurement.
    scale         is the scale of the drawing.
    x, y          are the coordinates of the bottom end of the arrow.
    strwid        is the stroke width of the lines.
    boundsln_len  is the length of the dimension bounds lines.
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


def vdimarrow_str(dim, scale, x, y, strwid, boundsln_len):
    """Return a vertical dimension arrow with labeled measurement."""
    result = vdimarrow(dim, scale, x, y, strwid, boundsln_len)
    add_vdimstr(result, dim, scale, x, y, boundsln_len)
    return result


def vdimarrow_iso_str(dim, scale, x, y, strwid, boundsln_len):
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


def ddimarrow_iso(dim, scale, x, y, strwid, boundsln_len):
    """Return a depth dimension arrow for the isometric drawing.

    The isometric version of the dimension arrow has angled boundary lines
    and arrowheads.

    dim           is the dimension measurement.
    scale         is the scale of the drawing.
    x, y          are the coordinates of the lower left end of the arrow.
    strwid        is the stroke width of the lines.
    boundsln_len  is the length of the dimension bounds lines.
    """
    dim_scaled = dim * inch * scale
    # `iso45' is divided by 2 below because that is how it's calculated
    # in the isometric_view, above.
    iso45 = math.sin(math.radians(45)) * dim_scaled / 2
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


def ddimarrow_iso_str(dim, scale, x, y, strwid, boundsln_len):
    """Return an isometric depth dimension arrow with labeled measurement."""
    result = ddimarrow_iso(dim, scale, x, y, strwid, boundsln_len)
    add_ddimstr_iso(result, dim, scale, x, y, boundsln_len)
    return result


def add_ddimstr_iso(arrow, dim, scale, x, y, boundsln_len):
    """Add a measurement label to the given isometric depth dimension arrow."""
    dim_scaled = dim * inch * scale
    # `iso45' is divided by 2 below because that is how it's calculated
    # in the isometric_view, above.
    iso45 = math.sin(math.radians(45)) * dim_scaled / 2
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
        material=job.cabs.prim_material, thickness=job.cabs.back_thickness
        )
    bottompanel_dr = panel_drawing(
        'Bottom', job.cabs.bottom_width, job.cabs.bottom_depth,
        material=job.cabs.prim_material, thickness=job.cabs.bottom_thickness
        )
    sidepanel_dr = panel_drawing(
        'Side', job.cabs.side_depth, job.cabs.side_height,
        material=job.cabs.prim_material, thickness=job.cabs.side_thickness
        )
    # Nailer scale may need to be 1/16 for hdim to fit
    topnailer_dr = panel_drawing(
        'Nailer', job.cabs.topnailer_depth, job.cabs.topnailer_width
        )
    # Door scale may need to be 1/20 for hdim to fit
    door_dr = panel_drawing(
        'Door', job.cabs.door_width, job.cabs.door_height,
        material=job.cabs.door_material, thickness=job.cabs.door_thickness
        )
    # Create table for layout of the panel drawings
    colWidths = ('35%', '35%', '30%')
    rowHeights = (130, 130)       # assumes col_ht of 411 pts
                                  # 6.5 * 72 - 45 - 12
    if job.cabs.fillers is Ends.neither:
        # No fillers used; do not create a filler panel drawing.
        data = ( (backpanel_dr, sidepanel_dr, topnailer_dr),
                 (bottompanel_dr, door_dr)
                 )
    else:
        # Fillers are used, we need a filler panel drawing.
        filler_dr = panel_drawing(
            'Filler', job.cabs.filler_width, job.cabs.filler_height
        )
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
    boundsln_len = 10
    result.add(hdimarrow_str(hdim, scale, rx, ry - 9, 0.67, boundsln_len))
    result.add(vdimarrow_str(vdim, scale, rx - 9, ry, 0.67, boundsln_len))
    if material is not None and thickness is not None:
        matl = matl_abbrevs[material]
        # Default Graphics FontName is Times-Roman.
        font_nm = 'Helvetica'
        font_sz = 6    # 6 if len(matl) > 4 else 7
        str_wd = stringWidth(matl, font_nm, font_sz)    # in points
        rt_padding = min(6, (hdim_scaled - str_wd) / 2)
        str_x = rx + hdim_scaled - rt_padding

        thickn = dimstr(thickness) + '"'
        thick_str = String(
            str_x, ry + vdim_scaled - 7 - 8,
            thickn,
            textAnchor='end',
            fontName=font_nm,
            fontSize=7
            )
        result.add(thick_str)
        matl_str = String(
            str_x, ry + vdim_scaled - 7 - 8 - 8,
            matl,
            textAnchor='end',
            fontName=font_nm,
            fontSize= 6
            )
        result.add(matl_str)
    return result


# cutlist.py ends here
