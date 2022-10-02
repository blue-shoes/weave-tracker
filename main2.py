# main.py -- put your code here!

from project import Project
from ui.welcome import Welcome
from ui.start import StartMenu
from ui import setup
from ui.hardware import Hardware
import os
import json

project_file = "/flash/project.json"

hardware = Hardware()

project = None
#if os.path.exists(project_file):
#    f = open(project_file)
#    project = json.load(f)

welcome = Welcome(hardware)
welcome.open()

start = StartMenu(hardware, project)
start.open()

if start.new_proj:
    project = Project()
    setup.setup()
