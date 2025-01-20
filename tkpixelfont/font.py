from .glyph import Glyph


class Font:
    def __init__(self, w, h):
        self.width     = w
        self.height    = h
        self.glyphs    = [None] * 256

        self.glyphs[0] = Glyph(0, w, h)
        self.glyphs[0].set_all_pixels(0)

    def get_glyph(self, c):
        return self.glyphs[c] or self.glyphs[0]

    def instantiate(self, c):
        if self.glyphs[c] is None:
            self.glyphs[c] = Glyph(0, self.width, self.height)
            self.glyphs[c].set_all_pixels(0)
        return self.glyphs[c]
