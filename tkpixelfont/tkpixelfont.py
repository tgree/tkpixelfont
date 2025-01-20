#!/usr/bin/env python3
import tkinter.font

from .tk.elems import Canvas
from .workspace import Workspace
from .geom import Vec, Rect


WINDOW_X        = 10
WINDOW_Y        = 50
WINDOW_W        = 1600
WINDOW_H        = 804


CHR_MAP = [
      '00',  '01',  '02',  '03',  '04',  '05',  '06',  '07',  # noqa: E131
    '\\bs',  '09', '\\n',  '0B',  '0C', '\\r',  '0E',  '0F',  # noqa: E131
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
        f = tkinter.font.Font(family='Arial', size=12)

        for y in range(16):
            for x in range(16):
                p = Vec(4, 4) + Vec(x * 34, y * 50)
                r = Rect(p, p + Vec(32, 32))
                self.add_rectangle(r)
                self.add_text(p + Vec(16, 33), text=CHR_MAP[y*16 + x],
                              anchor='n', font=f)

        p = Vec(16, 4) + Vec(16 * 34 + 4, 0)
        r = Rect(p, p + Vec(16 * 32 + 2, 16 * 32 + 2))
        self.add_rectangle(r)

        self.pixel_elems = []
        self.pixel_rect = Rect(r.p0 + Vec(2, 2), r.p1 - Vec(2, 2))
        for y in range(32):
            for x in range(32):
                p = self.pixel_rect.p0 + Vec(x * 16, y * 16)
                r = Rect(p, p + Vec(14, 14))
                self.pixel_elems.append(self.add_rectangle(r, fill='black'))
                self.pixel_elems[-1].hide()

        self.draw_mode  = DM_NONE
        self.erasing    = False

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
            self.pixel_elems[py * 32 + px].hide()
        elif self.draw_mode == DM_DRAWING:
            self.pixel_elems[py * 32 + px].show()

    def handle_mouse_down(self, _e, x, y):
        p = Vec(x, y)
        if not self.pixel_rect.overlaps_point(p):
            return

        px = (x - self.pixel_rect.p0.x) // 16
        py = (y - self.pixel_rect.p0.y) // 16
        pe = self.pixel_elems[py * 32 + px]
        if pe.is_visible():
            self.draw_mode = DM_ERASING
        else:
            self.draw_mode = DM_DRAWING

        self.update_pixel(x, y)

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
