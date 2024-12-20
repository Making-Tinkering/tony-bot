import minimalmodbus
import serial
import time
val =[]

def encInnit(instrument):
    instrument.serial.baudrate = 9600         # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 0.05          # seconds
    instrument.address                         # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    instrument.clear_buffers_before_each_transaction = True


encoderA = minimalmodbus.Instrument('/dev/ttyUSB0', 80)  # port name, slave address (in decimal)
encInnit(encoderA)
encoderB = minimalmodbus.Instrument('/dev/ttyUSB0', 81)  # port name, slave address (in decimal)
encInnit(encoderB)

val.append(encoderA.read_register(17, 0, signed=True))  # Registernumber, number of decimals
val.append(encoderA.read_register(18, 0, signed=True))  # Registernumber, number of decimals
val.append(encoderB.read_register(17, 0, signed=True))  # Registernumber, number of decimals
val.append(encoderB.read_register(18, 0, signed=True))  # Registernumber, number of decimals
def read():
        for i in range(0,32):
                print(f'{hex(i)} : {encoderA.read_register(i,0)}        {encoderB.read_register(i,0)}')

print(val)

#read()


x = encoderB.read_register(17,0, signed=True)
print(type(x))
print(x)

for i in range(0,20):
	val.append(encoderA.read_register(17, 0, signed=True))  # Registernumber, number of decimals
	val.append(encoderA.read_register(18, 0, signed=True))  # Registernumber, number of decimals
	val.append(encoderB.read_register(17, 0, signed=True))  # Registernumber, number of decimals
	val.append(encoderB.read_register(18, 0, signed=True))  # Registernumber, number of decimals

	print(val)
	val = []
	time.sleep(0.2)
