from ui.button_render import TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
import time
from ui import button_render, hardware
import project
from ui.lever_render import LeverRender
import json
import os
from const import project_file, c_step_file

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
        elapsed = 0
        while not finished:
            time.sleep(0.1)
            elapsed += 1
            if self.up_btn.read():
                if self.steps:
                    self.project.total_steps = self.project.total_steps+1
                    self.update_steps()
                    elasped = 0
                else:
                    self.project.levers = self.project.levers+1
                    self.update_levers()
                    elapsed = 0
            if self.down_btn.read():
                if self.steps:
                    if self.project.total_steps > 1:
                        self.project.total_steps = self.project.total_steps-1
                        self.update_steps()
                        elapsed = 0
                else:
                    if self.project.levers > 1:
                        self.project.levers = self.project.levers-1
                        self.update_levers()
                        elapsed = 0
            if self.next_btn.read():
                if self.steps:
                    self.steps = False
                    self.update_steps()
                else:
                    finished = True
                elapsed = 0
            if self.back_btn.read():
                if not self.steps:
                    self.steps = True
                    self.update_levers()
                elapsed = 0
            if elapsed % 5 == 0:
                if elapsed % 2 == 0:
                    # Blink on
                    self.hardware.set_fg_pen()
                    if self.steps:
                        self.hardware.place_text(str(self.project.total_steps), 1.0, int(self.hardware.WIDTH/4), int(2*self.hardware.HEIGHT/3))
                    else:
                        self.hardware.place_text(str(self.project.levers), 1.0, int(3*self.hardware.WIDTH/4), int(2*self.hardware.HEIGHT/3))
                else:
                    # Blink off
                    self.hardware.set_bg_pen()
                    if self.steps:
                        self.hardware.display.rectangle(int(self.hardware.WIDTH/8), int(self.hardware.HEIGHT/2), int(self.hardware.WIDTH/4), int(self.hardware.HEIGHT/3))
                    else:
                        self.hardware.display.rectangle(int(5*self.hardware.WIDTH/8), int(self.hardware.HEIGHT/2), int(self.hardware.WIDTH/4), int(self.hardware.HEIGHT/3))
                self.hardware.display.update()

    
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

    def __init__(self, hardware : hardware.Hardware, project : project.Project, lever_renderer : LeverRender, step):
        self.hardware = hardware
        self.project = project
        self.step = step
        self.lever = 0
        self.lev_rend = lever_renderer
        self.up_btn = self.hardware.button_b
        self.down_btn = self.hardware.button_y
        self.back_btn = self.hardware.button_a
        self.next_btn = self.hardware.button_x

        lev_rend = LeverRender(hardware, project)

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

        self.lev_rend.refresh_levers()    

        elapsed = 0
        exit = False
        while not exit:
            time.sleep(0.1)
            elapsed += 1
            if self.up_btn.read():
                if self.project.get_sequence(self.step)[self.lever] != 1:
                    self.project.get_sequence(self.step)[self.lever] = 1
                    self.lev_rend.clear_lever(self.lever)
                    self.lev_rend.set_up(self.lever)
                    elapsed = 0
            if self.down_btn.read():
                if self.project.get_sequence(self.step)[self.lever] != 0:
                    self.project.get_sequence(self.step)[self.lever] = 0
                    self.lev_rend.clear_lever(self.lever)
                    self.lev_rend.set_down(self.lever)
                    elapsed = 0
            if self.next_btn.read():
                self.lev_rend.refresh_levers()
                self.lever = self.lever + 1
                if self.lever == self.project.levers:
                    exit = True
                    self.next = True
                    continue
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
                        self.lev_rend.set_up(self.lever)
                    else:
                        self.lev_rend.set_down(self.lever)
                else:
                    # Blink off
                    self.hardware.set_bg_pen()
                    if self.project.get_sequence(self.step)[self.lever] == 1:
                        self.hardware.display.rectangle(self.lev_rend.margin + self.lev_rend.lever_width*self.lever, self.hardware.LEVER_DIST - self.lev_rend.radius - self.lev_rend.L_PAD, 2*(self.lev_rend.radius+self.lev_rend.L_PAD), 2*(self.lev_rend.radius+self.lev_rend.L_PAD))
                    else:
                        self.hardware.display.rectangle(self.lev_rend.margin + self.lev_rend.lever_width*self.lever, self.hardware.HEIGHT - self.hardware.LEVER_DIST - self.lev_rend.radius-self.lev_rend.L_PAD, 2*(self.lev_rend.radius+self.lev_rend.L_PAD), 2*(self.lev_rend.radius+self.lev_rend.L_PAD))
                    self.hardware.set_fg_pen()
                self.hardware.display.update()



class Confirmation():

    def __init__(self, hardware : hardware.Hardware):
        self.hardware = hardware
        self.back_btn = self.hardware.button_b
        self.start_proj = self.hardware.button_y
    
    def open(self):
        # Main display
        self.hardware.set_bg_pen()
        self.hardware.display.clear()
        self.hardware.set_fg_pen()
        self.hardware.place_text("Start Project?", 1.0, int(self.hardware.WIDTH/2), int(self.hardware.HEIGHT/2))
        width = self.hardware.display.measure_text("Start", scale=0.5)
        button_render.place_button(self.hardware, "Back", width, self.hardware.BTN_HEIGHT, BOTTOM_LEFT)
        button_render.place_button(self.hardware, "Start", width, self.hardware.BTN_HEIGHT, BOTTOM_RIGHT)
        finished = False

        self.hardware.display.update()

        while not finished:
            time.sleep(0.1)
            if self.back_btn.read():
                return False
            if self.start_proj.read():
                return True

def setup(hardware : hardware.Hardware, project :project.Project):
    stage1 = Stage1(hardware, project)
    stage1.open()

    project.initialize()

    setup_finished = False
    step = 0

    lev_rend = LeverRender(hardware, project)

    while not setup_finished:
        stage2 = Stage2(hardware, project, lev_rend, step)
        stage2.open()

        if stage2.next:
            step += 1
        elif step > 0:
            step -= 1
        if step == project.total_steps:
            confirm = Confirmation(hardware)
            setup_finished = confirm.open()
            if not setup_finished:
                step -= 1

    # Save project file
    project.current_step = 0
    if not os.path.exists('/data'):
        os.mkdir('/data')
    with open(project_file, 'w') as json_file:
        json_file.write(json.dump(project))
    with open(c_step_file, 'w') as step_file:
        step_file.write(str(project.current_step))