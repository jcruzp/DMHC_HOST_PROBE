from m5stack import *
from m5stack_ui import *
from uiflow import *
import nvs

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x9fb5c2)





label1 = M5Label('Saved ID:', x=13, y=30, color=0x0816de, font=FONT_MONT_18, parent=None)
label0 = M5Label('Text', x=105, y=30, color=0xf40909, font=FONT_MONT_18, parent=None)


nvs.write(str('device_id'), 'JCruz')
label0.set_text(str(nvs.read_str('device_id')))