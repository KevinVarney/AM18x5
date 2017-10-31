import smbus as smbus
from datetime import time, date, datetime
import os

bus = smbus.SMBus(1)
address = 0x69

def bcd2dec(databyte):
	tens = databyte & 0xF0
	tens = tens >> 4
	tens = tens * 10
	units = databyte & 0x0F
	result = tens + units
	return result

# Read the time from the RTC
hundredths = bcd2dec(bus.read_byte_data(address,0x00))
seconds = bcd2dec(bus.read_byte_data(address,0x01))
minutes = bcd2dec(bus.read_byte_data(address,0x02))
hours = bus.read_byte_data(address,0x03)
date = bcd2dec(bus.read_byte_data(address,0x04))
month = bcd2dec(bus.read_byte_data(address,0x05))
year = bcd2dec(bus.read_byte_data(address,0x06))

# If the 12/24 flag is clear then hours register works in 24 hour mode
control1 = bus.read_byte_data(address,0x10)
if control1 & 0x40:
	hours = hours & 0x1F
else:
	hours = hours & 0x3F
hours = bcd2dec(hours)

# If the century flag is set then it's the 21st century
status = bus.read_byte_data(address,0x0F)
if status & 0x80:
	year = year + 2000
else:
	year = year + 1900

# Format the command string for setting the system time
set_date_string = "timedatectl set-time '"
dt = datetime(year,month,date,hours,minutes,seconds)
time_string = "{:%Y-%m-%d %H:%M:%S}'".format(dt)
cmd_string = set_date_string + time_string
print cmd_string

# Set system time
os.system(cmd_string)
