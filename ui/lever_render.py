from project import Project
from ui.hardware import Hardware


class LeverRender():

    def __init__(self, hardware : Hardware, project : Project):
        self.hardware = hardware
        self.project = project

        self.H_PAD = 20
        self.L_PAD = 3

        self.lever_width = int(min((hardware.WIDTH - self.H_PAD) / project.levers, hardware.MAX_LEVER_WIDTH))
        self.margin = int((hardware.WIDTH - project.levers * self.lever_width)/2)
        self.radius = int(self.lever_width/2 - self.L_PAD) 


    def refresh_levers(self):
        for l in range(self.project.levers):
            if self.project.get_sequence(self.step)[l] == 1:
                self.set_up(l)
            else:
                self.set_down(l)
        self.hardware.display.update()

    def set_up(self, lever_num):
        self.hardware.display.circle(self.margin + self.lever_width*lever_num + self.radius + self.L_PAD, self.hardware.LEVER_DIST, self.radius)
        self.hardware.display.line(self.margin + self.lever_width*lever_num + self.L_PAD, self.hardware.HEIGHT - self.hardware.LEVER_DIST, self.margin + self.lever_width*lever_num + self.L_PAD + 2*self.radius, self.hardware.HEIGHT - self.hardware.LEVER_DIST)

    def set_down(self, lever_num):
        self.hardware.display.circle(self.margin + self.lever_width*lever_num + self.radius + self.L_PAD, self.hardware.HEIGHT - self.hardware.LEVER_DIST, self.radius)
        self.hardware.display.line(self.margin + self.lever_width*lever_num + self.L_PAD, self.hardware.LEVER_DIST, self.margin + self.lever_width*lever_num + self.L_PAD + 2*self.radius, self.hardware.LEVER_DIST)

    def clear_lever(self, lever_num):
        self.hardware.set_bg_pen()
        self.hardware.display.rectangle(self.margin + self.lever_width*lever_num, self.hardware.LEVER_DIST - self.radius - self.L_PAD, 2*(self.radius+self.L_PAD),  self.hardware.HEIGHT - 2*(self.hardware.LEVER_DIST - self.radius - self.L_PAD))
        self.hardware.set_fg_pen()