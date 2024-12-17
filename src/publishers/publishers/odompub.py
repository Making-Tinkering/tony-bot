import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

import math
import numpy as np # Scientific computing library for Python
 



class OdometryPublisher(Node):
    def __init__(self):
        super().__init__('odometry_publisher')
        self.publisher_ = self.create_publisher(Odometry, 'odom', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.publish_odometry)
        

        self.subscription = self.create_subscription(
                Twist,
                '/cmd_vel',
                self.listener_callback,
                10)
        self.subscription  # prevent unused variable warning
        
        self.linearVel = 0.0
        self.angularVel = 0.0
        #Hardware measurements
        self.baseDistance = 0.3                                     #distance between wheels in metres
        self.baseHalf = self.baseDistance / 2
        self.wheelDiameter = 0.15                                   #diameter of wheel
        self.wheelRadius = self.wheelDiameter / 2
        self.distPerRev = self.wheelDiameter*math.pi                #dist per rev of wheel
        self.encResolution = 4096                                   #resolution of encoder
        self.sumEnc = self.encResolution * 4                        #total pulses per rev of encoder
        self.rateEnc = (2 * math.pi *self.wheelRadius) / self.sumEnc
        self.oldLeftD = 0.0
        self.oldrightD = 0.0
        self.wX = 0.0
        self.wY = 0.0
        self.wTheta = 0.0
        self.get_quaternion_from_euler(0.0,0.0,0.0)

    def listener_callback(self, msg):
        self.linearVel = msg.linear.x
        self.angularVel = msg.angular.z
        #self.get_logger().info(f'I heard: {self.linearVel} and {self.angularVel}')
        self.calculate_odom(0.0,0.0)
        #print(msg)
        
    def get_quaternion_from_euler(self, roll, pitch, yaw):
        self.qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        self.qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        self.qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        self.qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    def calculate_odom(self,leftD,rightD):
        deltaLeftD = self.oldLeftD - leftD
        deltaRightD = self.oldrightD - rightD

        avgD = (deltaLeftD + deltaRightD) / 2
        deltaTheta = (deltaRightD - deltaLeftD) / self.baseDistance
        deltaX =  avgD * math.cos(deltaTheta) 
        deltaY =  avgD * math.sin(deltaTheta)
        
        #Increment Odom
        self.wX += deltaX
        self.wY += deltaY
        self.wTheta += deltaTheta
        self.get_quaternion_from_euler(0.0,0.0,self.wTheta)
        #Update state
        self.oldLeftD = leftD
        self.oldrightD = rightD
        

    def publish_odometry(self):#   , x, y, z, quat_x, quat_y, quat_z, quat_w):
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.child_frame_id = "base_link"
        msg.pose.pose.position.x = self.wX
        msg.pose.pose.position.y = self.wY
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.x = self.qx
        msg.pose.pose.orientation.y = self.qy
        msg.pose.pose.orientation.z = self.qz
        msg.pose.pose.orientation.w = self.qw
        
        msg.twist.twist.linear.x = self.linearVel
        msg.twist.twist.angular.z = self.angularVel
        self.publisher_.publish(msg)
        #print(msg)

def main(args=None):
    rclpy.init(args=args)
    node = OdometryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
