#!/usr/bin/env python3

"""Cabinet-calc: generate cabinet layouts from available dimensions.

A command-line and GUI program to generate a Euro-style cabinet bank layout,
parts list, and pretty-printed cut sheet.
"""

import sys
import argparse
import math
from fractions import Fraction

import cabinet
import job
import gui


def start_gui():
    """Start the GUI version of the program."""
    app = gui.Application()
    app.mainloop()


def start_cli(args):
    """Start the command-line version of the program."""

    # How to NOT pass optional args 'material', 'thickness', et al, that
    # if not provided on the command line will have the value None?
    if args.thickness is not None:
        # Pass args.thickness to cabinet.Run(...)
        pass
    else:
        # Do not pass matl_thickness to cabinet.Run()
        pass
    
    job = job.Job(args.jobname, 'Customer 1')
    cabs = cabinet.Run(args.fullwidth, args.height, args.depth,
                       num_fillers=args.fillers, matl_thickness=args.thickness)

    # Create job description
    jobdesc = []
    jobdesc.append('-' * 60)
    jobdesc.append('JOB NAME: ' + job.name)

    # Create general overview of cabinet bank
    overview = []
    overview.append('-' * 60)
    overview.append('OVERVIEW:\n')
    overview.append('TOTAL WALL SPACE: ' + str(cabs.fullwidth) + '"')
    overview.append(str(cabs.num_cabinets) + " CABINETS MEASURING "
                    + str(cabs.cabinet_width) + '" TOTALLING '
                    + str(cabs.cabinet_width * cabs.num_cabinets) + '"')
    if cabs.num_fillers == 0:
        overview.append('WITH FINISHED END PANELS ON LEFT AND RIGHT')
        overview.append('NO FILLER PANELS REQUIRED')
    elif cabs.num_fillers == 1:
        overview.append('WITH A ' + str(cabs.filler_width) + '" FILLER')
    elif cabs.num_fillers == 2:
        overview.append('WITH TWO (2) ' + str(cabs.filler_width) + '" FILLERS')
    else:
        # Raise an exception for having fillers in the middle of a run.
        print('Your layout would have fillers in the middle of a run. WTF?\n')
    overview.append('\nMaterial thickness: ' + str(cabs.matl_thickness) + '"')

    # Create parts list, including doors
    parts = []
    parts.append('-' * 60)
    parts.append('PARTS LIST:\n')
    # Back panels
    parts.append(str(cabs.num_backpanels) + " @ "
                   + str(cabs.back_width) + '" x '
                   + str(cabs.back_height) + '" x '
                   + str(cabs.back_thickness) + '" -- BACK PNLS')
    # Bottom panels
    parts.append(str(cabs.num_bottompanels) + " @ "
                   + str(cabs.bottom_width) + '" x '
                   + str(cabs.bottom_depth) + '" x '
                   + str(cabs.bottom_thickness) + '" -- BOTTOM PNLS')
    # Side panels
    parts.append(str(cabs.num_sidepanels) + " @ "
                   + str(cabs.side_depth) + '" x '
                   + str(cabs.side_height) + '" x '
                   + str(cabs.side_thickness) + '" -- SIDE PNLS')
    # Top nailers
    parts.append(str(cabs.num_topnailers) + " @ "
                   + str(cabs.topnailer_width) + '" x '
                   + str(cabs.topnailer_depth) + '" x '
                   + str(cabs.topnailer_thickness) + '" -- TOP NAILERS')
    # Filler(s)
    if cabs.num_fillers > 0:
        parts.append(str(cabs.num_fillers) + ' @ '
                     + str(cabs.filler_width) + '" x '
                     + str(cabs.filler_height) + '" x '
                     + str(cabs.filler_thickness) + '" -- FILLERS')
    # Doors
    parts.append('DOOR DETAILS:')
    parts.append(str(cabs.num_doors) + " @ "
                   + str(cabs.door_width) + '" x '
                   + str(cabs.door_height) + '" x '
                   + str(cabs.door_thickness) + '" -- DOORS')
    parts.append('-' * 60)

    # Print job description
    for line in jobdesc:
        print(line)
    # Print general overview of cabinet bank
    for line in overview:
        print(line)
    # Print parts list, including doors
    for line in parts:
        print(line)

    # Generate PDF job sheet

    # Set the PDF output to landscape orientation

    # Set the scale
    scale = 1/16


def get_parser():
    """Create a parser for the command line arguments."""
    parser = argparse.ArgumentParser(description='Configure a bank of cabinets.')
    parser.add_argument("-w", "--fullwidth",
                        help="full bank width for all cabinets combined",
                        metavar='W',
                        type=float)
    parser.add_argument("-ht", "--height",
                        help="height from toe kick to top of cabinet",
                        metavar='HT',
                        type=float)
    parser.add_argument("-d", "--depth",
                        help="depth from front to back including door",
                        metavar='D',
                        type=float)
    parser.add_argument("-f", "--fillers",
                        help="number of fillers to be used",
                        metavar='N',
                        type=int,
                        default='0')
    parser.add_argument("-j", "--jobname",
                        help="an identifying name for the job",
                        type=str)
    parser.add_argument("-m", "--material",
                        help="primary building material name",
                        type=str)
    parser.add_argument("-th", "--thickness",
                        help="building material thickness",
                        type=float,
                        default='0.75')
    parser.add_argument("-ctl", "--ctopleft",
                        help="countertop overhang left side",
                        type=float)
    parser.add_argument("-ctr", "--ctopright",
                        help="countertop overhang right side",
                        type=float)
    parser.add_argument("-ctf", "--ctopfront",
                        help="countertop overhang front side",
                        type=float)
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        # No arguments have been passed on the cmdline; start the GUI version.
        start_gui()
    else:
        start_cli(args)
