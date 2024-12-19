#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray

import minimalmodbus
import serial


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('encoder_publisher')
    
        self.baseLength = 0.2 
        
        self.encoderA = minimalmodbus.Instrument('/dev/ttyUSB0', 80)  # port name, slave address (in decimal)
        self.encInnit(self.encoderA)
        self.encoderB = minimalmodbus.Instrument('/dev/ttyUSB0', 81)  # port name, slave address (in decimal)
        self.encInnit(self.encoderB)

        self.publisher_ = self.create_publisher(Float64MultiArray, 'encoder', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    

    def encInnit(self, instrument):
        instrument.serial.baudrate = 9600         # Baud
        instrument.serial.bytesize = 8
        instrument.serial.parity   = serial.PARITY_NONE
        instrument.serial.stopbits = 1
        instrument.serial.timeout  = 0.05          # seconds
        instrument.address                         # this is the slave address number
        instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        instrument.clear_buffers_before_each_transaction = True
        self.resetEnc(instrument)
        


    def resetEnc(self, instrument):
        unlock_register = 0x0069
        unlock_value = 0xB588
        instrument.write_register(unlock_register, unlock_value, functioncode=6)
        print("Encoder unlocked successfully.")

        angle_register = 0x0011
        angle_value = 0x0010  # Value for 0°
        instrument.write_register(angle_register, angle_value, functioncode=6) 
        print('Angle successfully set to 0')
        print(instrument.read_register(angle_register, functioncode=3))
        revolutions_register = 0x0012
        revolutions_value = 0x0000 # Set revolutions to 0 
        instrument.write_register(revolutions_register, revolutions_value, functioncode=6) 
        print("Revolutions set to 0 successfully.")
        read_revolutions = instrument.read_register(revolutions_register, functioncode=3) 
        print(f"Revolutions value read back: {read_revolutions}")




    def writeEnc(self, instrument, regName, register, payload):
        unlock_register = 0x0069
        unlock_value = 0xB588
        instrument.write_register(unlock_register, unlock_value, functioncode=6)
        print("Encoder unlocked successfully.")

        instrument.write_register(register, payload, functioncode=6) 
        print(instrument.read_register(register, functioncode=3))

    def encToAngle(self, angle_raw, revolutions):
        angle = angle_raw * 360 / 32768 # Convert raw value to degrees #         
        return ((angle / 360) + revolutions) * self.baseLength


    def calDistance(self):
        val = []
        #EncoderA
        angleA = self.encoderA.read_register(17, 0)
        revA = self.encoderA.read_register(18, 0)
        val.append(float(angleA)) 
        val.append(float(revA))
        val.append(self.encToAngle(angleA, revA))
        #EncoderB
        angleB = self.encoderB.read_register(17, 0)
        revB = self.encoderB.read_register(18, 0)
        val.append(float(angleB)) 
        val.append(float(revB))  
        val.append(self.encToAngle(angleB, revB))
        return val

    def timer_callback(self):
        msg = Float64MultiArray()

        msg.data = self.calDistance()

        print(msg.data)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)



def main(args=None):
    rclpy.init(args=args)

    encoder_publisher = MinimalPublisher()

    rclpy.spin(encoder_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    encoder_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
