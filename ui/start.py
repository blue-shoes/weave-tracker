from ui.button_render import TOP_RIGHT, TOP_LEFT, BOTTOM_LEFT, BOTTOM_RIGHT
import time
from ui import button_render

class StartMenu():

    def __init__(self, hardware, project):
        self.hardware = hardware
        self.new_proj_button = self.hardware.button_y
        self.resume_button = self.hardware.button_b
        self.project = project

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
    
    def main_display(self):
        self.hardware.display.set_pen(self.hardware.BG)
        self.hardware.display.clear()
        self.hardware.display.set_pen(self.hardware.FG)
        width = self.hardware.display.measure_text('Start Menu',scale=1.0)
        self.hardware.display.text("Start Menu", int(self.hardware.WIDTH/2 - width/2), int(self.hardware.HEIGHT/2), scale=1.0)

        width = self.hardware.display.measure_text("Resume Project", scale=0.5)

        if self.project is not None:
            button_render.place_button(self.hardware, "Resume Project", width, self.hardware.BTN_HEIGHT, BOTTOM_LEFT)
        button_render.place_button(self.hardware, "New Project", width, self.hardware.BTN_HEIGHT, BOTTOM_RIGHT)
        self.hardware.display.update()
