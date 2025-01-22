#!/usr/bin/env python3
from .tk.elems import Canvas

from .geom import Vec, Rect


DM_NONE    = 0
DM_DRAWING = 1
DM_ERASING = 2


class GridCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.selected_glyph = None

        # Draw the outline of the pixel grid.
        p = Vec(16, 4)
        r = Rect(p, p + Vec(16 * 32 + 2, 16 * 32 + 2))
        self.add_rectangle(r)

        # Generate the pixel grid individual pixel rectangles.
        self.pixel_elems = []
        self.pixel_rect = Rect(r.p0 + Vec(2, 2), r.p1 - Vec(2, 2))
        for y in range(32):
            for x in range(32):
                p = self.pixel_rect.p0 + Vec(x * 16, y * 16)
                r = Rect(p, p + Vec(14, 14))
                self.pixel_elems.append(self.add_rectangle(r, fill='white',
                                                           outline='white'))

        self.draw_mode  = DM_NONE
        self.erasing    = False

    def update_pixel(self, x, y):
        '''
        Given mouse coordinates, (x, y), turn the pixel on or off if it is in
        our drawing grid and we are in draw or erase mode.
        '''
        p = Vec(x, y)
        if not self.pixel_rect.overlaps_point(p):
            return

        px = (x - self.pixel_rect.p0.x) // 16
        py = (y - self.pixel_rect.p0.y) // 16
        if self.draw_mode == DM_ERASING:
            if self.selected_glyph.get_pixel(px, py):
                self.selected_glyph.set_pixel(px, py, 0)
                self.pixel_elems[py * 32 + px].configure(fill='white',
                                                         outline='white')
        elif self.draw_mode == DM_DRAWING:
            if not self.selected_glyph.get_pixel(px, py):
                self.selected_glyph.set_pixel(px, py, 1)
                self.pixel_elems[py * 32 + px].configure(fill='black',
                                                         outline='black')

    def select_char(self, c, g):
        self.selected_glyph = g

        w = g.width
        h = g.height
        for pe in self.pixel_elems:
            pe.configure(fill='white', outline='white')
        for y in range(h):
            for x in range(w):
                c = y * 32 + x
                if g.get_pixel(x, y):
                    self.pixel_elems[c].configure(fill='black', outline='black')
                else:
                    self.pixel_elems[c].configure(fill='white', outline='white')

    def handle_mouse_down(self, x, y):
        px = (x - self.pixel_rect.p0.x) // 16
        py = (y - self.pixel_rect.p0.y) // 16
        if self.selected_glyph.get_pixel(px, py):
            self.draw_mode = DM_ERASING
        else:
            self.draw_mode = DM_DRAWING

        self.update_pixel(x, y)

    def handle_mouse_up(self, _x, _y):
        self.draw_mode = DM_NONE

    def handle_mouse_moved(self, x, y):
        self.update_pixel(x, y)
