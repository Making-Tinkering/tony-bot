#!/bin/python3


import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import serial
import time 

 


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('motor_subscriber')
        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1) 
        print('\nStatus -> ',self.arduino)

        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('LINEAR: "%s"' % msg.linear)
        self.get_logger().info('ANGULAR: "%s"' %msg.angular)
        
        self.linearVel = msg.linear.x        
        self.angularVel = msg.angular.z
        self.instruction = "V"
        self.get_logger().info('linearVel: "%s"' %self.linearVel)
        self.get_logger().info('angularVel: "%s"' %self.angularVel)
        
        self.write_read()

    def write_read(self): 
        self.package = (f'<{self.instruction},{self.linearVel},{self.angularVel}>')
        self.arduino.write(bytes(self.package, 'utf-8')) 
	       #time.sleep(0.05) 
	       #data = arduino.readline() 
        

	       #num = input("Enter a number: ") # Taking input from user 
	       #value = write_read(num) 
        print("gheaga") 
        print(self.package) # printing the value 


def main(args=None):
    
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
