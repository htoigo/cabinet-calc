# -*- coding: utf-8; -*-

# cabinet_calc.py

# Copyright © 2018  Harry H. Toigo II, L33b0

# This file is part of Cabinet Calc.

# Cabinet Calc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Cabinet Calc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Cabinet Calc.  If not, see <https://www.gnu.org/licenses/>.

# To contact us:
#
# Email:       hhtpub@gmail.com
#
# Snail mail:  433 Buena Vista Ave. #310
#              Alameda CA  94501


"""The Cabinet Calc main module.

This module handles processing of command-line arguments, and starting either
the CLI or the GUI as required.

Cabinet Calc is the Custom Euro-Style Cabinet Configurator.

Quickly and easily, by entering a few dimensions, configure a bank of Euro-
style cabinets. Generate a parts list with dimensions, as well as a high-
quality cutlist in PDF format, suitable for printing, to be used on the shop
floor.

Cabinet Calc has both a GUI interface for ease of use, and a command line
interface for power users and scripting capability.
"""


import sys
from os.path import dirname
import argparse
import textwrap

if __name__ == '__main__':
    # Add the project root directory to sys.path, so the import machinery can
    # find other project modules when this script is run (as opposed to being
    # imported). The project root directory should be the parent of this file's
    # directory.
    project_root_dir = dirname(dirname(__file__))
    sys.path.insert(0, project_root_dir)

from cabinet_calc.cabinet import (
    MATERIALS, PRIM_MAT_DEFAULT, DOOR_MAT_DEFAULT, Ends, Run
    )
from cabinet_calc import gui
from cabinet_calc import job
from cabinet_calc import cutlist


def start_gui():
    """Start the GUI version of the program."""
    app = gui.Application()
    app.mainloop()


def start_cli(args):
    """Start the command-line version of the program."""
    # Create a cabinet Run object which does all the calculating.
    cab_run = Run(args.fullwidth, args.height, args.depth,
                  fillers=args.fillers,
                  prim_material=args.prim_matl,
                  prim_thickness=args.prim_thick,
                  door_material=args.door_matl,
                  door_thickness=args.door_thick,
                  btmpanel_thicknesses=args.btm_thicks,
                  has_legs=args.legs)
    # Create a job object that holds the name, a single cabinet run object,
    # and an optional description for the job.
    if args.desc is not None:
        j = job.Job(args.name, cab_run, args.desc)
    else:
        j = job.Job(args.name, cab_run)

    # Output the job specification to the terminal, ensuring lines are no
    # longer than 65 chars.
    for line in j.specification:
        print(textwrap.fill(line, width=65))

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
                        help="ends that will have filler panels",
                        type=Ends.from_string,
                        choices=list(Ends),
                        default=Ends.from_string('NEITHER'))
    parser.add_argument("-pm", "--prim_matl",
                        help="primary material name",
                        metavar='MTL',
                        type=str,
                        default=MATERIALS[PRIM_MAT_DEFAULT])
    parser.add_argument("-pt", "--prim_thick",
                        help="primary thickness",
                        metavar='TH',
                        type=float)
    parser.add_argument("-dm", "--door_matl",
                        help="door material name",
                        metavar='MTL',
                        type=str,
                        default=MATERIALS[DOOR_MAT_DEFAULT])
    parser.add_argument("-dt", "--door_thick",
                        help="door thickness",
                        metavar='TH',
                        type=float)
    parser.add_argument("-l", "--legs",
                        help="add cabinet legs",
                        action="store_true")
    parser.add_argument("-bt", "--btm_thicks",
                        help="bottom panel thicknesses",
                        metavar='TH',
                        nargs='+',
                        type=float)
    parser.add_argument("-c", "--cutlist",
                        help="generate cutlist & save in FN.pdf",
                        metavar='FN',
                        type=str)
    # parser.add_argument("-ctl", "--ctopleft",
    #                     help="countertop overhang left side",
    #                     type=float)
    # parser.add_argument("-ctr", "--ctopright",
    #                     help="countertop overhang right side",
    #                     type=float)
    # parser.add_argument("-ctf", "--ctopfront",
    #                     help="countertop overhang front side",
    #                     type=float)
    return parser


def main():
    """Parse the command-line args and pass them to the CLI or start the GUI."""
    parser = get_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        # No arguments have been passed on the cmdline; start the GUI version.
        start_gui()
    else:
        start_cli(args)


if __name__ == '__main__':
    main()


# cabinet_calc.py  ends here
