#!/usr/bin/env python3        -*- coding: utf-8 -*-

# cabcalc.py  --  The main executable for Cabinet Calc.


"""Cabinet Calc: generate a cabinet layout to fit given dimensions.

A command-line and GUI program to generate a Euro-style cabinet bank layout,
parts list, and pretty-printed cut sheet.
"""


import sys
import argparse
import textwrap

import gui
import cabinet as cab
import job
import cutlist
from text import wrap


def start_gui():
    """Start the GUI version of the program."""
    app = gui.Application()
    app.mainloop()


def start_cli(args):
    """Start the command-line version of the program."""

    # Create a cabinet Run object which does all the calculating.
    cab_run = cab.Run(args.fullwidth, args.height, args.depth,
                      num_fillers=args.fillers,
                      matl_thickness=args.thick)
    # Create a job object that holds the name, a single cabinet run object,
    # and an optional description for the job.
    if args.desc is not None:
        j = job.Job(args.name, cab_run, args.desc)
    else:
        j = job.Job(args.name, cab_run)

    # Output the job specification to the terminal, ensuring lines are no
    # longer than 60 chars.
    for line in wrap(j.specification, 60):
        print(line)

    # If requested, produce and save a cutlist pdf file.
    if args.cutlist is not None:
        # Generate a cutlist pdf and save in file given by args.cutlist
        cutlist.save_cutlist(args.cutlist, j)


def get_parser():
    """Create a parser for the command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Configure a one-off job consisting of a single bank of cabinets.

            Passing no arguments starts the GUI version of Cabinet Calc.
            When running the command line version, the following arguments are
            REQUIRED:  -w WIDTH -ht HT -d DEPTH -n NAME
            Otherwise, there is not enough information to compute the job.
            '''))
    parser.add_argument('-w', '--fullwidth',
                        help='full bank width for all cabinets combined',
                        metavar='WIDTH',
                        type=float)
    parser.add_argument('-ht', '--height',
                        help="height from toe kick to top of cabinet",
                        metavar='HT',
                        type=float)
    parser.add_argument('-d', '--depth',
                        help="depth from front to back including door",
                        metavar='DEPTH',
                        type=float)
    parser.add_argument('-n', "--name",
                        help="a unique identifying name for the job",
                        metavar='NAME',
                        type=str)
    parser.add_argument("-s", "--desc",
                        help="a description of the job",
                        metavar='DESC',
                        type=str)
    parser.add_argument("-f", "--fillers",
                        help="number of fillers to be used (0, 1, or 2); "
                             "if unspecified, defaults to 0",
                        metavar='N',
                        type=int,
                        default='0')
    parser.add_argument("-m", "--matl",
                        help="primary building material name",
                        type=str)
    parser.add_argument("-th", "--thick",
                        help="building material thickness",
                        metavar='TH',
                        type=float,
                        default='0.75')
    parser.add_argument("-c", "--cutlist",
                        help="generate a cutlist & save in FN.pdf",
                        metavar='FN',
                        type=str)
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


# cabcalc.py ends here
