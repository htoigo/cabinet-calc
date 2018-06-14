# -*- coding: utf-8 -*-

"""
cabinet-calc GUI
~~~~~~~~~~~~~~~~

This module implements the Cabinet-Calc GUI.

:copyright: (c) 2018 by Harry H. Toigo II.
:license: MIT, see LICENSE file for more details.

Display Cabinet-Calc in a tkinter top-level window on the user's desktop.

Where will the output go?
"""

#__all__ = [max_cabinet_width, door_hinge_gap, cabinet_run, num_cabinets, Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'

import tkinter as tk
import tkinter.ttk as ttk


class Application(tk.Frame):
    """A class representing the application (and top-level window)."""
    def __init__(self, master=None, title=None):
        if master is None:
            # Create a new top-level window to be our master
            master = tk.Tk()
            if title is not None:
                master.title(title)
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title_lbl = ttk.Label(self, text='Euro-Style Cabinet Calculator')
        self.title_lbl.pack()
        self.job_name_lbl = ttk.Label(self, text='Job Name:')
        self.job_name_lbl.pack()
        self.job_name_entry = ttk.Entry(self)
        self.job_name_entry.pack()
        # Material
        self.material_mb = ttk.Menubutton(self, text='Plywood')
        self.material_mb.pack()
        self.material_mb.menu = tk.Menu(self.material_mb, tearoff=0)
        self.material_mb['menu'] = self.material_mb.menu
        self.material_mb.menu.add_command(label='Melamine')
        self.material_mb.menu.add_command(label='Granite')
        self.matl_thickness_lbl = ttk.Label(self, text='Thickness:')
        self.matl_thickness_lbl.pack()
        self.matl_thickness_text = tk.StringVar()
        self.matl_thickness_text.set('0.75')
        self.matl_thickness_entry = ttk.Entry(self, textvariable=self.matl_thickness_text)
        self.matl_thickness_entry.pack()
        # Doors
        # The control variable
        self.doors_per_cab = tk.IntVar()
        self.doors_per_cab.set(2)
        self.doors_per_cab_lbl = ttk.Label(self, text='Doors per Cabinet:')
        self.doors_per_cab_lbl.pack()
        self.doors_per_cab_radio1 = ttk.Radiobutton(self, value=1, text='1',
                                                    variable=self.doors_per_cab)
        self.doors_per_cab_radio1.pack()
        self.doors_per_cab_radio2 = ttk.Radiobutton(self, value=2, text='2',
                                                    variable=self.doors_per_cab)
        self.doors_per_cab_radio2.pack()
        # Total Width
        self.total_width_lbl = ttk.Label(self, text='W:')
        self.total_width_lbl.pack()
        self.total_width_entry = ttk.Entry(self)
        self.total_width_entry.pack()
        # Height
        self.height_lbl = ttk.Label(self, text='H:')
        self.height_lbl.pack()
        self.height_entry = ttk.Entry(self)
        self.height_entry.pack()
        # Depth
        self.depth_lbl = ttk.Label(self, text='D:')
        self.depth_lbl.pack()
        self.depth_entry = ttk.Entry(self)
        self.depth_entry.pack()

        # Ttk code:
        # style = ttk.Style()
        # style.configure('BW.TLabel', foreground='black', background='white')
        # self.l3 = ttk.Label(text='Label 3', style='BW.TLabel')
        # self.l3.pack()

    def print_contents(self, event):
        print('Hi. Contents of entry are now ---->', self.contents.get())


# root = tk.Tk()
# app = Application(master=root)
# Using the Wm (window manager) class methods:
# app.master.title('Cabinet Calc')
# app.master.maxsize(200, 100)
# app.mainloop()
