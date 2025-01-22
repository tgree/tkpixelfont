#!/usr/bin/env python3
import tkinter.font

from .tk.elems import Canvas
from .geom import Vec, Rect
from .font import Font


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


class ASCIICanvas(Canvas):
    def __init__(self, ascii_w, ascii_h, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ascii_w = ascii_w
        self.ascii_h = ascii_h

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
        self.ascii_grid_rect = Rect(Vec(4, 4), Vec(4 + 16 * ascii_w,
                                                   4 + 16 * ascii_h))
        for y in range(16):
            for x in range(16):
                p = self.ascii_grid_rect.p0 + Vec(x * ascii_w, y * ascii_h)
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

    def render_char(self, c):
        if self.image_elems[c] is not None:
            self.delete_elem(self.image_elems[c])

        image = self.font.get_glyph(c).image
        self.image_elems[c] = self.add_image(self.image_points[c] + Vec(1, 1),
                                             image, anchor='nw')

    def select_char(self, c):
        g = self.font.instantiate(c)
        self.render_char(c)

        p0 = self.ascii_grid_rect.p0 - Vec(2, 2)
        x  = c % 16
        y  = c // 16
        self.selection_rect.move_to(p0.x + x * self.ascii_w,
                                    p0.y + y * self.ascii_h)

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

    def handle_mouse_down(self, x, y):
        px = (x - self.ascii_grid_rect.p0.x) // self.ascii_w
        py = (y - self.ascii_grid_rect.p0.y) // self.ascii_h
        self.select_char(py * 16 + px)
