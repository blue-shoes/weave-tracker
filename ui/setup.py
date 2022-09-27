from ui.button_render import ButtonEnum
from ..main import display, WIDTH, HEIGHT, button_a, button_b, button_x, button_y, project, BTN_HEIGHT, LEVER_DIST, MAX_LEVER_WIDTH
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
        button_render.place_button("Back", width, BTN_HEIGHT, ButtonEnum.TOP_LEFT)
        button_render.place_button("Next", width, BTN_HEIGHT, ButtonEnum.TOP_RIGHT)
        button_render.place_button("Increase", width, BTN_HEIGHT, ButtonEnum.BOTTOM_LEFT)
        button_render.place_button("Decrease", width, BTN_HEIGHT, ButtonEnum.BOTTOM_RIGHT)

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

    def __init__(self, step, lever_width, margin, radius):
        self.step = step
        self.lever = 0
        self.lever_width = lever_width
        self.margin = margin
        self.radius = radius

    def open(self):
        next = False
        display.clear()

        display.text(f"Step {self.step}/{project.total_steps}", WIDTH/2, HEIGHT - 20)

        display.text("Set Lever positions", WIDTH/2, 20)

        width = max(measure_text("Increase"), measure_text("Decrease"))
        button_render.place_button("Back", width, BTN_HEIGHT, ButtonEnum.TOP_LEFT)
        button_render.place_button("Next", width, BTN_HEIGHT, ButtonEnum.TOP_RIGHT)
        button_render.place_button("Up", width, BTN_HEIGHT, ButtonEnum.BOTTOM_LEFT)
        button_render.place_button("Down", width, BTN_HEIGHT, ButtonEnum.BOTTOM_RIGHT)

        for l in range(project.levers):
            if project.get_sequence(self.step)[l] == 1:
                self.set_up(l)
            else:
                self.set_down(l)
        
        display.update()

        elapsed = 0.0
        exit = False
        while not exit:
            time.sleep(0.1)
            elapsed += 0.1
        
    def set_up(self, lever_num):
        display.circle(self.margin + self.lever_width*lever_num + self.radius + 3, HEIGHT - LEVER_DIST, self.radius)
        display.line(self.margin + self.lever_width*lever_num + 3, LEVER_DIST, self.margin + self.lever_width*lever_num + 3 + 2*self.radius, LEVER_DIST)
    
    def set_down(self, lever_num):
        display.circle(self.margin + self.lever_width*lever_num + self.radius + 3, LEVER_DIST, self.radius)
        display.line(self.margin + self.lever_width*lever_num + 3, HEIGHT - LEVER_DIST, self.margin + self.lever_width*lever_num + 3 + 2*self.radius, HEIGHT - LEVER_DIST)
        

def setup():
    stage1 = Stage1()
    stage1.open()

    project.initialize()

    setup_finished = False
    step = 0

    lever_width = min((WIDTH - 20) / project.levers, MAX_LEVER_WIDTH)
    margin = (WIDTH - project.levers * lever_width)/2
    radius = int(lever_width/2 - 3) 

    while not setup_finished:
        stage2 = Stage2(step, lever_width, margin, radius)
        stage2.open()

        if stage2.next:
            step += 1
        elif step > 0:
            step -= 1
        if step == project.total_steps:
            setup_finished = True

