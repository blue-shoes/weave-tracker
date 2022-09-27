from ui.button_render import ButtonEnum
from ..main import display, WIDTH, HEIGHT, button_b, button_y, project, BTN_HEIGHT
import time
import button_render

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
    
    def main_display(self):
        display.clear()
        display.text("Start Menu", WIDTH/2, HEIGHT/2)

        width = measure_text("Resume Project")

        if project is not None:
            button_render.place_button("Resume Project", width, BTN_HEIGHT, ButtonEnum.BOTTOM_LEFT)
        button_render.place_button("New Project", width, BTN_HEIGHT, ButtonEnum.BOTTOM_RIGHT)
        display.update()
