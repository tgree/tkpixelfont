#!/usr/bin/env python3
from .tk.elems import TKBase

from .ascii_canvas import ASCIICanvas


class Workspace(TKBase):
    def __init__(self, x, y, w, h, ascii_w, ascii_h):
        super().__init__()

        self.set_title('tkpixelfont')

        self.set_geometry(x, y, w, h)
        self.ascii_canvas = self.add_canvas(w, h, ASCIICanvas, ascii_w, ascii_h,
                                            sticky='nws')

        self.register_mouse_down(self.handle_mouse_down)
        self.register_mouse_up(self.handle_mouse_up)
        self.register_mouse_moved(self.handle_mouse_moved)

        self.ascii_canvas.focus_set()

    def handle_mouse_down(self, _, e, x, y):
        if e.widget == self.ascii_canvas._canvas:
            self.ascii_canvas.handle_mouse_down(x, y)

    def handle_mouse_up(self, _, e, x, y):
        if e.widget == self.ascii_canvas._canvas:
            # self.ascii_canvas.handle_mouse_up(x, y)
            pass

    def handle_mouse_moved(self, _, e, x, y):
        if e.widget == self.ascii_canvas._canvas:
            # self.ascii_canvas.handle_mouse_moved(x, y)
            pass
