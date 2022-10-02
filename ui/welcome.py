from ui.button_render import TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
import time
from ui import button_render

class Welcome():

    def __init__(self, hardware):
        self.hardware = hardware
        self.bright_up = self.hardware.button_a
        self.bright_down = self.hardware.button_b
        self.next_screen = self.hardware.button_y

    def open(self):
        # Main display
        self.main_display()
        finished = False

        while not finished:
            time.sleep(0.1)
            if self.bright_up.read():
                if self.hardware.backlight < 1.0:
                    self.hardware.backlight = self.hardware.backlight + 0.1
                    if self.hardware.backlight > 1.0:
                        self.hardware.backlight = 1.0
                    self.hardware.display.set_backlight(self.hardware.backlight)
                    self.main_display()
            if self.bright_down.read():
                if self.hardware.backlight > 0.1:
                    self.hardware.backlight = self.hardware.backlight - 0.1
                    self.hardware.display.set_backlight(self.hardware.backlight)
                    self.main_display()
            if self.next_screen.read():
                finished = True

    
    def main_display(self):
        self.hardware.display.set_pen(self.hardware.BG)
        self.hardware.display.clear()
        self.hardware.display.set_pen(self.hardware.FG)
        width = self.hardware.display.measure_text('Welcome!', scale=1.0)
        self.hardware.display.text("Welcome!", int(self.hardware.WIDTH/2)-int(width/2), int(self.hardware.HEIGHT/2), scale=1.0)
        # Brightness box
        self.hardware.display.line(5, 5, 5, self.hardware.HEIGHT - 5)
        self.hardware.display.line(5, 5, 10, 5)
        self.hardware.display.line(10, 5, 10, self.hardware.HEIGHT - 5)
        self.hardware.display.line(5, self.hardware.HEIGHT - 5, 10, self.hardware.HEIGHT - 5)
        # And value
        self.hardware.display.rectangle(5, int((self.hardware.HEIGHT - 10) * (1.0-self.hardware.backlight)) + 5, 5, int((self.hardware.HEIGHT - 10) * self.hardware.backlight))

        # Buttons
        width = max(self.hardware.display.measure_text("Bright -", scale=0.5), self.hardware.display.measure_text("Bright +", scale=0.5))
        button_render.place_button(self.hardware, "Bright +", width, self.hardware.BTN_HEIGHT, TOP_LEFT, width_pad = 11)
        button_render.place_button(self.hardware, "Bright -", width, self.hardware.BTN_HEIGHT, BOTTOM_LEFT, width_pad = 11)
        width = self.hardware.display.measure_text("Start", scale=0.5)
        button_render.place_button(self.hardware, "Start", width, self.hardware.BTN_HEIGHT, BOTTOM_RIGHT)
        self.hardware.display.update()

