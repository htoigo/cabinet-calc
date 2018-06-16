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

from tkinter import *
from tkinter import ttk


class Application(ttk.Frame):
    """The application, which is a frame within the root window."""
    def __init__(self, root=None, title='Cabinet Calc'):
        if root is None:
            # Create a new root window to be our master
            self.root = Tk()
        else:
            self.root = root
        super().__init__(self.root, padding=(3, 3))
        self.root.title(title)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.title_lbl = ttk.Label(self, text='Euro-Style Cabinet Calculator')
        self.jobname_lbl = ttk.Label(self, text='Job Name:')
        self.jobname_ent = ttk.Entry(self)
        # Material
        self.material = StringVar()
        self.material.set('Plywood')
        self.material_lbl = ttk.Label(self, text='Material:')
        self.material_cbx = ttk.Combobox(self, textvariable=self.material)
        # self.material_cbx.bind('<<ComboboxSelected>>', lambda x: pass)
        self.material_cbx['values'] = ('Plywood', 'Melamine', 'Graphite')

        self.thickness_lbl = ttk.Label(self, text='Thickness:')
        self.thickness = StringVar()
        self.thickness.set('0.75')
        self.thickness_ent = ttk.Entry(self, textvariable=self.thickness)
        # Doors
        self.doors_per_cab = IntVar()
        self.doors_per_cab.set(2)
        self.doors_per_cab_lbl = ttk.Label(self, text='Doors per Cabinet:')
        self.doors_per_cab_rad1 = ttk.Radiobutton(self, value=1, text='1',
                                                  variable=self.doors_per_cab)
        self.doors_per_cab_rad2 = ttk.Radiobutton(self, value=2, text='2',
                                                  variable=self.doors_per_cab)
        self.total_width_lbl = ttk.Label(self, text='Width:')
        self.total_width_ent = ttk.Entry(self)
        self.height_lbl = ttk.Label(self, text='Height:')
        self.height_ent = ttk.Entry(self)
        self.depth_lbl = ttk.Label(self, text='Depth:')
        self.depth_ent = ttk.Entry(self)

        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.title_lbl.grid(column=0, columnspan=6, row=0)
        self.jobname_lbl.grid(column=0, columnspan=2, row=1)
        self.jobname_ent.grid(column=2, columnspan=2, row=1)
        self.material_lbl.grid(column=0, columnspan=2, row=2)
        self.material_cbx.grid(column=2, columnspan=2, row=2)
        self.thickness_lbl.grid(column=4, row=2)
        self.thickness_ent.grid(column=5, row=2)
        self.doors_per_cab_lbl.grid(column=0, columnspan=3, row=3)
        self.doors_per_cab_rad1.grid(column=3, row=3)
        self.doors_per_cab_rad2.grid(column=4, row=3)
        self.total_width_lbl.grid(column=0, row=4)
        self.total_width_ent.grid(column=1, row=4)
        self.height_lbl.grid(column=2, row=4)
        self.height_ent.grid(column=3, row=4)
        self.depth_lbl.grid(column=4, row=4)
        self.depth_ent.grid(column=5, row=4)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(1, weight=1)

        # Ttk code:
        # style = ttk.Style()
        # style.configure('BW.TLabel', foreground='black', background='white')
        # self.l3 = ttk.Label(text='Label 3', style='BW.TLabel')
        # self.l3.pack()


# root = tk.Tk()
# app = Application(master=root)
# Using the Wm (window manager) class methods:
# app.master.title('Cabinet Calc')
# app.master.maxsize(200, 100)
# app.mainloop()
