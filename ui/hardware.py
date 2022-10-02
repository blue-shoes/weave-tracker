from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8


class Hardware():

    def __init__(self):
        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8, rotate=0)
        self.backlight = 0.5
        self.display.set_backlight(self.backlight)
        self.display.set_font("sans")

        self.button_a = Button(12)
        self.button_b = Button(13)
        self.button_x = Button(14)
        self.button_y = Button(15)

        self.WIDTH, self.HEIGHT = self.display.get_bounds()

        self.BTN_HEIGHT = 16
        self.LEVER_DIST = 50
        self.MAX_LEVER_WIDTH = 30

        self.BG = self.display.create_pen(40,40,40)
        self.FG = self.display.create_pen(225, 225, 225)