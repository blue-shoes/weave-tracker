from ui.button_render import TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
import time
from ui import button_render, hardware
import project



class Stage1():

    steps = True
    
    def __init__(self, hardware : hardware.Hardware, project : project.Project):
        self.hardware = hardware
        self.project = project
        self.up_btn = self.hardware.button_b
        self.down_btn = self.hardware.button_y
        self.back_btn = self.hardware.button_a
        self.next_btn = self.hardware.button_x

    def open(self):
        self.hardware.set_bg_pen()
        self.hardware.display.clear()
        self.hardware.set_fg_pen()
        self.hardware.place_text("Steps", 1.0, int(self.hardware.WIDTH/4), int(self.hardware.HEIGHT/3))
        self.hardware.place_text("Levers", 1.0, int(3*self.hardware.WIDTH/4), int(self.hardware.HEIGHT/3))

        width = max(self.hardware.display.measure_text("Increase", scale=0.5), self.hardware.display.measure_text("Decrease", scale=0.5))
        button_render.place_button(self.hardware, "Back", width, self.hardware.BTN_HEIGHT, TOP_LEFT)
        button_render.place_button(self.hardware, "Next", width, self.hardware.BTN_HEIGHT, TOP_RIGHT)
        button_render.place_button(self.hardware, "Increase", width, self.hardware.BTN_HEIGHT, BOTTOM_LEFT)
        button_render.place_button(self.hardware, "Decrease", width, self.hardware.BTN_HEIGHT, BOTTOM_RIGHT)

        self.update_display()

        finished = False
        while not finished:
            time.sleep(0.1)
            if self.up_btn.read():
                if self.steps:
                    self.project.total_steps = self.project.total_steps+1
                    self.update_steps()
                else:
                    self.project.levers = self.project.levers+1
                    self.update_levers()
            if self.down_btn.read():
                if self.steps:
                    if self.project.total_steps > 1:
                        self.project.total_steps = self.project.total_steps-1
                        self.update_steps()
                else:
                    if self.project.levers > 1:
                        self.project.levers = self.project.levers-1
                        self.update_levers()
            if self.next_btn.read():
                if self.steps:
                    self.steps = False
                else:
                    finished = True
            if self.back_btn.read():
                if not self.steps:
                    self.steps = True
    
    def update_display(self):
        self.update_steps()
        self.update_levers()
    
    def update_steps(self):
        self.hardware.set_bg_pen()
        self.hardware.display.rectangle(int(self.hardware.WIDTH/8), int(self.hardware.HEIGHT/2), int(self.hardware.WIDTH/4), int(self.hardware.HEIGHT/3))
        self.hardware.set_fg_pen()
        self.hardware.place_text(str(self.project.total_steps), 1.0, int(self.hardware.WIDTH/4), int(2*self.hardware.HEIGHT/3))
        self.hardware.display.update()
    
    def update_levers(self):
        self.hardware.set_bg_pen()
        self.hardware.display.rectangle(int(5*self.hardware.WIDTH/8), int(self.hardware.HEIGHT/2), int(self.hardware.WIDTH/4), int(self.hardware.HEIGHT/3))
        self.hardware.set_fg_pen()
        self.hardware.place_text(str(self.project.levers), 1.0, int(3*self.hardware.WIDTH/4), int(2*self.hardware.HEIGHT/3))
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
        self.up_btn = self.hardware.button_b
        self.down_btn = self.hardware.button_y
        self.back_btn = self.hardware.button_a
        self.next_btn = self.hardware.button_x

    def open(self):
        self.next = False
        self.hardware.set_bg_pen()
        self.hardware.display.clear()
        self.hardware.set_fg_pen()
        self.hardware.place_text(f"Step {self.step+1}/{self.project.total_steps}", 0.75, int(self.hardware.WIDTH/2), self.hardware.HEIGHT - 20)
        self.hardware.place_text("Set Lever positions", 0.75, int(self.hardware.WIDTH/2), 20)
        width = max(self.hardware.display.measure_text("Increase", scale=0.5), self.hardware.display.measure_text("Decrease", scale=0.5))
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

        elapsed = 0
        exit = False
        while not exit:
            time.sleep(0.1)
            elapsed += 1
            if self.up_btn.read():
                if self.project.get_sequence(self.step)[self.lever] != 1:
                    self.project.get_sequence(self.step)[self.lever] = 1
                    self.clear_lever(self.lever)
                    self.set_up(self.lever)
                    elapsed = 0
            if self.down_btn.read():
                if self.project.get_sequence(self.step)[self.lever] != 0:
                    self.project.get_sequence(self.step)[self.lever] = 0
                    self.clear_lever(self.lever)
                    self.set_down(self.lever)
                    elapsed = 0
            if self.next_btn.read():
                self.lever = self.lever + 1
                if self.lever == self.project.levers:
                    exit = True
                    self.next = True
                elapsed = 0
            if self.back_btn.read():
                if self.lever == 0:
                    exit = True
                else:
                    self.lever = self.lever - 1
                elapsed = 0
            if elapsed % 5 == 0:
                if elapsed % 2 == 0:
                    # Blink on
                    if self.project.get_sequence(self.step)[self.lever] == 1:
                        self.set_up(self.lever)
                    else:
                        self.set_down(self.lever)
                else:
                    # Blink off
                    self.hardware.set_bg_pen()
                    if self.project.get_sequence(self.step)[self.lever] == 1:
                        self.hardware.display.rectangle(self.margin + self.lever_width*self.lever, self.hardware.LEVER_DIST, 2*(self.radius+3), 2*(self.radius+3))
                    else:
                        self.hardware.display.rectangle(self.margin + self.lever_width*self.lever, self.hardware.HEIGHT - self.hardware.LEVER_DIST - 2*(self.radius+3), 2*(self.radius+3), 2*(self.radius+3))
                    self.hardware.set_fg_pen()
                self.hardware.display.update()
            
    def set_up(self, lever_num):
        self.hardware.display.circle(self.margin + self.lever_width*lever_num + self.radius + 3, self.hardware.LEVER_DIST, self.radius)
        self.hardware.display.line(self.margin + self.lever_width*lever_num + 3, self.hardware.HEIGHT - self.hardware.LEVER_DIST, self.margin + self.lever_width*lever_num + 3 + 2*self.radius, self.hardware.LEVER_DIST)
    
    def set_down(self, lever_num):
        self.hardware.display.circle(self.margin + self.lever_width*lever_num + self.radius + 3, self.hardware.HEIGHT - self.hardware.LEVER_DIST, self.radius)
        self.hardware.display.line(self.margin + self.lever_width*lever_num + 3, self.hardware.LEVER_DIST, self.margin + self.lever_width*lever_num + 3 + 2*self.radius, self.hardware.HEIGHT - self.hardware.LEVER_DIST)

    def clear_lever(self, lever_num):
        self.hardware.set_bg_pen()
        self.hardware.display.rectangle(self.margin + self.lever_width*lever_num, self.hardware.LEVER_DIST - self.radius, 2*(self.radius+3), self.hardware.HEIGHT - 2*(self.hardware.LEVER_DIST))
        self.hardware.set_fg_pen()

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

