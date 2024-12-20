import minimalmodbus
import serial



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

def val(instrument):
    val = []
    val.append(encoderA.read_register(17, 0))  # Registernumber, number of decimals
    val.append(encoderA.read_register(18, 0))  # Registernumber, number of decimals
    val.append(encoderB.read_register(17, 0))  # Registernumber, number of decimals
    val.append(encoderB.read_register(18, 0))  # Registernumber, number of decimals
    print(val)

def read():
	for i in range(0,32):
		print(f'{hex(i)} : {encoderA.read_register(i,0)}	{encoderB.read_register(i,0)}')

val()

#read()


# Unlock command

def unlock(instrument):
    unlock_register = 0x0069
    unlock_value = 0xB588
    instrument.write_register(unlock_register, unlock_value, functioncode=6)
    print("Encoder unlocked successfully.")

#Step 1: set angle to 0
def angle(instrument):
    angle_register = 0x0011
    angle_value = 0x0000  # Value for 0°
    instrument.write_register(angle_register, angle_value, functioncode=6)
    print("Angle set to 0° successfully.")


# Step 2: Write 0 to the revolutions register
def rev(instrument):
    revolutions_register = 0x0012
    revolutions_value = 0x0000 # Set revolutions to 0 
	    
    read_revolutions = instrument.read_register(revolutions_register, functioncode=3) 
    print(f"Revolutions value read back: {read_revolutions}")
    instrument.write_register(revolutions_register, revolutions_value, functioncode=6) 
    print("Revolutions set to 0 successfully.")

def all(instrument):
    unlock(instrument)
    angle(instrument)
    rev(instrument)


all(encoderA)
all(encoderB)
val()
