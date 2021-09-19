from m5stack import *
from m5stack_ui import *
from uiflow import *
from IoTcloud.AWS import AWS
import wifiCfg
import machine
import time
import nvs
import json

import unit

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xa5a5a5)
heart_5 = unit.get(unit.HEART, unit.PORTA)
ncir_3 = unit.get(unit.NCIR, (21,22))
env3_0 = unit.get(unit.ENV3, (21,22))


value_read = None
temp_list = None
spo2_list = None
heart_list = None
DataJson = None
device_id = None

wifiCfg.autoConnect(lcdShow=True)
im_heartrate = M5Img("res/heartrate.png", x=16, y=50, parent=None)
im_temperature = M5Img("res/temperature.png", x=180, y=50, parent=None)
im_spo2 = M5Img("res/spo2.png", x=99, y=50, parent=None)
lb_title = M5Label('DMHC v1.0 ', x=8, y=6, color=0x074302, font=FONT_MONT_20, parent=None)
lb_status = M5Label('Init device...', x=10, y=210, color=0x061fbb, font=FONT_MONT_18, parent=None)
lb_heartrate = M5Label('0', x=26, y=113, color=0x000, font=FONT_MONT_18, parent=None)
lb_spo2 = M5Label('0', x=104, y=111, color=0x000, font=FONT_MONT_18, parent=None)
lb_temperature = M5Label('0', x=186, y=113, color=0x000, font=FONT_MONT_18, parent=None)
lb_pressure = M5Label('0', x=253, y=114, color=0x000, font=FONT_MONT_16, parent=None)
lb_time = M5Label('00:00', x=253, y=6, color=0x000, font=FONT_MONT_18, parent=None)
bar0 = M5Bar(x=0, y=151, w=238, h=20, min=0, max=100, bg_c=0x9e9b9b, color=0x078f9c, parent=None)
im_sensor = M5Img("res/hletter.png", x=169, y=2, parent=None)
line0 = M5Line(x1=1, y1=36, x2=320, y2=36, color=0x6c6c6c, width=1, parent=None)
lb_ambienttemp = M5Label('0', x=253, y=140, color=0x000, font=FONT_MONT_16, parent=None)
lb_humidity = M5Label('0', x=253, y=166, color=0x000, font=FONT_MONT_16, parent=None)
line1 = M5Line(x1=237, y1=36, x2=237, y2=200, color=0x6c6c6c, width=1, parent=None)
im_ambient = M5Img("res/ambient.png", x=264, y=50, parent=None)

import math


# Get time from device, format it and show at user interface
def Get_Time():
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  lb_status.set_text('Get time ...')
  lb_time.set_text(str((str((rtc.datetime()[4])) + str(((str(':') + str((rtc.datetime()[5]))))))))

# Paint user interface, get time and environment data
def DMHC_Init():
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  im_sensor.set_hidden(True)
  bar0.set_hidden(True)
  Get_Time()
  lb_status.set_text('Drawing ...')
  im_spo2.set_img_src("res/spo2.png")
  im_heartrate.set_img_src("res/heartrate.png")
  im_temperature.set_img_src("res/temperature.png")
  im_ambient.set_img_src("res/ambient.png")
  lb_spo2.set_align(ALIGN_CENTER, x=0, y=50, ref=im_spo2.obj)
  lb_heartrate.set_align(ALIGN_CENTER, x=0, y=50, ref=im_heartrate.obj)
  lb_temperature.set_align(ALIGN_CENTER, x=0, y=50, ref=im_temperature.obj)
  lcd.rect(0, 200, 320, 40, color=0x666666)
  lcd.rect(1, 201, 318, 38, color=0xcccccc)
  device_id = nvs.read_str('device_id')
  lb_status.set_text(str(device_id))
  Read_ENV3()

# Read from Env III unit temperature, pressure,
# humidity, format values and show at user interface
def Read_ENV3():
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  lb_ambienttemp.set_text(str((str(("%.0f"%((env3_0.temperature)))) + str(' C'))))
  lb_pressure.set_text(str((str(("%.0f"%(((env3_0.pressure) / 1000)))) + str(' kPa'))))
  lb_humidity.set_text(str((str(("%.0f"%((env3_0.humidity)))) + str(' %'))))

# Begin check process activate vibration, play
# wav, RGB leds blink between red and green
def TimeToCheck():
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  lb_status.set_text('Time to check your health')
  speaker.playWAV("res/time-to-check.wav")
  power.setVibrationIntensity(50)
  power.setVibrationEnable(True)
  rgb.setBrightness(100)
  for count in range(6):
    rgb.setColorFrom(6 , 10 ,0xff0000)
    wait_ms(250)
    rgb.setColorFrom(6 , 10 ,0x000000)
    rgb.setColorFrom(1 , 5 ,0x009900)
    wait_ms(250)
    rgb.setColorFrom(1 , 5 ,0x000000)
  power.setVibrationEnable(False)

# Read data from heart and temperature unit sensor and put them at three value lists
def Read_Data():
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  im_sensor.set_hidden(False)
  im_sensor.set_img_src("res/hletter.png")
  lb_status.set_text('Please put your finger at H sensor')
  speaker.playWAV("res/put-finger-h-sensor.wav")
  bar0.set_hidden(False)
  bar0.set_value(0)
  heart_list = []
  spo2_list = []
  for count2 in range(10):
    rgb.setColorFrom(6 , 10 ,0xff0000)
    wait_ms(250)
    rgb.setColorFrom(1 , 5 ,0xff0000)
    wait_ms(250)
    rgb.setColorFrom(6 , 10 ,0x000000)
    wait_ms(250)
    rgb.setColorFrom(1 , 5 ,0x000000)
    bar0.set_value(((bar0.get_value()) + 10))
    _thread.stack_size(0)
    Read_HeartRate_SpO2()
  heart_5.setLedCurrent(0x00, 0x00)
  im_sensor.set_img_src("res/tletter.png")
  lb_status.set_text('Please put your finger at T sensor')
  speaker.playWAV("res/put-finger-t-sensor.wav")
  bar0.set_value(0)
  temp_list = []
  for count3 in range(10):
    rgb.setColorFrom(6 , 10 ,0x009900)
    wait_ms(250)
    rgb.setColorFrom(1 , 5 ,0x009900)
    wait_ms(250)
    rgb.setColorFrom(6 , 10 ,0x000000)
    wait_ms(250)
    rgb.setColorFrom(1 , 5 ,0x000000)
    bar0.set_value(((bar0.get_value()) + 10))
    _thread.stack_size(0)
    Read_Temperature()

# Read heart rate and spo2 from Heart Unit, put
# values in two lists and show at user interface
def Read_HeartRate_SpO2():
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  heart_5.setLedCurrent(0x04, 0x01)
  heart_5.setMode(0x03)
  value_read = heart_5.getSpO2()
  lb_spo2.set_text(str(value_read))
  spo2_list.append(value_read)
  value_read = heart_5.getHeartRate()
  lb_heartrate.set_text(str(value_read))
  heart_list.append(value_read)
  wait(0.6)

# Indicate that test was completed
def Test_Completed():
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  bar0.set_hidden(True)
  im_sensor.set_hidden(True)
  lb_status.set_text('Test completed')
  speaker.playWAV("res/test-completed.wav")

# Read temperature value from NCIR Unit, put it in a list and show at user interface
def Read_Temperature():
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  value_read = math.ceil(ncir_3.temperature)
  temp_list.append(value_read)
  lb_temperature.set_text(str(value_read))
  wait(0.6)


# Wait from AWS Cloud that call dmhc/reset
# topic to reset device and begin new process
def fun_dmhc_reset_(topic_data):
  global value_read, temp_list, spo2_list, heart_list, DataJson, device_id
  lb_status.set_text(str(topic_data))
  machine.reset()
  pass

# DMHC HOST Probe program v2

DMHC_Init()
TimeToCheck()
Read_Data()
Test_Completed()
lb_status.set_text('Connecting to AWS ...')
_thread.stack_size(0)
# Connect to thing endpoint at AWS IoT Core using MQTT protocol
aws = AWS(things_name='DMHC_HOST_Probe', host='a2i2bsijbyml6j-ats.iot.us-west-2.amazonaws.com', port=8883, keepalive=60, cert_file_path="/flash/res/certificate.pem", private_key_path="/flash/res/private.pem")
aws.subscribe(str('dmhc/reset'), fun_dmhc_reset_)
aws.start()
lb_status.set_text('AWS Connected')
_thread.stack_size(0)
DataJson = {}
# Create a Json with all list data read from sensors and send to AWS cloud
while not not len(temp_list):
  DataJson['device_id'] = device_id
  DataJson['heartrate'] = heart_list.pop(0)
  DataJson['spo2'] = spo2_list.pop(0)
  DataJson['temperature'] = temp_list.pop(0)
  # Publish to topic dmhc/host_data
  aws.publish(str('dmhc/host_data'),str((json.dumps(DataJson))))
  lb_status.set_text('Sending data to AWS ...')
_thread.stack_size(0)
lb_status.set_text('Waiting for a new request')
