from ui.button_render import TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
import time
from ui import button_render

up_btn = button_a
down_btn = button_b
back_btn = button_x
next_btn = button_y

class Stage1():

    steps = True
    
    def __init__(self, hardware, project):
        self.hardware = hardware
        self.project = project

    def open(self):
        self.hardware.set_bg_pen()
        self.hardware.display.clear()
        self.hardware.set_fg_pen()
        self.hardware.display.text("Steps:", self.hardware.WIDTH/4, self.hardware.HEIGHT/3)
        self.hardware.display.text("Levers:", 3*self.hardware.WIDTH/4, 2*self.hardware.HEIGHT/3)

        width = max(self.hardware.display.measure_text("Increase", scale=0.5), self.hardware.display.measure_text("Decrease", scale=0.5))
        button_render.place_button(self.hardware, "Back", width, self.hardware.BTN_HEIGHT, TOP_LEFT)
        button_render.place_button(self.hardware, "Next", width, self.hardware.BTN_HEIGHT, TOP_RIGHT)
        button_render.place_button(self.hardware, "Increase", width, self.hardware.BTN_HEIGHT, BOTTOM_LEFT)
        button_render.place_button(self.hardware, "Decrease", width, self.hardware.BTN_HEIGHT, BOTTOM_RIGHT)

        self.update_display()

        finished = False
        while not finished:
            time.sleep(0.1)
            if up_btn.read():
                if self.steps:
                    self.project.total_steps = self.project.total_steps+1
                    self.update_steps()
                else:
                    self.project.levers = self.project.levers+1
                    self.update_levers()
            if down_btn.read():
                if self.steps:
                    if self.project.total_steps > 1:
                        self.project.total_steps = self.project.total_steps-1
                        self.update_steps()
                else:
                    if self.project.levers > 1:
                        self.project.levers = self.project.levers-1
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
        self.hardware.set_bg_pen()
        self.hardware.display.rectangle(self.hardware.WIDTH/8, self.hardware.HEIGHT/2, self.hardware.WIDTH/4, self.hardware.HEIGHT/3)
        self.hardware.set_fg_pen()
        self.hardware.display.text(self.project.total_steps, self.hardware.WIDTH/4, 2*self.hardware.HEIGHT/3)
        self.hardware.display.update()
    
    def update_levers(self):
        self.hardware.set_bg_pen()
        self.hardware.display.rectangle(5*self.hardware.WIDTH/8, self.hardware.HEIGHT/2, self.hardware.WIDTH/4, self.hardware.HEIGHT/3)
        self.hardware.set_fg_pen()
        self.hardware.display.text(self.project.levers, 3*self.hardware.WIDTH/4, 2*self.hardware.HEIGHT/3)
        self.hardware.display.update()

class Stage2():

    def __init__(self, hardware, project, step, lever_width, margin, radius):
        self.hardware = hardware
        self.project = project
        self.step = step
        self.lever = 0
        self.lever_width = lever_width
        self.margin = margin
        self.radius = radius

    def open(self):
        self.next = False
        self.hardware.set_bg_pen()
        self.hardware.display.clear()
        self.hardware.set_fg_pen()
        self.hardware.display.text(f"Step {self.step}/{self.project.total_steps}", self.hardware.WIDTH/2, self.hardware.HEIGHT - 20)

        self.hardware.display.text("Set Lever positions", self.hardware.WIDTH/2, 20)

        width = max(self.hardware.display.measure_text("Increase"), self.hardware.display.measure_text("Decrease"))
        button_render.place_button(self.hardware, "Back", width, self.hardware.BTN_HEIGHT, TOP_LEFT)
        button_render.place_button(self.hardware, "Next", width, self.hardware.BTN_HEIGHT, TOP_RIGHT)
        button_render.place_button(self.hardware, "Up", width, self.hardware.BTN_HEIGHT, BOTTOM_LEFT)
        button_render.place_button(self.hardware, "Down", width, self.hardware.BTN_HEIGHT, BOTTOM_RIGHT)

        for l in range(self.project.levers):
            if self.project.get_sequence(self.step)[l] == 1:
                self.set_up(l)
            else:
                self.set_down(l)
        
        self.hardware.display.update()

        elapsed = 0.0
        exit = False
        while not exit:
            time.sleep(0.1)
            elapsed += 0.1
        
    def set_up(self, lever_num):
        self.hardware.display.circle(self.margin + self.lever_width*lever_num + self.radius + 3, self.hardware.HEIGHT - self.hardware.LEVER_DIST, self.radius)
        self.hardware.display.line(self.margin + self.lever_width*lever_num + 3, self.hardware.LEVER_DIST, self.margin + self.lever_width*lever_num + 3 + 2*self.radius, self.hardware.LEVER_DIST)
    
    def set_down(self, lever_num):
        self.hardware.display.circle(self.margin + self.lever_width*lever_num + self.radius + 3, self.hardware.LEVER_DIST, self.radius)
        self.hardware.display.line(self.margin + self.lever_width*lever_num + 3, self.hardware.HEIGHT - self.hardware.LEVER_DIST, self.margin + self.lever_width*lever_num + 3 + 2*self.radius, self.hardware.HEIGHT - self.hardware.LEVER_DIST)
        

def setup(hardware, project):
    stage1 = Stage1(hardware, project)
    stage1.open()

    project.initialize()

    setup_finished = False
    step = 0

    lever_width = int(min((hardware.WIDTH - 20) / project.levers, hardware.MAX_LEVER_WIDTH))
    margin = int((hardware.WIDTH - project.levers * lever_width)/2)
    radius = int(lever_width/2 - 3) 

    while not setup_finished:
        stage2 = Stage2(hardware, project, step, lever_width, margin, radius)
        stage2.open()

        if stage2.next:
            step += 1
        elif step > 0:
            step -= 1
        if step == project.total_steps:
            setup_finished = True

