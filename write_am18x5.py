import smbus as smbus
from datetime import time, date, datetime
import os

bus = smbus.SMBus(1)
address = 0x69

def dec2bcd(databyte):
	units = databyte % 10
	tens = databyte - units
	tens = tens / 10
	tens = tens << 4
	result = tens + units
	return result

# Get the system time
dt = datetime.utcnow()
day = dt.day
month = dt.month
year = dt.year
hours = dt.hour
minutes = dt.minute
seconds = dt.second

# Set the century flag in the status register if year is > 2000
status = bus.read_byte_data(address,0x0F)
if year >= 2000:
	status = status | 0x80
	year = year - 2000
else:
	status = status & 0x7F
        year = year - 1900
bus.write_byte_data(address,0x0F,status)

# Set the write to RTC flag in the control 1 register
control1 = 0x1
bus.write_byte_data(address,0x10,control1)

# Copy the date and time into binary coded decimal bytes
timedata = []
timedata.append(0)
timedata.append(dec2bcd(seconds))
timedata.append(dec2bcd(minutes))
timedata.append(dec2bcd(hours))
timedata.append(dec2bcd(day))
timedata.append(dec2bcd(month))
timedata.append(dec2bcd(year))

# Write the time and date to the RTC
bus.write_i2c_block_data(address,0,timedata)

# Key register needs to be written with value 0x9D in order to access the trickle register
bus.write_byte_data(address,0x1F,0x9D)

# Set the trickle register to charge the supercapacitor
# TCS field = 0x1010, Diode field = 0x1 (3V), ROUT field = 0x1 (3kohms)
bus.write_byte_data(address,0x20,0xa5)
