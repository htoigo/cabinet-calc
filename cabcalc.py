#!/usr/bin/env python3

"""Cabinet-calc: generate cabinet layouts from available dimensions.

A command-line and GUI program to generate a Euro-style cabinet bank layout,
parts list, and pretty-printed cut sheet.
"""

import sys
import argparse

import cabinet as cab
import job
import gui


def start_gui():
    """Start the GUI version of the program."""
    app = gui.Application()
    app.mainloop()


def start_cli(args):
    """Start the command-line version of the program."""

    j = job.Job(args.jobname, 'Customer 1',
                cab.Run(args.fullwidth, args.height, args.depth,
                        num_fillers=args.fillers,
                        matl_thickness=args.thickness))
    for line in j.description():
        print(line)
    # TODO: Generate PDF job sheet, if requested.


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
