# main.py -- put your code here!

from project import Project
from ui.welcome import Welcome
from ui.start import StartMenu
from ui import setup
from ui.hardware import Hardware
import os
import json
from const import project_file, c_step_file

hardware = Hardware()

project = None
if os.path.exists(project_file):
    f = open(project_file)
    project = json.load(f)
    c = open(c_step_file)
    project.current_step = int(c.readline())

welcome = Welcome(hardware)
welcome.open()

start = StartMenu(hardware, project)
start.open()

if start.new_proj:
    project = Project()
    setup.setup(hardware, project)
