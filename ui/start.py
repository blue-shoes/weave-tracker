from ..main import display, WIDTH, HEIGHT, button_a, button_b, button_x, button_y, backlight
import time

class StartMenu():

    new_proj_button = button_y
    resume_button = button_b

    def open(self):
        # Main display
        self.main_display()
        finished = False

        while not finished:
            time.sleep(0.1)
            if self.new_proj_button.read():
                self.new_proj = True
                finished = True
            if self.resume_button.read():
                self.new_proj = False
                finished = True