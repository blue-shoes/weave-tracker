from ui.button_render import ButtonEnum
from ..main import display, WIDTH, HEIGHT, button_a, button_b, button_y, backlight
import time
from picographics import measure_text
import button_render

class Welcome():

    bright_up = button_a
    bright_down = button_b
    next_screen = button_y

    def open(self):
        # Main display
        self.main_display()
        finished = False

        while not finished:
            time.sleep(0.1)
            if self.bright_up.read():
                if backlight < 1:
                    backlight = backlight + 0.1
                    display.set_backlight = backlight
                    self.main_display()
            if self.bright_down.read():
                if backlight > 0.1:
                    backlight = backlight - 0.1
                    display.set_backlight = backlight
                    self.main_display()
            if self.next_screen.read():
                finished = True

    
    def main_display(self):
        display.clear()
        display.text("Welcome!", WIDTH/2, HEIGHT/2)
        # Brightness box
        display.line(5, 5, 5, HEIGHT - 5)
        display.line(5, 5, 10, 5)
        display.line(10, 5, 10, HEIGHT - 5)
        display.line(5, HEIGHT - 5, 10, HEIGHT - 5)
        # And value
        display.rectangle(5, 5, 5, (HEIGHT - 10) * backlight)

        # Buttons
        width = max(measure_text("Bright -"), measure_text("Bright +"))
        button_render.place_button("Bright +", width, 16, ButtonEnum.TOP_LEFT)
        button_render.place_button("Bright -", width, 16, ButtonEnum.BOTTOM_LEFT)
        button_render.place_button("Start", width, 16, ButtonEnum.BOTTOM_RIGHT)

        display.update()

