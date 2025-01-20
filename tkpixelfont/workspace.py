#!/usr/bin/env python3
from .tk.elems import TKBase


class Workspace(TKBase):
    def __init__(self, canvas_cls, x, y, w, h):
        super().__init__()

        self.set_title('tkpixelfont')

        self.set_geometry(x, y, w, h)
        self.canvas = self.add_canvas(w, h, 0, 0, sticky='nws', _cls=canvas_cls)

        self.register_mouse_down(self.handle_mouse_down)
        self.register_mouse_up(self.handle_mouse_up)
        self.register_mouse_moved(self.handle_mouse_moved)

        self.canvas.focus_set()

    def handle_mouse_down(self, _, e, x, y):
        if e.widget == self.canvas._canvas:
            self.canvas.handle_mouse_down(e, x, y)

    def handle_mouse_up(self, _, e, x, y):
        if e.widget == self.canvas._canvas:
            self.canvas.handle_mouse_up(e, x, y)

    def handle_mouse_moved(self, _, e, x, y):
        if e.widget == self.canvas._canvas:
            self.canvas.handle_mouse_moved(e, x, y)
