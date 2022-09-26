from ui.button_render import ButtonEnum
from ..main import display, WIDTH, HEIGHT, button_a, button_b, button_x, button_y, project
import time
import button_render

up_btn = button_a
down_btn = button_b
back_btn = button_x
next_btn = button_y

class Stage1():

    steps = True

    def open(self):
        display.clear()
        display.text("Steps:", WIDTH/4, HEIGHT/3)
        display.text("Levers:", 3*WIDTH/4, 2*HEIGHT/3)

        width = max(measure_text("Increase"), measure_text("Decrease"))
        button_render.place_button("Back", width, 16, ButtonEnum.TOP_LEFT)
        button_render.place_button("Next", width, 16, ButtonEnum.TOP_RIGHT)
        button_render.place_button("Increase", width, 16, ButtonEnum.BOTTOM_LEFT)
        button_render.place_button("Decrease", width, 16, ButtonEnum.BOTTOM_RIGHT)

        self.update_display()

        finished = False
        while not finished:
            time.sleep(0.1)
            if up_btn.read():
                if self.steps:
                    project.total_steps = project.total_steps+1
                    self.update_steps()
                else:
                    project.levers = project.levers+1
                    self.update_levers()
            if down_btn.read():
                if self.steps:
                    if project.total_steps > 1:
                        project.total_steps = project.total_steps-1
                        self.update_steps()
                else:
                    if project.levers > 1:
                        project.levers = project.levers-1
                        self.update_levers()
            if next_btn.read():
                if self.steps:
                    self.steps = False
                else:
                    finished = True
            if back_btn.read():
                if not self.steps:
                    self.steps = True
    
    def update_display(self):
        self.update_steps()
        self.update_levers()
    
    def update_steps(self):
        display.rectangle(WIDTH/8, HEIGHT/2, WIDTH/4, HEIGHT/3)
        display.text(project.total_steps, WIDTH/4, 2*HEIGHT/3)
        display.update()
    
    def update_levers(self):
        display.rectangle(5*WIDTH/8, HEIGHT/2, WIDTH/4, HEIGHT/3)
        display.text(project.levers, 3*WIDTH/4, 2*HEIGHT/3)
        display.update()

class Stage2():

    def open(self):
        display.clear()

def setup():
    stage1 = Stage1()
    stage1.open()

    setup_finished = False
    while not setup_finished:
        stage2 = Stage2()
        stage2.open()

