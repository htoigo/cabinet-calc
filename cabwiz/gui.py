# gui.py        -*- coding: utf-8 -*-

# Module implementing the Tkinter GUI for Cabinet Wiz.

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


"""Cabinet Wiz GUI module.

This module implements the Cabinet Wiz GUI.
"""


#__all__ = [max_cabinet_width, door_hinge_gap, cabinet_run, num_cabinets,
#           Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import reduce

import cabinet as cab
import job
import cutlist
from text import wrap


class Application(ttk.Frame):
    """The application, which is the main content frame in the root window."""
    def __init__(self, root=None, title='Cabinet Wiz'):
        if root is None:
            # Create a new root window to be our master
            self.root = Tk()
        else:
            # Our master will be what was passed in as `root'
            self.root = root
        super().__init__(self.root, padding=5)
        # Instance variables
        self.root.title(title)
        self.jobname = StringVar()
        self.description = StringVar()
        self.fullwidth = StringVar()
        self.height = StringVar()
        self.depth = StringVar()
        self.num_fillers = IntVar()
        self.material = StringVar()
        self.thickness = StringVar()
        self.diff_btm_thickness = StringVar()
        self.bottom_thickness = StringVar()
        self.doors_per_cab = IntVar()
        self.output = StringVar()
        self.job = None
        self.initialize_vars()
        self.make_widgets()

    def initialize_vars(self):
        self.jobname.set('')
        self.description.set('')
        self.fullwidth.set('')
        self.height.set('')
        self.depth.set('')
        self.num_fillers.set(0)
        self.material.set('Plywood')
        self.thickness.set('0.75')
        self.diff_btm_thickness.set('no')
        self.bottom_thickness.set('')
        self.doors_per_cab.set(2)
        self.output.set('No job yet.')
        self.job = None

    def make_widgets(self):
        """Create and layout all the UI elements.

        Only the widgets that need to be refered to in other parts of the code
        are made as instance variables (with `self.').
        """
        ttk.Label(self, text='The Custom Euro-Style Cabinet Configurator').grid(
            column=0, row=0, sticky=W)
        inputframe = ttk.Labelframe(self, text='Parameters: ', borderwidth=2,
            relief='groove', padding=5)
        ttk.Label(self, text='Job Specification:').grid(
            column=0, row=2, sticky=W, pady=2)
        outputframe = ttk.Frame(self, borderwidth=1, relief='sunken',
                                padding=5)
        outp_btnsframe = ttk.Frame(self, padding=(0, 10))
        self.grid(column=0, row=0, sticky=(N, S, W, E))
        inputframe.grid(column=0, row=1, sticky=(N, S, W, E), pady=10)
        outputframe.grid(column=0, row=3, sticky=(N, S, W, E))
        outp_btnsframe.grid(column=0, row=4, sticky=(N, S, W, E))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.fill_inputframe(inputframe)
        self.fill_outputframe(outputframe)
        self.fill_outp_btnsframe(outp_btnsframe)

    def fill_inputframe(self, inpframe):

        def make_jobframe():
            jobframe = ttk.Frame(inpframe, padding=(0, 5, 0, 10))
            jobframe.grid(column=0, row=0, sticky=(N, S, W, E))
            jobframe.columnconfigure(0, weight=0)
            jobframe.columnconfigure(1, weight=1)
            ttk.Label(jobframe, text='Job Name:').grid(
                column=0, row=0, pady=2, sticky=W)
            self.jobname_ent = ttk.Entry(jobframe, textvariable=self.jobname,
                validate='key', validatecommand=(vcmd, '%P'))
            ttk.Label(jobframe, text='Description:').grid(
                column=0, row=1, pady=2, sticky=W)
            self.descrip_ent = ttk.Entry(
                jobframe, textvariable=self.description, validate='key',
                validatecommand=(vcmd, '%P'))
            self.jobname_ent.grid(column=1, row=0, pady=2, sticky=(W, E),
                                  padx=(5, 0))
            self.descrip_ent.grid(column=1, row=1, pady=2, sticky=(W, E),
                                  padx=(5, 0))
            self.jobname_ent.focus_set()

        def make_dimframe():
            dimframe = ttk.Frame(inpframe, padding=(0, 10))
            dimframe.grid(column=0, row=1, sticky=(N, S, W, E))
            dimframe.columnconfigure(0, weight=0)
            dimframe.columnconfigure(1, weight=1)
            dimframe.columnconfigure(2, weight=0)
            dimframe.columnconfigure(3, weight=1)
            dimframe.columnconfigure(4, weight=0)
            dimframe.columnconfigure(5, weight=1)
            ttk.Label(dimframe, text='Width:').grid(
                column=0, row=0, sticky=W, padx=(0, 3))
            self.fullwidth_ent = ttk.Entry(dimframe, width=10,
                textvariable=self.fullwidth, validate='key',
                validatecommand=(vcmd, '%P'))
            ttk.Label(dimframe, text='Height:').grid(
                column=2, row=0, sticky=E, padx=(6, 3))
            self.height_ent = ttk.Entry(dimframe, width=10,
                textvariable=self.height, validate='key',
                validatecommand=(vcmd, '%P'))
            ttk.Label(dimframe, text='Depth:').grid(
                column=4, row=0, sticky=E, padx=(6, 3))
            self.depth_ent = ttk.Entry(dimframe, width=10,
                textvariable=self.depth, validate='key',
                validatecommand=(vcmd, '%P'))
            self.fullwidth_ent.grid(column=1, row=0, sticky=(W, E), padx=3)
            self.height_ent.grid(column=3, row=0, sticky=(W, E), padx=3)
            self.depth_ent.grid(column=5, row=0, sticky=(W, E), padx=3)

        def make_miscframe():
            miscframe = ttk.Frame(inpframe, padding=(0, 5))
            miscframe.grid(column=0, row=2, sticky=(N, S, W, E))
            miscframe.columnconfigure(0, weight=0)
            miscframe.columnconfigure(1, weight=0)
            miscframe.columnconfigure(2, weight=0)
            miscframe.columnconfigure(3, weight=0)
            miscframe.columnconfigure(4, weight=1)
            miscframe.columnconfigure(5, weight=1)
            miscframe.columnconfigure(6, weight=1)
            ttk.Label(miscframe, text='Number of fillers:').grid(
                column=0, columnspan=2, row=0, sticky=W, padx=(0, 2), pady=2)
            ttk.Radiobutton(miscframe, value=0, text='0',
                            variable=self.num_fillers).grid(
                                column=2, row=0, sticky=W, padx=3, pady=2)
            ttk.Radiobutton(miscframe, value=1, text='1',
                            variable=self.num_fillers).grid(
                                column=3, row=0, sticky=W, padx=3, pady=2)
            ttk.Radiobutton(miscframe, value=2, text='2',
                            variable=self.num_fillers).grid(
                                column=4, row=0, sticky=W, padx=3, pady=2)
            ttk.Label(miscframe, text='Material:').grid(
                column=0, row=1, sticky=W, padx=(0, 2), pady=2)
            material_cbx = ttk.Combobox(miscframe, textvariable=self.material,
                                width=max(map(len, cab.materials)) + 2)
            material_cbx['values'] = cab.materials
            # Prevent direct editing of the value in the combobox:
            material_cbx.state(['readonly'])
            # Call the `selection clear' method when the value changes. It looks
            # a bit odd visually without doing that.
            material_cbx.bind('<<ComboboxSelected>>',
                              lambda x: material_cbx.selection_clear())
            material_cbx.grid(column=1, columnspan=2, row=1, sticky=W,
                              padx=(6, 0), pady=2)
            ttk.Label(miscframe, text='Thickness:').grid(
                column=4, row=1, sticky=E, padx=4, pady=2)
            ttk.Entry(miscframe, textvariable=self.thickness,
                      width=6).grid(column=5, row=1, sticky=W, pady=2)
            bottom_thickness_chk = ttk.Checkbutton(
                miscframe, text='Different Bottom Thickness:',
                command=self.diff_btm_changed, variable=self.diff_btm_thickness,
                onvalue='yes', offvalue='no').grid(
                    column=1, columnspan=4, row=2, sticky=E, padx=4, pady=2)
            self.bottom_thickness_ent = ttk.Entry(
                miscframe, textvariable=self.bottom_thickness, width=6
            )
            self.bottom_thickness_ent.state(['disabled'])
            self.bottom_thickness_ent.grid(column=5, row=2, sticky=W, pady=2)
            ttk.Label(miscframe, text='Doors per Cabinet:').grid(
                column=0, columnspan=2, row=3, sticky=W, padx=(0, 6), pady=(10, 2))
            drs_per_cab_rb1 = ttk.Radiobutton(
                miscframe, value=1, text='1', variable=self.doors_per_cab
            )
            # Do not allow selection of one door per cabinet. This can only be
            # enabled after major code changes throughout, to allow for upper
            # cabinet banks, variable height/width cabinets, etc.
            drs_per_cab_rb1.state(['disabled'])
            drs_per_cab_rb1.grid(column=2, row=3, sticky=W, padx=3, pady=(10, 2))
            ttk.Radiobutton(miscframe, value=2, text='2',
                variable=self.doors_per_cab).grid(
                    column=3, row=3, sticky=W, padx=3, pady=(10, 2))

        def make_buttonframe():
            buttonframe = ttk.Frame(inpframe, padding=(0, 12, 0, 0))
            buttonframe.grid(column=0, row=3, sticky=(N, S, W, E))
            buttonframe.columnconfigure(0, weight=1)
            buttonframe.columnconfigure(1, weight=1)
            buttonframe.columnconfigure(2, weight=1)
            buttonframe.rowconfigure(0, weight=1)
            self.calc_button = ttk.Button(buttonframe, text='Calculate',
                                          command=self.calculate_job)
            self.calc_button.state(['disabled'])
            clear_button = ttk.Button(buttonframe, text='Clear',
                                      command=self.clear_input)
            quit_button = ttk.Button(buttonframe, text='Quit',
                                     command=self.quit)
            self.calc_button.grid(column=0, row=0, sticky=E, padx=2)
            clear_button.grid(column=1, row=0, sticky=W, padx=2)
            quit_button.grid(column=2, row=0, padx=2)

        # Register our validate function to get its function ID. This is used
        # to disable the `Calculate' button if the fields necessary for
        # calculation are not filled in.
        vcmd = self.root.register(self.validate_entry)
        make_jobframe()
        make_dimframe()
        make_miscframe()
        make_buttonframe()
        inpframe.columnconfigure(0, weight=1)

    def fill_outputframe(self, outpframe):
        self.output_lbl = ttk.Label(outpframe, textvariable=self.output,
                                    font='TkFixedFont')
        self.output_lbl.grid(column=0, row=0, sticky=(N, S, E, W), pady=(0, 50))

    def fill_outp_btnsframe(self, outp_btnsframe):
        outp_btnsframe.columnconfigure(0, weight=1)
        outp_btnsframe.columnconfigure(1, weight=1)
        outp_btnsframe.rowconfigure(0, weight=1)
        self.cutlist_button = ttk.Button(
            outp_btnsframe, text='Save Cutlist', command=self.save_cutlist)
        self.cutlist_button.state(['disabled'])
        self.panel_layout_btn = ttk.Button(
            outp_btnsframe, text='Optimize Panel Layout',
            command=self.optimize_panel_layout)
        self.panel_layout_btn.state(['disabled'])
        self.cutlist_button.grid(column=0, row=0, sticky=E, padx=2)
        self.panel_layout_btn.grid(column=1, row=0, sticky=W, padx=2)

    def validate_entry(self, value):
        if self.have_enough_info():
            self.calc_button.state(['!disabled'])
        else:
            self.calc_button.state(['disabled'])
        return True

    def have_enough_info(self):
        result = (self.jobname_ent.get() != ''
                  and self.fullwidth_ent.get() != ''
                  and self.height_ent.get() != ''
                  and self.depth_ent.get() != '')
        return result

    def diff_btm_changed(self):
        if self.diff_btm_thickness.get() == 'yes':
            self.bottom_thickness_ent.state(['!disabled'])
        else:
            self.bottom_thickness.set('')
            self.bottom_thickness_ent.state(['disabled'])

    def quit(self):
        # Destroying the app's top-level window quits the app.
        self.root.destroy()

    def clear_input(self):
        self.initialize_vars()
        self.bottom_thickness_ent.state(['disabled'])
        self.calc_button.state(['disabled'])
        self.cutlist_button.state(['disabled'])
        self.panel_layout_btn.state(['disabled'])
        self.output_lbl.grid_configure(pady=(0, 50))

    def calculate_job(self):
        cab_run = cab.Run(float(self.fullwidth.get()),
                          float(self.height.get()),
                          float(self.depth.get()),
                          num_fillers=self.num_fillers.get(),
                          material=self.material.get(),
                          matl_thickness=float(self.thickness.get()))
        if self.description.get() != '':
            self.job = job.Job(self.jobname.get(), cab_run,
                               self.description.get())
        else:
            self.job = job.Job(self.jobname.get(), cab_run)
        # Ensure output lines are no longer than 60 chars
        self.output.set('\n'.join(wrap(self.job.specification, 60)))
        self.output_lbl.grid_configure(pady=0)
        self.cutlist_button.state(['!disabled'])

    def save_cutlist(self):
        """Generate a cutlist pdf and save in file chosen by user."""
        filename = filedialog.asksaveasfilename(
            title='Filename to Save Cutlist As',
            parent=self.root,
            filetypes=(('PDF Files', '*.pdf'), ('All Files', '*')))
        if filename != '':
            cutlist.save_cutlist(filename, self.job)

    def optimize_panel_layout(self):
        pass


# gui.py ends here
