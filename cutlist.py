"""Cutlist module."""

from reportlab.pdfgen import canvas as canv
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

# Interface

# Global variables

scale = 1 / 16


def save_cutlist(fname, job):
    """Generate a cutlist for the job and save in fname."""
    c = canv.Canvas(fname + ".pdf", pagesize=letter)
    # TODO: Set landscape mode.
    draw_isoview(c)
    drawtxt_jobheader(c)
    drawtxt_overview(c)
    drawtxt_partslist(c)
    draw_panels(c)
    c.showPage()
    c.save()


# Implementation


def draw_isoview(canvas):
    pass

def drawtxt_jobheader(canvas):
    pass

def drawtxt_overview(canvas):
    pass

def drawtxt_partslist(canvas):
    pass

def draw_panels(canvas):
    pass
