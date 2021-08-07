#!/usr/bin/env python3
import LCD1602
import time

def setup():
	while True:
		LCD1602.init(0x27, 1)	# init(slave address, background light)
		LCD1602.write(0, 0, 'Line 1')
		LCD1602.write(0, 1, 'Line 2')
		time.sleep(2)

def destroy():
	LCD1602.clear()

if __name__ == "__main__":
	try:
		setup()
	except KeyboardInterrupt:
		destroy()

