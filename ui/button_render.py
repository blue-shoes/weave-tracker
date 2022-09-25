from ..main import display, WIDTH, HEIGHT
from enum import Enum

class ButtonEnum(Enum):
    TOP_LEFT = 1,
    TOP_RIGHT = 2,
    BOTTOM_LEFT = 3,
    BOTTOM_RIGHT = 4

def place_button(text, width, height, button_placement, width_pad=2, height_pad=2):
    if button_placement == ButtonEnum.TOP_LEFT:
        display.text(text, width/2 + width_pad, HEIGHT - (height/2 + height_pad))
        display.line(0, HEIGHT-(height + 2*height_pad), (width + 2*width_pad), HEIGHT-(height + 2*height_pad))
        display.line(width + 2*width_pad, HEIGHT, width + 2(width_pad), HEIGHT-(height + 2*height_pad))
    elif button_placement == ButtonEnum.TOP_RIGHT:
        display.text(text, WIDTH - (width/2 + width_pad), HEIGHT - (height/2 + height_pad))
        display.line(WIDTH, HEIGHT-(height + 2*height_pad), WIDTH - (width + 2*width_pad), HEIGHT-(height + 2*height_pad))
        display.line(WIDTH - (width + 2*width_pad), HEIGHT, WIDTH - (width + 2(width_pad)), HEIGHT-(height + 2*height_pad))
    elif button_placement == ButtonEnum.BOTTOM_LEFT:
        display.text(text, width/2 + width_pad, (height/2 + height_pad))
        display.line(0, (height + 2*height_pad), (width + 2*width_pad), (height + 2*height_pad))
        display.line(width + 2*width_pad, 0, width + 2(width_pad), (height + 2*height_pad))
    elif button_placement == ButtonEnum.BOTTOM_RIGHT:
        display.text(text, WIDTH - (width/2 + width_pad), (height/2 + height_pad))
        display.line(WIDTH, (height + 2*height_pad), WIDTH - (width + 2*width_pad), (height + 2*height_pad))
        display.line(WIDTH - (width + 2*width_pad), 0, WIDTH - (width + 2(width_pad)), (height + 2*height_pad))
