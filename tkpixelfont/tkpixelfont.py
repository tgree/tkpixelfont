#!/usr/bin/env python3
from .workspace import Workspace


ASCII_W         = 38
ASCII_H         = 52

WINDOW_X        = 5
WINDOW_Y        = 45
WINDOW_W        = 1500
WINDOW_H        = ASCII_H * 16 + 4


def main():
    w = Workspace(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H, ASCII_W, ASCII_H)
    w.mainloop()


def _main():
    main()


if __name__ == '__main__':
    _main()
