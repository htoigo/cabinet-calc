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


from functools import reduce
import textwrap
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from .cabinet import (
    materials, matl_thicknesses, prim_mat_default, door_mat_default, Ends, Run
    )
from . import job
from . import cutlist


def yn_to_bool(str):
    """True if str is 'y' or 'yes', False if str is 'n' or 'no', else error.

    String matching is case-insensitive.

    We need the function yn_to_bool because the built-in function bool() does
    not do what we want. For example, bool('no') returns True.
    """
    if str.lower() in ['y', 'yes']:
        result = True
    elif str.lower() in ['n', 'no']:
        result = False
    else:
        raise ValueError('str is not one of "y", "yes", "n" or "no"')
    return result


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
        self.fillers = StringVar()
        self.prim_material = StringVar()
        self.prim_thickness = StringVar()
        self.door_material = StringVar()
        self.door_thickness = StringVar()
        self.legs = StringVar()
        self.bottom_thickness = StringVar()
        self.btmpanel1_thickness = StringVar()
        self.btmpanel2_thickness = StringVar()
        self.stacked_btm = StringVar()
        self.btm_material = StringVar()
        self.doors_per_cab = IntVar()
        self.output = ''
        self.job = None
        self.initialize_vars()
        self.make_widgets()

    def initialize_vars(self):
        self.jobname.set('')
        self.description.set('')
        self.fullwidth.set('')
        self.height.set('')
        self.depth.set('')
        self.fillers.set('neither')
        self.prim_material.set(materials[prim_mat_default])
        self.prim_thickness.set(matl_thicknesses[self.prim_material.get()][0])
        self.door_material.set(materials[door_mat_default])
        self.door_thickness.set(matl_thicknesses[self.door_material.get()][0])
        self.legs.set('no')
        self.bottom_thickness.set('')
        self.btmpanel1_thickness.set('')
        self.btmpanel1_thickness.trace('w', self.btmpnl_thickness_changed)
        self.btmpanel2_thickness.set('')
        self.btmpanel2_thickness.trace('w', self.btmpnl_thickness_changed)
        self.stacked_btm.set('no')
        self.btm_material.set('')
        self.doors_per_cab.set(2)
        self.output = 'No job yet.'
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
        outputframe = ttk.Frame(self, borderwidth=1, relief='sunken')
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
            ttk.Label(miscframe, text='Fillers for which ends?').grid(
                column=0, columnspan=2, row=0, sticky=W, padx=(0, 2), pady=2)
            ttk.Radiobutton(miscframe, value='neither', text='Neither',
                            variable=self.fillers).grid(
                                column=2, row=0, sticky=W, padx=3, pady=2)
            ttk.Radiobutton(miscframe, value='left', text='Left',
                            variable=self.fillers).grid(
                                column=3, row=0, sticky=W, padx=3, pady=2)
            ttk.Radiobutton(miscframe, value='right', text='Right',
                            variable=self.fillers).grid(
                                column=4, row=0, sticky=W, padx=3, pady=2)
            ttk.Radiobutton(miscframe, value='both', text='Both',
                            variable=self.fillers).grid(
                                column=5, row=0, sticky=W, padx=3, pady=2)

            ttk.Label(miscframe, text='Material:').grid(
                column=1, row=1, sticky=(N, W), padx=4, pady=(15, 2))
            ttk.Label(miscframe, text='Thickness:').grid(
                column=2, row=1, sticky=W, padx=4, pady=(15, 2))

            ttk.Label(
                miscframe, text='Measure actual material thickness to the\n'
                                'nearest 0.01" and adjust values accordingly.'
            ).grid(column=3, columnspan=3, row=2, rowspan=2, sticky=(N,W),
                   padx=(8,4), pady=2)

            ttk.Label(miscframe, text='Primary:').grid(
                column=0, row=2, sticky=W, padx=(0, 2), pady=2)
            self.prim_material_cbx = ttk.Combobox(
                miscframe, textvariable=self.prim_material,
                width=max(map(len, materials)) - 2
            )
            self.prim_material_cbx['values'] = materials
            # Prevent direct editing of the value in the combobox:
            self.prim_material_cbx.state(['readonly'])
            # Call the `selection clear' method when the value changes. It looks
            # a bit odd visually without doing that.
            self.prim_material_cbx.bind('<<ComboboxSelected>>',
                                        self.prim_material_changed)
            self.prim_material_cbx.grid(column=1, row=2,
                                        sticky=W, padx=(6, 3), pady=2)
            ttk.Entry(miscframe, textvariable=self.prim_thickness,
                      width=6).grid(column=2, row=2, padx=6, pady=2)

            ttk.Label(miscframe, text='Doors:').grid(
                column=0, row=3, sticky=W, padx=(0, 2), pady=2)
            self.door_material_cbx = ttk.Combobox(
                miscframe, textvariable=self.door_material,
                width=max(map(len, materials)) - 2
            )
            self.door_material_cbx['values'] = materials
            # Prevent direct editing of the value in the combobox:
            self.door_material_cbx.state(['readonly'])
            # Call the `selection clear' method when the value changes. It looks
            # a bit odd visually without doing that.
            self.door_material_cbx.bind('<<ComboboxSelected>>',
                                        self.door_material_changed)
            self.door_material_cbx.grid(column=1, row=3,
                                        sticky=W, padx=(6, 3), pady=2)

            # ttk.Label(miscframe, text='Thickness:').grid(
            #     column=4, row=3, sticky=E, padx=4, pady=2)
            ttk.Entry(miscframe, textvariable=self.door_thickness,
                      width=6).grid(column=2, row=3, padx=6, pady=2)

            self.legs_thicker_btm_lbl = ttk.Label(
                miscframe, text='Mounting legs requires bottoms thicker than\n'
                                '3/4" so that leg mounting screws will grab.'
            )
            self.legs_thicker_btm_lbl.state(['disabled'])
            self.legs_thicker_btm_lbl.grid(
                column=3, columnspan=3, row=7, rowspan=2, sticky=(N,W),
                padx=(8, 4), pady=2
            )

            legs_chk = ttk.Checkbutton(
                miscframe, text='Mount legs on cabinets.',
                variable=self.legs, command=self.legs_changed,
                onvalue='yes', offvalue='no'
            ).grid(column=0, columnspan=3, row=6, sticky=W,
                   padx=2, pady=(15, 2))

            self.bottoms_lbl = ttk.Label(miscframe, text='Bottoms:')
            self.bottoms_lbl.state(['disabled'])
            self.bottoms_lbl.grid(
                column=0, row=9, sticky=W, padx=2, pady=(6, 2)
            )
            self.btm_material_lbl = ttk.Label(
                miscframe, textvariable=self.btm_material,
                width=max(map(len, materials)) - 2
            )
            self.btm_material_lbl.grid(column=1, row=9, sticky=W, padx=2, pady=(6, 2))
            self.bottom_thickness_ent = ttk.Entry(
                miscframe, textvariable=self.bottom_thickness, width=6
            )
            self.bottom_thickness_ent.state(['disabled'])
            self.bottom_thickness_ent.grid(column=2, row=9, padx=6, pady=(6, 2))

            self.stacked_btm_chk = ttk.Checkbutton(
                miscframe, text='Stack bottom panels:', variable=self.stacked_btm,
                command=self.stacked_btm_changed,
                onvalue='yes', offvalue='no')
            self.stacked_btm_chk.state(['disabled'])
            self.stacked_btm_chk.grid(column=0, columnspan=2, row=7, sticky=W,
                                      padx=(25, 2), pady=2)

#            ttk.Label(miscframe, text='Upper panel:').grid(
#                column=1, row=7, sticky=W, padx=(10, 2), pady=2)
            self.btmpanel1_thickness_ent = ttk.Entry(
                miscframe, textvariable=self.btmpanel1_thickness, width=6
            )
            self.btmpanel1_thickness_ent.state(['disabled'])
            self.btmpanel1_thickness_ent.grid(column=2, row=7, padx=6, pady=2)

#            ttk.Label(miscframe, text='Lower panel:').grid(
#                column=1, row=8, sticky=W, padx=(10, 2), pady=2)
            self.btmpanel2_thickness_ent = ttk.Entry(
                miscframe, textvariable=self.btmpanel2_thickness, width=6
            )
            self.btmpanel2_thickness_ent.state(['disabled'])
            self.btmpanel2_thickness_ent.grid(column=2, row=8, padx=6, pady=2)

            ttk.Label(miscframe, text='Doors per Cabinet:').grid(
                column=0, columnspan=2, row=10, sticky=W, padx=(0, 6), pady=(15, 2))
            drs_per_cab_rb1 = ttk.Radiobutton(
                miscframe, value=1, text='1', variable=self.doors_per_cab
            )
            # Do not allow selection of one door per cabinet. This can only be
            # enabled after major code changes throughout, to allow for upper
            # cabinet banks, variable height/width cabinets, etc.
            drs_per_cab_rb1.state(['disabled'])
            drs_per_cab_rb1.grid(column=2, row=10, sticky=W, padx=3, pady=(15, 2))
            ttk.Radiobutton(miscframe, value=2, text='2',
                variable=self.doors_per_cab).grid(
                    column=3, row=10, sticky=W, padx=3, pady=(15, 2))

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
        # self.output_lbl = ttk.Label(outpframe, textvariable=self.output,
        #                             font='TkFixedFont')
        # self.output_lbl.grid(column=0, row=0, sticky=(N, S, E, W), pady=(0, 50))
        outpframe.columnconfigure(0, weight=1)
        outpframe.columnconfigure(1, weight=0)
        outpframe.rowconfigure(0, weight=1)
        self.output_txt = Text(outpframe, height=3, relief='flat',
                               background='gray85', font='TkFixedFont')
        self.output_sb = ttk.Scrollbar(outpframe, orient='vertical',
                                       command=self.output_txt.yview)
        self.output_txt.configure(yscrollcommand=self.output_sb.set)
        self.output_txt.grid(column=0, row=0, sticky=(N, S, W, E))
        self.output_sb.grid(column=1, row=0, sticky=(N, S, E))
        self.output_txt.insert('end', self.output)
        self.output_txt.configure(state='disabled')

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

    def prim_material_changed(self, e):
        self.prim_thickness.set(matl_thicknesses[self.prim_material.get()][0])
        self.prim_material_cbx.selection_clear()
        if self.legs.get() == 'yes':
            self.btm_material.set(self.prim_material.get())
            btm_thicknesses = matl_thicknesses[self.prim_material.get()][1]
            self.bottom_thickness.set(sum(btm_thicknesses))
            if len(btm_thicknesses) > 1:
                self.stacked_btm.set('yes')
                self.btmpanel1_thickness.set(btm_thicknesses[0])
                self.btmpanel1_thickness_ent.state(['!disabled'])
                self.btmpanel2_thickness.set(btm_thicknesses[1])
                self.btmpanel2_thickness_ent.state(['!disabled'])
                self.bottom_thickness_ent.state(['disabled'])
            else:
                self.stacked_btm.set('no')
                self.btmpanel1_thickness.set('')
                self.btmpanel1_thickness_ent.state(['disabled'])
                self.btmpanel2_thickness.set('')
                self.btmpanel2_thickness_ent.state(['disabled'])
                self.bottom_thickness_ent.state(['!disabled'])

    def door_material_changed(self, e):
        self.door_thickness.set(matl_thicknesses[self.door_material.get()][0])
        self.door_material_cbx.selection_clear()

    def legs_changed(self):
        if self.legs.get() == 'yes':
            self.legs_thicker_btm_lbl.state(['!disabled'])
            self.bottoms_lbl.state(['!disabled'])
            self.btm_material.set(self.prim_material.get())
            btm_thicknesses = matl_thicknesses[self.prim_material.get()][1]
            self.bottom_thickness.set(sum(btm_thicknesses))
            self.bottom_thickness_ent.state(['!disabled'])
            self.stacked_btm.set('no')
            self.stacked_btm_chk.state(['!disabled'])
            if len(btm_thicknesses) > 1:
                self.stacked_btm.set('yes')
                self.btmpanel1_thickness.set(btm_thicknesses[0])
                self.btmpanel1_thickness_ent.state(['!disabled'])
                self.btmpanel2_thickness.set(btm_thicknesses[1])
                self.btmpanel2_thickness_ent.state(['!disabled'])
                self.bottom_thickness_ent.state(['disabled'])
        else:
            self.legs_thicker_btm_lbl.state(['disabled'])
            self.bottoms_lbl.state(['disabled'])
            self.btm_material.set('')
            self.bottom_thickness.set('')
            self.bottom_thickness_ent.state(['disabled'])
            self.btmpanel1_thickness.set('')
            self.btmpanel1_thickness_ent.state(['disabled'])
            self.btmpanel2_thickness.set('')
            self.btmpanel2_thickness_ent.state(['disabled'])
            self.stacked_btm.set('no')
            self.stacked_btm_chk.state(['disabled'])

    def stacked_btm_changed(self):
        if self.stacked_btm.get() == 'yes':
            half_btm = float(self.bottom_thickness.get()) / 2
            self.btmpanel1_thickness_ent.state(['!disabled'])
            self.btmpanel1_thickness.set(half_btm)
            self.btmpanel2_thickness_ent.state(['!disabled'])
            self.btmpanel2_thickness.set(half_btm)
            self.bottom_thickness_ent.state(['disabled'])
        else:
            self.btmpanel1_thickness.set('')
            self.btmpanel1_thickness_ent.state(['disabled'])
            self.btmpanel2_thickness.set('')
            self.btmpanel2_thickness_ent.state(['disabled'])
            self.bottom_thickness_ent.state(['!disabled'])

    def btmpnl_thickness_changed(self, *args):
        if self.stacked_btm.get() == 'yes':
            if self.btmpanel1_thickness.get() == '':
                bp1 = 0.0
            else:
                bp1 = float(self.btmpanel1_thickness.get())
            if self.btmpanel2_thickness.get() == '':
                bp2 = 0.0
            else:
                bp2 = float(self.btmpanel2_thickness.get())
            new_thickness = bp1 + bp2
            if new_thickness == 0.0:
                thickness_str = ''
            else:
                thickness_str = str(new_thickness)
            self.bottom_thickness.set(thickness_str)

    def quit(self):
        # Destroying the app's top-level window quits the app.
        self.root.destroy()

    def clear_input(self):
        self.initialize_vars()
        self.legs_thicker_btm_lbl.state(['disabled'])
        self.bottoms_lbl.state(['disabled'])
        self.bottom_thickness_ent.state(['disabled'])
        self.btmpanel1_thickness_ent.state(['disabled'])
        self.btmpanel2_thickness_ent.state(['disabled'])
        self.stacked_btm_chk.state(['disabled'])
        self.calc_button.state(['disabled'])
        self.cutlist_button.state(['disabled'])
        self.panel_layout_btn.state(['disabled'])
        self.output_txt.configure(state='normal', height=3)
        self.output_txt.delete('1.0', 'end')
        self.output_txt.insert('end', self.output)
        self.output_txt.configure(state='disabled')

    def calculate_job(self):
        if self.legs.get() == 'no':
            bp_list = [float(self.prim_thickness.get())]
        else:
            if self.stacked_btm.get() == 'yes':
                bp1 = float(self.btmpanel1_thickness.get())
                bp2 = float(self.btmpanel2_thickness.get())
                bp_list = [bp1, bp2]
            else:
                bt = float(self.bottom_thickness.get())
                bp_list = [bt]
        cab_run = Run(float(self.fullwidth.get()),
                      float(self.height.get()),
                      float(self.depth.get()),
                      fillers=Ends.from_string(self.fillers.get()),
                      prim_material=self.prim_material.get(),
                      prim_thickness=float(self.prim_thickness.get()),
                      door_material=self.door_material.get(),
                      door_thickness=float(self.door_thickness.get()),
                      btmpanel_thicknesses=bp_list,
                      has_legs=yn_to_bool(self.legs.get()))
        if self.description.get() != '':
            self.job = job.Job(self.jobname.get(), cab_run,
                               self.description.get())
        else:
            self.job = job.Job(self.jobname.get(), cab_run)
        # Display the computed job specification, ensuring output lines are no
        # longer than 65 chars.
        self.output = ''
        for line in self.job.specification:
            self.output += textwrap.fill(line, width=65) + '\n'
        lines = self.output.count('\n') + 1
        self.output_txt.configure(state='normal')
        self.output_txt.delete('1.0', 'end')
        self.output_txt.insert('end', self.output)
        self.output_txt.configure(state='disabled', height=lines + 1)
        # self.output_txt.grid_configure(pady=0)
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
