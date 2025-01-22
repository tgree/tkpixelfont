#!/usr/bin/env python3
import tkinter.font

from .tk.elems import Canvas
from .geom import Vec, Rect


class InfoCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        arial_b12_font = tkinter.font.Font(family='Arial', size=12,
                                           weight='bold')
        arial_b10_font = tkinter.font.Font(family='Arial', size=10,
                                           weight='bold')
        arial_10_font  = tkinter.font.Font(family='Arial', size=10)

        # Generate the font info panel.
        v = Vec(4, 4)
        self.add_text(v, text='FONT INFO', anchor='nw', font=arial_b12_font)
        v += Vec(0, 20)
        self.add_text(v, text='NAME', anchor='nw', font=arial_b10_font)
        v += Vec(0, 12)
        self.fi_name_sv = tkinter.StringVar()
        self.fi_name_entry = self.add_entry(font=arial_10_font, width=40,
                                            textvariable=self.fi_name_sv)
        self.fi_name_entry.configure(highlightthickness=3)
        self.add_window(v.x + 8, v.y, self.fi_name_entry, anchor='nw')
        v += Vec(0, 28)
        self.add_text(v, text='WIDTH', anchor='nw', font=arial_b10_font)
        v += Vec(0, 14)
        self.add_text(v, text='HEIGHT', anchor='nw', font=arial_b10_font)
