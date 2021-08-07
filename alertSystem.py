#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import LCD1602

# Set alert color choices
COLORS = [0xFF0000, 0xFFCC00, 0x00FF00 ]

# Set LEDPINS and BUTTONS channels with dictionary
LEDPINS = {'Red':33, 'Green':35, 'Blue':37}
BUTTONS = {'Red':40, 'Yellow':38, 'Normal':36}

def setup():
  global p_R, p_G, p_B, p_S
  #Set BOARD mode and initialize the display
  GPIO.setmode(GPIO.BOARD)
  LCD1602.init(0x27, 1)	

  # Set LED as Output
  for i in LEDPINS:
    GPIO.setup(LEDPINS[i], GPIO.OUT, initial=GPIO.HIGH)

# Set Buttons as Inputs
  for i in BUTTONS:
    GPIO.setup(BUTTONS[i], GPIO.IN)

  # Set all led as pwm channel and frequece to 2KHz
  p_R = GPIO.PWM(LEDPINS['Red'], 2000)
  p_G = GPIO.PWM(LEDPINS['Green'], 1000)
  p_B = GPIO.PWM(LEDPINS['Blue'], 1000)

  # Set all begin with value 0
  p_R.start(0)
  p_G.start(0)
  p_B.start(0)

def ledOff():
  # Stop all pins
  p_R.stop()
  p_G.stop()
  p_B.stop()


def MAP(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setRGB(color):
  # Split the color hex values into Red Green and Blue values
  R_val = (color & 0xFF0000) >> 16
  G_val = (color & 0x00FF00) >> 8
  B_val = (color & 0x0000FF) >> 0

  R_val = MAP(R_val, 0, 255, 0, 5)
  G_val = MAP(G_val, 0, 255, 0, 5)
  B_val = MAP(B_val, 0, 255, 0, 5)

  # Set Brightness of each of the RGB LED color brighness
  p_R.ChangeDutyCycle(R_val)
  p_G.ChangeDutyCycle(G_val)
  p_B.ChangeDutyCycle(B_val)

def setColorAndMessage(color, line1, line2):
  setRGB(color)
  LCD1602.clear()
  LCD1602.write(0, 0, line1)
  LCD1602.write(0, 1, line2)
  time.sleep(0.1)

def setAlert(state):
  if state == 'Red':
    print ("RED ALERT")
    setColorAndMessage(COLORS[0], 'ALERT', 'Condition RED')
  
  if state == 'Yellow':
    print ("Yellow Alert")
    setColorAndMessage(COLORS[1], 'ALERT', 'Condition Yellow')

  if state == 'Normal':
    print ("Systems Normal")
    setColorAndMessage(COLORS[2], 'Normal', 'Systems Online')

def main():
  # I don't know why this loop doesn't work
  # for i in BUTTONS:
  #   GPIO.add_event_detect(BUTTONS[i], GPIO.FALLING, callback=lambda x: setAlert(i))

  GPIO.add_event_detect(BUTTONS["Red"], GPIO.FALLING, callback=lambda x: setAlert("Red"))
  GPIO.add_event_detect(BUTTONS["Yellow"], GPIO.FALLING, callback=lambda x: setAlert("Yellow"))
  GPIO.add_event_detect(BUTTONS["Normal"], GPIO.FALLING, callback=lambda x: setAlert("Normal"))
  
  # Set the initial state
  setAlert("Normal")

  while True:
    # Do nothing but wait
    time.sleep(1)

def destroy():
  ledOff()
  GPIO.cleanup()
  LCD1602.clear()

if __name__ == '__main__':
  setup()
  try:
    main()
  except KeyboardInterrupt:
    destroy()
