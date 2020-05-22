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


"""First Cabinet Wiz GUI module.

This module implements the proof-of-concept GUI for Cabinet Wiz, implemented
in Tk using the Python Tkinter module.
"""


# __all__ = [max_cabinet_width, door_hinge_gap, cabinet_run, num_cabinets,
#            Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'


import textwrap
import tkinter as tk
from tkinter import N, S, W, E
from tkinter import ttk
from tkinter import filedialog

from app.cabinet import (
    materials, matl_thicknesses, prim_mat_default, door_mat_default, Ends, Run,
    ctop_ovrhang_l_default, ctop_ovrhang_r_default, ctop_ovrhang_f_default,
    ctop_thickness_default, toekick_ht_default)
import app.job as job
import app.cutlist as cutlist


# Global module constants

_no_job_message = 'No job yet.'


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
            self.root = tk.Tk()
        else:
            # Our master will be what was passed in as `root'
            self.root = root
        super().__init__(self.root, padding=5)
        # Instance variables
        self.root.title(title)
        self.jobname = tk.StringVar()
        self.description = tk.StringVar()
        self.dimension_base = tk.StringVar()
        self.fullwidth = tk.StringVar()
        self.height = tk.StringVar()
        self.depth = tk.StringVar()
        self.ctop_ovrhang_l = tk.StringVar()
        self.ctop_ovrhang_f = tk.StringVar()
        self.ctop_ovrhang_r = tk.StringVar()
        self.ctop_thickness = tk.StringVar()
        self.fillers = tk.StringVar()
        self.prim_material = tk.StringVar()
        self.prim_thickness = tk.StringVar()
        self.door_material = tk.StringVar()
        self.door_thickness = tk.StringVar()
        self.toekick_style = tk.StringVar()
        self.toekick_ht = tk.StringVar()
        self.stacked_btm = tk.StringVar()
        self.bottom_thickness = tk.StringVar()
        self.btmpanel1_thickness = tk.StringVar()
        self.btmpanel2_thickness = tk.StringVar()
        self.btm_material = tk.StringVar()
        self.doors_per_cab = tk.IntVar()
        self.output = ''
        self.job = None
        self.initialize_vars()
        self.make_widgets()
        self.reset_widgets()

    def initialize_vars(self):
        self.jobname.set('')
        self.description.set('')
        self.dimension_base.set('countertop')
        self.fullwidth.set('')
        self.height.set('')
        self.depth.set('')
        self.ctop_ovrhang_l.set(str(ctop_ovrhang_l_default))
        self.ctop_ovrhang_f.set(str(ctop_ovrhang_f_default))
        self.ctop_ovrhang_r.set(str(ctop_ovrhang_r_default))
        self.ctop_thickness.set(str(ctop_thickness_default))
        self.fillers.set('neither')
        self.prim_material.set(materials[prim_mat_default])
        self.prim_thickness.set(matl_thicknesses[self.prim_material.get()][0])
        self.door_material.set(materials[door_mat_default])
        self.door_thickness.set(matl_thicknesses[self.door_material.get()][0])
        self.toekick_style.set('box_frame')
        self.toekick_ht.set(str(toekick_ht_default))
        self.stacked_btm.set('no')
        self.bottom_thickness.set('')
        self.btmpanel1_thickness.set('')
        self.btmpanel1_thickness.trace('w', self.btmpnl_thickness_changed)
        self.btmpanel2_thickness.set('')
        self.btmpanel2_thickness.trace('w', self.btmpnl_thickness_changed)
        self.btm_material.set('')
        self.doors_per_cab.set(2)
        self.output = _no_job_message
        self.job = None

    def make_widgets(self):
        """Create and layout all the UI elements.

        Only the widgets that need to be refered to in other parts of the code
        are made as instance variables (with `self.').
        """
        ttk.Label(self, text='The Custom Euro-Style Cabinet Configurator'
                  ).grid(column=0, row=0, sticky=W)
        inputframe = ttk.Labelframe(
            self, text='Parameters: ', borderwidth=2, relief='groove',
            padding=5)
        inputframe.grid(column=0, row=1, sticky=(N, S, W, E), pady=10)
        ttk.Label(self, text='Job Specification:').grid(
            column=0, row=2, sticky=W, pady=2)
        outputframe = ttk.Frame(self, borderwidth=1, relief='sunken')
        outputframe.grid(column=0, row=3, sticky=(N, S, W, E))
        outp_btnsframe = ttk.Frame(self, padding=(0, 10))
        outp_btnsframe.grid(column=0, row=4, sticky=(N, S, W, E))
        self.grid(column=0, row=0, sticky=(N, S, W, E))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.fill_inputframe(inputframe)
        self.fill_outputframe(outputframe)
        self.fill_outp_btnsframe(outp_btnsframe)

    def reset_widgets(self):
        """Reset all UI elements to their proper states for input of a new job.

        This is where we enable/disable widgets and set their initial values,
        so that we can use this function in multiple places, in particular,
        at initial program start AND when the `Clear' button is pressed.
        """
        self.dimbase_changed()
        self.toekick_changed()
        self.calc_button.state(['disabled'])
        self.update_output_txt()
        self.cutlist_button.state(['disabled'])
        self.panel_layout_btn.state(['disabled'])

    def update_output_txt(self):
        """Update output area to display current value of self.output.

        At program start, and after the Clear button is pressed, the output
        will be _no_job_message, since no job output has been computed. In this
        case we set the output text area to be 3 lines high. Otherwise, set the
        height to match the output contents.
        """
        if self.output == _no_job_message:
            lines = 3
        else:
            lines = self.output.count('\n') + 2
        self.output_txt.configure(state='normal')
        self.output_txt.delete('1.0', 'end')
        self.output_txt.insert('end', self.output)
        self.output_txt.configure(state='disabled', height=lines)

    def make_jobframe(self, inpframe, vcmd):
        jobframe = ttk.Frame(inpframe, padding=(0, 5, 0, 10))
        jobframe.grid(column=0, row=0, sticky=(N, S, W, E))
        jobframe.columnconfigure(0, weight=0)
        jobframe.columnconfigure(1, weight=1)
        ttk.Label(jobframe, text='Job Name:').grid(
            column=0, row=0, pady=2, sticky=W)
        self.jobname_ent = ttk.Entry(
            jobframe, textvariable=self.jobname,
            validate='all', validatecommand=(vcmd, '%P'))
        ttk.Label(jobframe, text='Description:').grid(
            column=0, row=1, pady=2, sticky=W)
        self.descrip_ent = ttk.Entry(
            jobframe, textvariable=self.description, validate='all',
            validatecommand=(vcmd, '%P'))
        self.jobname_ent.grid(column=1, row=0, pady=2, sticky=(W, E),
                              padx=(5, 0))
        self.descrip_ent.grid(column=1, row=1, pady=2, sticky=(W, E),
                              padx=(5, 0))
        self.jobname_ent.focus_set()

    def make_dimbase_frame(self, inpframe):
        dimbase_frame = ttk.Frame(inpframe, padding=(0, 10))
        dimbase_frame.grid(column=0, row=1, sticky=(N, S, W, E))
        dimbase_frame.columnconfigure(0, weight=0)
        dimbase_frame.columnconfigure(1, weight=0)
        dimbase_frame.columnconfigure(2, weight=1)
        ttk.Label(dimbase_frame, text='Base measurement calculations on:'
                  ).grid(column=0, row=0, sticky=W, padx=(0, 15), pady=2)
        ttk.Radiobutton(
            dimbase_frame, value='countertop', text='Countertop',
            variable=self.dimension_base, command=self.dimbase_changed
            ).grid(column=1, row=0, sticky=W, padx=(5, 20), pady=2)
        ttk.Radiobutton(
            dimbase_frame, value='cab_bank', text='Cabinet bank',
            variable=self.dimension_base, command=self.dimbase_changed
            ).grid(column=2, row=0, sticky=W, padx=5, pady=2)

    def make_dimframe(self, inpframe, vcmd):
        dimframe = ttk.Frame(inpframe, padding=(0, 10))
        dimframe.grid(column=0, row=2, sticky=(N, S, W, E))
        dimframe.columnconfigure(0, weight=0)
        dimframe.columnconfigure(1, weight=1)
        dimframe.columnconfigure(2, weight=0)
        dimframe.columnconfigure(3, weight=1)
        dimframe.columnconfigure(4, weight=0)
        dimframe.columnconfigure(5, weight=1)
        ttk.Label(dimframe, text='Width:').grid(
            column=0, row=0, sticky=W, padx=(0, 3))
        self.fullwidth_ent = ttk.Entry(
            dimframe, textvariable=self.fullwidth, width=12, validate='all',
            validatecommand=(vcmd, '%P'))
        ttk.Label(dimframe, text='Height:').grid(
            column=2, row=0, sticky=E, padx=(6, 3))
        self.height_ent = ttk.Entry(
            dimframe, textvariable=self.height, width=12, validate='all',
            validatecommand=(vcmd, '%P'))
        ttk.Label(dimframe, text='Depth:').grid(
            column=4, row=0, sticky=E, padx=(6, 3))
        self.depth_ent = ttk.Entry(
            dimframe, textvariable=self.depth, width=12, validate='all',
            validatecommand=(vcmd, '%P'))
        self.fullwidth_ent.grid(column=1, row=0, sticky=(W), padx=(3, 40))
        self.height_ent.grid(column=3, row=0, sticky=(W), padx=(3, 40))
        self.depth_ent.grid(column=5, row=0, sticky=(W), padx=(3, 10))

    def make_countertop_frame(self, inpframe, vcmd):
        countertop_frame = ttk.Frame(inpframe, padding=(0, 10))
        countertop_frame.grid(column=0, row=3, sticky=(N, S, W, E))
        countertop_frame.columnconfigure(0, weight=1)
        # Countertop overhang frame
        ctop_ovrhang_frame = ttk.Frame(countertop_frame, padding=(0, 5))
        ctop_ovrhang_frame.grid(column=0, row=0, sticky=(N, S, W, E))
        ctop_ovrhang_frame.columnconfigure(0, weight=0)
        ctop_ovrhang_frame.columnconfigure(1, weight=0)
        ctop_ovrhang_frame.columnconfigure(2, weight=1)
        ctop_ovrhang_frame.columnconfigure(3, weight=0)
        ctop_ovrhang_frame.columnconfigure(4, weight=1)
        ctop_ovrhang_frame.columnconfigure(5, weight=0)
        ctop_ovrhang_frame.columnconfigure(6, weight=1)
        self.ctop_ovrhang_lbl = ttk.Label(
            ctop_ovrhang_frame, text='Countertop Overhang:')
        self.ctop_ovrhang_lbl.grid(
            column=0, row=0, sticky=W, padx=(0, 15))
        self.ctop_ovrhang_left_lbl = ttk.Label(
            ctop_ovrhang_frame, text='Left:')
        self.ctop_ovrhang_left_lbl.grid(
            column=1, row=0, sticky=E, padx=(6, 3))
        self.ctop_ovrhang_left_ent = ttk.Entry(
            ctop_ovrhang_frame, width=8, textvariable=self.ctop_ovrhang_l,
            validate='all', validatecommand=(vcmd, '%P'))
        self.ctop_ovrhang_left_ent.grid(
            column=2, row=0, sticky=(W), padx=(3, 20))
        self.ctop_ovrhang_front_lbl = ttk.Label(
            ctop_ovrhang_frame, text='Front:')
        self.ctop_ovrhang_front_lbl.grid(
            column=3, row=0, sticky=E, padx=(6, 3))
        self.ctop_ovrhang_front_ent = ttk.Entry(
            ctop_ovrhang_frame, width=8, textvariable=self.ctop_ovrhang_f,
            validate='all', validatecommand=(vcmd, '%P'))
        self.ctop_ovrhang_front_ent.grid(
            column=4, row=0, sticky=(W), padx=(3, 20))
        self.ctop_ovrhang_right_lbl = ttk.Label(
            ctop_ovrhang_frame, text='Right:')
        self.ctop_ovrhang_right_lbl.grid(
            column=5, row=0, sticky=E, padx=(6, 3))
        self.ctop_ovrhang_right_ent = ttk.Entry(
            ctop_ovrhang_frame, width=8, textvariable=self.ctop_ovrhang_r,
            validate='all', validatecommand=(vcmd, '%P'))
        self.ctop_ovrhang_right_ent.grid(
            column=6, row=0, sticky=(W), padx=(3, 10))
        # Countertop thickness frame
        ctop_thickness_frame = ttk.Frame(countertop_frame, padding=(0, 5))
        ctop_thickness_frame.grid(column=0, row=1, sticky=(N, S, W, E))
        ctop_thickness_frame.columnconfigure(0, weight=0)
        ctop_thickness_frame.columnconfigure(1, weight=1)
        self.ctop_thickness_lbl = ttk.Label(
            ctop_thickness_frame, text='Countertop Thickness:')
        self.ctop_thickness_lbl.grid(
            column=0, row=0, sticky=W, padx=(0, 15))
        self.ctop_thickness_ent = ttk.Entry(
            ctop_thickness_frame, width=7, textvariable=self.ctop_thickness,
            validate='all', validatecommand=(vcmd, '%P'))
        self.ctop_thickness_ent.grid(column=1, row=0, sticky=W, padx=3)

    def make_filler_frame(self, inpframe):
        filler_frame = ttk.Frame(inpframe, padding=(0, 5))
        filler_frame.grid(column=0, row=4, sticky=(N, S, W, E))
        filler_frame.columnconfigure(0, weight=0)
        filler_frame.columnconfigure(1, weight=0)
        filler_frame.columnconfigure(2, weight=0)
        filler_frame.columnconfigure(3, weight=0)
        filler_frame.columnconfigure(4, weight=1)
        ttk.Label(filler_frame, text='Fillers for which ends?').grid(
            column=0, row=0, sticky=W, padx=(0, 15), pady=2)
        ttk.Radiobutton(filler_frame, value='neither', text='Neither',
                        variable=self.fillers).grid(
                        column=1, row=0, sticky=W, padx=(5, 20), pady=2)
        ttk.Radiobutton(filler_frame, value='left', text='Left',
                        variable=self.fillers).grid(
                        column=2, row=0, sticky=W, padx=(5, 20), pady=2)
        ttk.Radiobutton(filler_frame, value='right', text='Right',
                        variable=self.fillers).grid(
                        column=3, row=0, sticky=W, padx=(5, 20), pady=2)
        ttk.Radiobutton(filler_frame, value='both', text='Both',
                        variable=self.fillers).grid(
                        column=4, row=0, sticky=W, padx=5, pady=2)

    def make_materials_frame(self, inpframe):
        matls_frame = ttk.Frame(inpframe, padding=(0, 5))
        matls_frame.grid(column=0, row=5, sticky=(N, S, W, E))
        matls_frame.columnconfigure(0, weight=0)
        matls_frame.columnconfigure(1, weight=0)
        matls_frame.columnconfigure(2, weight=0)
        matls_frame.columnconfigure(3, weight=0)
        ttk.Label(matls_frame, text='Material:').grid(
            column=1, row=0, sticky=(N, W), padx=4, pady=(15, 2))
        ttk.Label(matls_frame, text='Thickness:').grid(
            column=2, row=0, sticky=W, padx=4, pady=(15, 2))
        ttk.Label(matls_frame,
                  text=('Measure actual material thickness to the\n'
                        'nearest 0.01" and adjust values accordingly.')).grid(
            column=3, row=1, rowspan=2, sticky=(N, W), padx=(8, 4), pady=2)
        ttk.Label(matls_frame, text='Primary:').grid(
            column=0, row=1, sticky=W, padx=(0, 2), pady=2)
        self.prim_material_cbx = ttk.Combobox(
            matls_frame, textvariable=self.prim_material,
            width=max(map(len, materials)) - 2)
        self.prim_material_cbx['values'] = materials
        # Prevent direct editing of the value in the combobox:
        self.prim_material_cbx.state(['readonly'])
        # Call the `selection clear' method when the value changes. It looks
        # a bit odd visually without doing that.
        self.prim_material_cbx.bind(
            '<<ComboboxSelected>>', self.prim_material_changed)
        self.prim_material_cbx.grid(
            column=1, row=1, sticky=W, padx=(6, 3), pady=2)
        ttk.Entry(matls_frame, textvariable=self.prim_thickness,
                  width=6).grid(column=2, row=1, padx=6, pady=2)

        ttk.Label(matls_frame, text='Doors:').grid(
            column=0, row=2, sticky=W, padx=(0, 2), pady=2)
        self.door_material_cbx = ttk.Combobox(
            matls_frame, textvariable=self.door_material,
            width=max(map(len, materials)) - 2)
        self.door_material_cbx['values'] = materials
        # Prevent direct editing of the value in the combobox:
        self.door_material_cbx.state(['readonly'])
        # Call the `selection clear' method when the value changes. It looks
        # a bit odd visually without doing that.
        self.door_material_cbx.bind(
            '<<ComboboxSelected>>', self.door_material_changed)
        self.door_material_cbx.grid(
            column=1, row=2, sticky=W, padx=(6, 3), pady=2)
        ttk.Entry(matls_frame, textvariable=self.door_thickness,
                  width=6).grid(column=2, row=2, padx=6, pady=2)

    def make_toekick_frame(self, inpframe, vcmd):
        toekick_frame = ttk.Frame(inpframe, padding=(0, 10))
        toekick_frame.grid(column=0, row=6, sticky=(N, S, W, E))
        # Toekick style frame
        toekick_style_frame = ttk.Frame(toekick_frame, padding=(0, 5))
        toekick_style_frame.grid(column=0, row=0, sticky=(N, S, W, E))
        toekick_style_frame.columnconfigure(0, weight=0)
        toekick_style_frame.columnconfigure(1, weight=0)
        toekick_style_frame.columnconfigure(2, weight=1)
        ttk.Label(toekick_style_frame, text='Toekick style:').grid(
            column=0, row=0, sticky=W, padx=(0, 15), pady=2)
        ttk.Radiobutton(
            toekick_style_frame, value='box_frame', text='Plywood box frame',
            variable=self.toekick_style, command=self.toekick_changed).grid(
            column=1, row=0, sticky=W, padx=(5, 20), pady=2)
        ttk.Radiobutton(
            toekick_style_frame, value='steel_legs',
            text='Stainless steel legs with clip-on toe kicks',
            variable=self.toekick_style, command=self.toekick_changed).grid(
            column=2, row=0, sticky=W, padx=5, pady=2)
        # Toekick height frame
        toekick_height_frame = ttk.Frame(toekick_frame, padding=(0, 5))
        toekick_height_frame.grid(column=0, row=1, sticky=(N, S, W, E))
        toekick_height_frame.columnconfigure(0, weight=0)
        toekick_height_frame.columnconfigure(1, weight=1)
        ttk.Label(toekick_height_frame, text='Toekick height:').grid(
            column=0, row=0, sticky=W, padx=(0, 15))
        self.toekick_ht_ent = ttk.Entry(
            toekick_height_frame, width=6, textvariable=self.toekick_ht,
            validate='all', validatecommand=(vcmd, '%P'))
        self.toekick_ht_ent.grid(column=1, row=0, sticky=W, padx=3)

    def make_btmpanels_frame(self, inpframe):
        btmpanels_frame = ttk.Frame(inpframe, padding=(0, 10))
        btmpanels_frame.grid(column=0, row=7, sticky=(N, S, W, E))
        btmpanels_frame.columnconfigure(0, weight=1)
        btmpanels_frame.columnconfigure(1, weight=1)
        btmpanels_frame.columnconfigure(2, weight=1)
        btmpanels_frame.columnconfigure(3, weight=1)
        self.stacked_btm_chk = ttk.Checkbutton(
            btmpanels_frame, text='Stacked bottom panels:',
            variable=self.stacked_btm, command=self.stacked_btm_changed,
            onvalue='yes', offvalue='no')
        self.stacked_btm_chk.state(['disabled'])
        self.stacked_btm_chk.grid(column=0, columnspan=2, row=0,
                                  sticky=W, padx=(2, 2), pady=2)

        self.btmpanel1_thickness_ent = ttk.Entry(
            btmpanels_frame, textvariable=self.btmpanel1_thickness, width=6)
        self.btmpanel1_thickness_ent.state(['disabled'])
        self.btmpanel1_thickness_ent.grid(column=2, row=0, padx=6, pady=2)
        self.btmpanel2_thickness_ent = ttk.Entry(
            btmpanels_frame, textvariable=self.btmpanel2_thickness, width=6)
        self.btmpanel2_thickness_ent.state(['disabled'])
        self.btmpanel2_thickness_ent.grid(column=2, row=1, padx=6, pady=2)
        self.legs_thicker_btm_lbl = ttk.Label(
            btmpanels_frame, text='Mounting legs requires bottoms thicker '
            'than\n3/4" so that leg mounting screws will grab.')
        self.legs_thicker_btm_lbl.state(['disabled'])
        self.legs_thicker_btm_lbl.grid(
            column=3, row=0, rowspan=2, sticky=(N, W), padx=(8, 4), pady=2)
        self.bottoms_lbl = ttk.Label(btmpanels_frame, text='Bottoms:')
        self.bottoms_lbl.state(['disabled'])
        self.bottoms_lbl.grid(column=0, row=2, sticky=W, padx=2, pady=(6, 2))
        self.btm_material_lbl = ttk.Label(
            btmpanels_frame, textvariable=self.btm_material,
            width=max(map(len, materials)) - 2)
        self.btm_material_lbl.grid(
            column=1, row=2, sticky=W, padx=2, pady=(6, 2))
        self.bottom_thickness_ent = ttk.Entry(
            btmpanels_frame, textvariable=self.bottom_thickness, width=6)
        self.bottom_thickness_ent.state(['disabled'])
        self.bottom_thickness_ent.grid(column=2, row=2, padx=6, pady=(6, 2))

    # At this point, we only support cabinets with two doors each. Changing
    # things to allow for cabinets with one door will entail major refactoring
    # throughout the codebase, including upper cabinet banks, varying cabinet
    # heights and widths in the same bank, etc.

    def make_doors_per_cab_frame(self, inpframe):
        doors_per_cab_frame = ttk.Frame(inpframe, padding=(0, 10))
        doors_per_cab_frame.grid(column=0, row=8, sticky=(N, S, W, E))
        doors_per_cab_frame.columnconfigure(0, weight=0)
        doors_per_cab_frame.columnconfigure(1, weight=1)
        ttk.Label(doors_per_cab_frame, text='Doors per Cabinet:').grid(
            column=0, row=0, sticky=W, padx=(0, 15), pady=(15, 2))
        ttk.Label(doors_per_cab_frame, text='2').grid(
            column=1, row=0, sticky=W, padx=0, pady=(15, 2))
        # ttk.Radiobutton(doors_per_cab_frame, value=1, text='1',
        #     variable=self.doors_per_cab).grid(
        #     column=1, row=0, sticky=W, padx=3, pady=(15, 2))
        # ttk.Radiobutton(doors_per_cab_frame, value=2, text='2',
        #     variable=self.doors_per_cab).grid(
        #     column=2, row=0, sticky=W, padx=3, pady=(15, 2))

    def make_buttonframe(self, inpframe):
        buttonframe = ttk.Frame(inpframe, padding=(0, 12, 0, 0))
        buttonframe.grid(column=0, row=9, sticky=(N, S, W, E))
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.columnconfigure(2, weight=1)
        buttonframe.rowconfigure(0, weight=1)
        self.calc_button = ttk.Button(
            buttonframe, text='Calculate', command=self.calculate_job)
        self.calc_button.state(['disabled'])
        clear_button = ttk.Button(
            buttonframe, text='Clear', command=self.clear_input)
        quit_button = ttk.Button(
            buttonframe, text='Quit', command=self.quit)
        self.calc_button.grid(column=0, row=0, sticky=E, padx=2)
        clear_button.grid(column=1, row=0, sticky=W, padx=2)
        quit_button.grid(column=2, row=0, padx=2)

    def fill_inputframe(self, inpframe):
        # Register our validate function to get its function ID. This is used
        # to disable the `Calculate' button if the fields necessary for
        # calculation are not filled in.
        vcmd = self.root.register(self.validate_entry)
        self.make_jobframe(inpframe, vcmd)
        self.make_dimbase_frame(inpframe)
        self.make_dimframe(inpframe, vcmd)
        self.make_countertop_frame(inpframe, vcmd)
        self.make_filler_frame(inpframe)
        self.make_materials_frame(inpframe)
        self.make_toekick_frame(inpframe, vcmd)
        self.make_btmpanels_frame(inpframe)
        self.make_doors_per_cab_frame(inpframe)
        self.make_buttonframe(inpframe)
        inpframe.columnconfigure(0, weight=1)

    def fill_outputframe(self, outpframe):
        outpframe.columnconfigure(0, weight=1)
        outpframe.columnconfigure(1, weight=0)
        outpframe.rowconfigure(0, weight=1)
        self.output_txt = tk.Text(
            outpframe, height=3, relief='flat', background='gray85',
            font='TkFixedFont')
        self.output_sb = ttk.Scrollbar(
            outpframe, orient='vertical', command=self.output_txt.yview)
        self.output_txt.configure(yscrollcommand=self.output_sb.set)
        self.output_txt.grid(column=0, row=0, sticky=(N, S, W, E))
        self.output_sb.grid(column=1, row=0, sticky=(N, S, E))

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
                  and self.depth_ent.get() != ''
                  and self.toekick_ht.get() != '')
        if self.dimension_base.get() == 'countertop':
            result = result and (
                self.ctop_ovrhang_left_ent.get() != ''
                and self.ctop_ovrhang_front_ent.get() != ''
                and self.ctop_ovrhang_right_ent.get() != ''
                and self.ctop_thickness_ent.get() != '')
        return result

    def prim_material_changed(self, e):
        self.prim_thickness.set(matl_thicknesses[self.prim_material.get()][0])
        self.prim_material_cbx.selection_clear()
        if self.toekick_style.get() == 'steel_legs':
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

    def dimbase_changed(self):
        if self.dimension_base.get() == 'countertop':
            self.ctop_ovrhang_lbl.state(['!disabled'])
            self.ctop_ovrhang_left_lbl.state(['!disabled'])
            self.ctop_ovrhang_l.set(str(ctop_ovrhang_l_default))
            self.ctop_ovrhang_left_ent.state(['!disabled'])
            self.ctop_ovrhang_front_lbl.state(['!disabled'])
            self.ctop_ovrhang_f.set(str(ctop_ovrhang_f_default))
            self.ctop_ovrhang_front_ent.state(['!disabled'])
            self.ctop_ovrhang_right_lbl.state(['!disabled'])
            self.ctop_ovrhang_r.set(str(ctop_ovrhang_r_default))
            self.ctop_ovrhang_right_ent.state(['!disabled'])
            self.ctop_thickness_lbl.state(['!disabled'])
            self.ctop_thickness.set(str(ctop_thickness_default))
            self.ctop_thickness_ent.state(['!disabled'])
        else:
            self.ctop_ovrhang_lbl.state(['disabled'])
            self.ctop_ovrhang_left_lbl.state(['disabled'])
            self.ctop_ovrhang_l.set('')
            self.ctop_ovrhang_left_ent.state(['disabled'])
            self.ctop_ovrhang_front_lbl.state(['disabled'])
            self.ctop_ovrhang_f.set('')
            self.ctop_ovrhang_front_ent.state(['disabled'])
            self.ctop_ovrhang_right_lbl.state(['disabled'])
            self.ctop_ovrhang_r.set('')
            self.ctop_ovrhang_right_ent.state(['disabled'])
            self.ctop_thickness_lbl.state(['disabled'])
            self.ctop_thickness.set('')
            self.ctop_thickness_ent.state(['disabled'])

    def toekick_changed(self):
        if self.toekick_style.get() == 'steel_legs':
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
        self.reset_widgets()

    def calculate_job(self):
        if self.toekick_style.get() == 'box_frame':
            bp_list = [float(self.prim_thickness.get())]
        else:
            # Steel legs will be mounted.
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
                      toekick_style=self.toekick_style.get()
                      )
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
        self.update_output_txt()
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


# gui.py  ends here
