# main.py -- put your code here!

from project import Project
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
from ui.welcome import Welcome

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB332, rotate=90)
backlight = 0.5
display.set_backlight=backlight
display.set_font("sans")

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WIDTH, HEIGHT = display.get_bound()

welcome = Welcome()

