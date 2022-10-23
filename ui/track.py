from project import Project
from ui.hardware import Hardware
from ui.lever_render import LeverRender
from ui import button_render
from ui.button_render import TOP_LEFT, TOP_RIGHT
from const import c_step_file
import time

class LeverPage():
    def __init__(self, hardware : Hardware, project : Project, lev_rend : LeverRender):
        self.hardware = hardware
        self.project = project
        self.lev_rend = lev_rend
        self.back_btn = self.hardware.button_a
        self.next_btn = self.hardware.button_x

    def open(self):
        self.next = False
        self.hardware.set_bg_pen()
        self.hardware.display.clear()
        self.hardware.set_fg_pen()
        self.hardware.place_text(f"Step {self.project.current_step+1}/{self.project.total_steps}", 0.75, int(self.hardware.WIDTH/2), self.hardware.HEIGHT - 20)
        width = max(self.hardware.display.measure_text("Back", scale=0.5), self.hardware.display.measure_text("Next", scale=0.5))
        button_render.place_button(self.hardware, "Back", width, self.hardware.BTN_HEIGHT, TOP_LEFT)
        button_render.place_button(self.hardware, "Next", width, self.hardware.BTN_HEIGHT, TOP_RIGHT)

        self.lev_rend.refresh_levers(self.project.current_step)

        change_page = False
        while not change_page:
            time.sleep(0.1)
            if self.next_btn.read():
                self.next = True
                change_page = True
            if self.back_btn.read():
                self.next = False
                change_page = True


def run(hardware : Hardware, project : Project):
    lev_rend = LeverRender(hardware, project)
    while True:
        page = LeverPage(hardware, project, lev_rend)
        page.open()

        if page.next:
            project.current_step += 1
            if project.current_step == project.total_steps:
                project.current_step  = 0
        else:
            project.current_step -= 1
            if project.current_step < 0:
                project.current_step = project.total_steps - 1
        
        # Save current step for reopening project
        with open(c_step_file, 'w') as step_file:
            step_file.write(str(project.current_step))
        