#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int64MultiArray

import minimalmodbus
import serial


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('encoder_publisher')
        self.encoderA = minimalmodbus.Instrument('/dev/ttyUSB0', 80)  # port name, slave address (in decimal)
        self.encInnit(self.encoderA)
        self.encoderB = minimalmodbus.Instrument('/dev/ttyUSB0', 81)  # port name, slave address (in decimal)
        self.encInnit(self.encoderB)

        self.publisher_ = self.create_publisher(Int64MultiArray, 'topic', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.val = []
        self.i = 0

    def encInnit(self, instrument):
        instrument.serial.baudrate = 9600         # Baud
        instrument.serial.bytesize = 8
        instrument.serial.parity   = serial.PARITY_NONE
        instrument.serial.stopbits = 1
        instrument.serial.timeout  = 0.05          # seconds
        instrument.address                         # this is the slave address number
        instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        instrument.clear_buffers_before_each_transaction = True
        

    def timer_callback(self):
        msg = Int64MultiArray()

        self.val.append(self.encoderA.read_register(17, 0))  # Registernumber, number of decimals
        self.val.append(self.encoderA.read_register(18, 0))  # Registernumber, number of decimals
        self.val.append(self.encoderB.read_register(17, 0))  # Registernumber, number of decimals
        self.val.append(self.encoderB.read_register(18, 0))  # Registernumber, number of decimals
        msg.data = self.val

        print(self.val)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.val = []


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
