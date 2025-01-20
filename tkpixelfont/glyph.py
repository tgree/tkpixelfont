import tkinter


class Glyph:
    '''
    Glyph for a monochrome pixel image.  The colors are:

        1 - black
        0 - white
    '''
    def __init__(self, c, w, h):
        self.char   = c
        self.width  = w
        self.height = h
        self.pixels = None
        self.image  = tkinter.PhotoImage(width=w, height=h)
        self.set_all_pixels(0)

    def get_pixel(self, x, y):
        return self.pixels[y * self.width + x]

    def set_pixel(self, x, y, v):
        self.pixels[y * self.width + x] = v
        self.image.put('black' if v else 'white', to=(x, y, x + 1, y + 1))

    def set_all_pixels(self, v):
        self.pixels = [v] * (self.width * self.height)
        self.image.put('black' if v else 'white',
                       to=(0, 0, self.width, self.height))

    def render_tk_image(self):
        return self.image
