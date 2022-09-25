from ..main import display, WIDTH, HEIGHT, button_a, button_b, button_x, button_y, backlight
import time
from picographics import measure_text

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
            if self.bright_down.read() > 0.1:
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

        # Button labels
        width = measure_text("Bright -")
        display.text("Bright +", width/2 + 2, HEIGHT - 8)
        display.text("Bright -", width/2 + 2, 8)
        display.text("Start", WIDTH - width/2 - 2, 8)

        # And label outlines
        display.line(0, HEIGHT-16, width + 4, HEIGHT-16)
        display.line(width + 4, HEIGHT, width + 4, HEIGHT-16)
        display.line(0, 16, width + 4, 16)
        display.line(width+4, 0, width+4, 16)
        display.line(WIDTH, 16, WIDTH - (width + 4), 16)
        display.line(WIDTH - (width+4), 0, WIDTH - (width+4), 16)

        display.update()

