TOP_LEFT = 1,
TOP_RIGHT = 2,
BOTTOM_LEFT = 3,
BOTTOM_RIGHT = 4

def place_button(hardware, text, width, height, button_placement, width_pad=2, height_pad=2):
    
    if button_placement == TOP_LEFT:
        hardware.display.text(text, width_pad, int(height/2 + height_pad), scale=0.5)
        hardware.display.line(width_pad, (height + 2*height_pad), (width + 2*width_pad), (height + 2*height_pad))
        hardware.display.line(width + 2*width_pad, 0, width + 2*(width_pad), (height + 2*height_pad))
    elif button_placement == TOP_RIGHT:
        hardware.display.text(text, hardware.WIDTH - int(width + width_pad), int(height/2 + height_pad), scale=0.5)
        hardware.display.line(hardware.WIDTH, (height + 2*height_pad), hardware.WIDTH - (width + 2*width_pad), (height + 2*height_pad))
        hardware.display.line(hardware.WIDTH - (width + 2*width_pad), 0, hardware.WIDTH - (width + 2*(width_pad)), (height + 2*height_pad))
    elif button_placement == BOTTOM_LEFT:
        hardware.display.text(text, width_pad, hardware.HEIGHT - int(height/2 + height_pad), scale=0.5)
        hardware.display.line(width_pad, hardware.HEIGHT - (height + 2*height_pad), (width + 2*width_pad), hardware.HEIGHT-(height + 2*height_pad))
        hardware.display.line(width + 2*width_pad, hardware.HEIGHT, width + 2*(width_pad), hardware.HEIGHT-(height + 2*height_pad))
    elif button_placement == BOTTOM_RIGHT:
        hardware.display.text(text, hardware.WIDTH - int(width + width_pad), hardware.HEIGHT-int(height/2 + height_pad), scale=0.5)
        hardware.display.line(hardware.WIDTH, hardware.HEIGHT-(height + 2*height_pad), hardware.WIDTH - (width + 2*width_pad), hardware.HEIGHT-(height + 2*height_pad))
        hardware.display.line(hardware.WIDTH - (width + 2*width_pad), hardware.HEIGHT, hardware.WIDTH - (width + 2*(width_pad)), hardware.HEIGHT-(height + 2*height_pad))
