#!/usr/bin/env python3
import tkinter.font
import tkinter.filedialog

from .tk.elems import Canvas
from .workspace import Workspace
from .geom import Vec, Rect
from .font import Font


ASCII_W         = 38
ASCII_H         = 52

WINDOW_X        = 5
WINDOW_Y        = 45
WINDOW_W        = 1500
WINDOW_H        = ASCII_H * 16 + 4

FONT_INFO_X     = 16 * ASCII_W + 16 * 32 + 32
FONT_INFO_Y     = 4


CHR_MAP = [
      '00',  '01',  '02',  '03',  '04',  '05',  '06',  '07',  # noqa: E131
     '\\b', '\\t', '\\n',  '0B',  '0C', '\\r',  '0E',  '0F',  # noqa: E131
      '10',  '11',  '12',  '13',  '14',  '15',  '16',  '17',  # noqa: E131
      '18',  '19',  '1A', 'ESC',  '1C',  '1D',  '1E',  '1F',  # noqa: E131
      'SP',   '!',   '"',   '#',   '$',   '%',   '&',  '\'',  # noqa: E131
       '(',   ')',   '*',   '+',   ',',   '-',   '.',   '/',  # noqa: E131
       '0',   '1',   '2',   '3',   '4',   '5',   '6',   '7',  # noqa: E131
       '8',   '9',   ':',   ';',   '<',   '=',   '>',   '?',  # noqa: E131
       '@',   'A',   'B',   'C',   'D',   'E',   'F',   'G',  # noqa: E131
       'H',   'I',   'J',   'K',   'L',   'M',   'N',   'O',  # noqa: E131
       'P',   'Q',   'R',   'S',   'T',   'U',   'V',   'W',  # noqa: E131
       'X',   'Y',   'Z',   '[',  '\\',   ']',   '^',   '_',  # noqa: E131
       '`',   'a',   'b',   'c',   'd',   'e',   'f',   'g',  # noqa: E131
       'h',   'i',   'j',   'k',   'l',   'm',   'n',   'o',  # noqa: E131
       'p',   'q',   'r',   's',   't',   'u',   'v',   'w',  # noqa: E131
       'x',   'y',   'z',   '{',   '|',   '}',   '~', 'DEL',  # noqa: E131
      '80',  '81',  '82',  '83',  '84',  '85',  '86',  '87',  # noqa: E131
      '88',  '89',  '8A',  '8B',  '8C',  '8D',  '8E',  '8F',  # noqa: E131
      '90',  '91',  '92',  '93',  '94',  '95',  '96',  '97',  # noqa: E131
      '98',  '99',  '9A',  '9B',  '9C',  '9D',  '9E',  '9F',  # noqa: E131
      'A0',  'A1',  'A2',  'A3',  'A4',  'A5',  'A6',  'A7',  # noqa: E131
      'A8',  'A9',  'AA',  'AB',  'AC',  'AD',  'AE',  'AF',  # noqa: E131
      'B0',  'B1',  'B2',  'B3',  'B4',  'B5',  'B6',  'B7',  # noqa: E131
      'B8',  'B9',  'BA',  'BB',  'BC',  'BD',  'BE',  'BF',  # noqa: E131
      'C0',  'C1',  'C2',  'C3',  'C4',  'C5',  'C6',  'C7',  # noqa: E131
      'C8',  'C9',  'CA',  'CB',  'CC',  'CD',  'CE',  'CF',  # noqa: E131
      'D0',  'D1',  'D2',  'D3',  'D4',  'D5',  'D6',  'D7',  # noqa: E131
      'D8',  'D9',  'DA',  'DB',  'DC',  'DD',  'DE',  'DF',  # noqa: E131
      'E0',  'E1',  'E2',  'E3',  'E4',  'E5',  'E6',  'E7',  # noqa: E131
      'E8',  'E9',  'EA',  'EB',  'EC',  'ED',  'EE',  'EF',  # noqa: E131
      'F0',  'F1',  'F2',  'F3',  'F4',  'F5',  'F6',  'F7',  # noqa: E131
      'F8',  'F9',  'FA',  'FB',  'FC',  'FD',  'FE',  'FF',  # noqa: E131
]


DM_NONE    = 0
DM_DRAWING = 1
DM_ERASING = 2


class MainCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font = Font(32, 32)
        self.selected_char = None
        self.selected_glyph = None
        self.image_elems = [None] * 256
        self.image_points = []

        monaco_font    = tkinter.font.Font(family='Monaco', size=12)
        arial_b12_font = tkinter.font.Font(family='Arial', size=12,
                                           weight='bold')
        arial_b10_font = tkinter.font.Font(family='Arial', size=10,
                                           weight='bold')
        arial_10_font  = tkinter.font.Font(family='Arial', size=10)

        # Render the grid of ASCII characters.
        self.ascii_grid_rect = Rect(Vec(4, 4), Vec(4 + 16 * ASCII_W,
                                                   4 + 16 * ASCII_H))
        for y in range(16):
            for x in range(16):
                p = self.ascii_grid_rect.p0 + Vec(x * ASCII_W, y * ASCII_H)
                r = Rect(p, p + Vec(33, 33))
                self.add_rectangle(r)

                c = y * 16 + x
                self.add_text(p + Vec(17, 33), text=CHR_MAP[c], anchor='n',
                              font=monaco_font)

                self.image_points.append(p)
                self.render_char(c)

        # Generate a rectangle for the selected character in the ASCII grid.
        p0 = self.ascii_grid_rect.p0 - Vec(2, 2)
        r = Rect(p0, p0 + Vec(38, 51))
        self.selection_rect = self.add_rectangle(r, fill='', width=2)

        # Draw the outline of the pixel grid.
        p = Vec(16, 4) + Vec(16 * ASCII_W + 4, 0)
        r = Rect(p, p + Vec(16 * 32 + 2, 16 * 32 + 2))
        self.add_rectangle(r)

        # Generate the pixel grid individual pixel rectangles.
        self.pixel_elems = []
        self.pixel_rect = Rect(r.p0 + Vec(2, 2), r.p1 - Vec(2, 2))
        for y in range(32):
            for x in range(32):
                p = self.pixel_rect.p0 + Vec(x * 16, y * 16)
                r = Rect(p, p + Vec(14, 14))
                self.pixel_elems.append(self.add_rectangle(r))

        # Generate the font info panel.
        v = Vec(FONT_INFO_X, FONT_INFO_Y)
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

        self.draw_mode  = DM_NONE
        self.erasing    = False

        # Select character 0.
        self.select_char(0)

    def update_pixel(self, x, y):
        '''
        Given mouse coordinates, (x, y), turn the pixel on if it overlaps our
        drawing grid.
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
                self.render_char(self.selected_char)
        elif self.draw_mode == DM_DRAWING:
            if not self.selected_glyph.get_pixel(px, py):
                self.selected_glyph.set_pixel(px, py, 1)
                self.pixel_elems[py * 32 + px].configure(fill='black',
                                                         outline='black')
                self.render_char(self.selected_char)

    def render_char(self, c):
        if self.image_elems[c] is not None:
            self.delete_elem(self.image_elems[c])

        image = self.font.get_glyph(c).image
        self.image_elems[c] = self.add_image(self.image_points[c] + Vec(1, 1),
                                             image, anchor='nw')

    def handle_pixel_rect_click(self, x, y):
        self.selected_glyph = self.font.instantiate(self.selected_char)

        px = (x - self.pixel_rect.p0.x) // 16
        py = (y - self.pixel_rect.p0.y) // 16
        if self.selected_glyph.get_pixel(px, py):
            self.draw_mode = DM_ERASING
        else:
            self.draw_mode = DM_DRAWING

        self.update_pixel(x, y)

    def select_char(self, c):
        g = self.font.instantiate(c)
        self.render_char(c)

        p0 = self.ascii_grid_rect.p0 - Vec(2, 2)
        x  = c % 16
        y  = c // 16
        self.selection_rect.move_to(p0.x + x * ASCII_W, p0.y + y * ASCII_H)

        self.selected_char = c
        self.selected_glyph = g
        w = self.selected_glyph.width
        h = self.selected_glyph.height
        for pe in self.pixel_elems:
            pe.configure(fill='white', outline='white')
        for y in range(h):
            for x in range(w):
                if g.get_pixel(x, y):
                    self.pixel_elems[y * 32 + x].configure(fill='black',
                                                           outline='black')

    def handle_ascii_grid_rect_click(self, x, y):
        px = (x - self.ascii_grid_rect.p0.x) // ASCII_W
        py = (y - self.ascii_grid_rect.p0.y) // ASCII_H
        self.select_char(py * 16 + px)

    def handle_mouse_down(self, _e, x, y):
        p = Vec(x, y)
        if self.pixel_rect.overlaps_point(p):
            self.handle_pixel_rect_click(x, y)
        elif self.ascii_grid_rect.overlaps_point(p):
            self.handle_ascii_grid_rect_click(x, y)

    def handle_mouse_up(self, _e, _x, _y):
        self.draw_mode = DM_NONE

    def handle_mouse_moved(self, _e, x, y):
        self.update_pixel(x, y)


def main():
    w = Workspace(MainCanvas, WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H)
    w.mainloop()


def _main():
    main()


if __name__ == '__main__':
    _main()
