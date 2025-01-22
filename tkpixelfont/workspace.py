#!/usr/bin/env python3
from .tk.elems import TKBase

from .document import Document
from .ascii_canvas import ASCIICanvas
from .grid_canvas import GridCanvas


class Workspace(TKBase):
    def __init__(self, x, y, w, h, ascii_w, ascii_h):
        super().__init__()

        self.document = Document()

        self.set_title('tkpixelfont')
        self.set_geometry(x, y, w, h)

        acw = 16 * ascii_w + 4
        ach = 16 * ascii_h + 4
        self.ascii_canvas = self.add_canvas(acw, ach,
                                            ASCIICanvas, ascii_w, ascii_h,
                                            sticky='nws', column=0, row=0)

        gcw = 16 + 16 * 32 + 2
        gch = 16 * 32 + 2
        self.grid_canvas = self.add_canvas(gcw, gch,
                                           GridCanvas, sticky='nws', column=1,
                                           row=0)

        self.register_mouse_down(self.handle_mouse_down)
        self.register_mouse_up(self.handle_mouse_up)
        self.register_mouse_moved(self.handle_mouse_moved)

        self.select_char(0)

    def select_char(self, c):
        g = self.document.font.instantiate(c)
        self.ascii_canvas.update_image(c)
        self.ascii_canvas.select_char(c)
        self.grid_canvas.select_char(c, g)

    def handle_mouse_down(self, _, e, x, y):
        if e.widget == self.ascii_canvas._canvas:
            c = self.ascii_canvas.pos_to_char(x, y)
            self.select_char(c)
        elif e.widget == self.grid_canvas._canvas:
            self.grid_canvas.handle_mouse_down(x, y)

    def handle_mouse_up(self, _, e, x, y):
        if e.widget == self.grid_canvas._canvas:
            self.grid_canvas.handle_mouse_up(x, y)

    def handle_mouse_moved(self, _, e, x, y):
        if e.widget == self.grid_canvas._canvas:
            self.grid_canvas.handle_mouse_moved(x, y)
