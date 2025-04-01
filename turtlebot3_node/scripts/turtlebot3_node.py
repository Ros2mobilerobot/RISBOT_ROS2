#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial
from geometry_msgs.msg import Twist
import math

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

DISTANCE_WHEEL = 0.5    # Khoảng cách giữa hai bánh xe (m)
DIAMETER_WHEEL = 0.3    # Đường kính bánh xe (m)
WHEEL_RADIUS = 0.150    # Bán kính bánh xe (m)
STEP_PER_REVOLUTION = 800  # Số bước mỗi vòng quay của động cơ

class CmdVelToStep(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_step')
        self.subscription = self.create_subscription(
            Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        self.serial_subscription = self.create_timer(0.1, self.receive_step_feedback)

    def cmd_vel_callback(self, msg):
        linear_velocity = msg.linear.x
        angular_velocity = msg.angular.z

        wheel_right_kinematic = (linear_velocity + angular_velocity * (DISTANCE_WHEEL / 2)) / (DIAMETER_WHEEL / 2)
        wheel_left_kinematic = (linear_velocity - angular_velocity * (DISTANCE_WHEEL / 2)) / (DIAMETER_WHEEL / 2)

        step_right = int(wheel_right_kinematic * STEP_PER_REVOLUTION / (2 * math.pi * WHEEL_RADIUS))
        step_left = int(wheel_left_kinematic * STEP_PER_REVOLUTION / (2 * math.pi * WHEEL_RADIUS))

        send_data = f"{step_right},{step_left}\n"
        ser.write(send_data.encode('utf-8'))

    def receive_step_feedback(self):
        if ser.in_waiting:
            feedback = ser.readline().decode('utf-8').strip()
            self.get_logger().info(f"Received feedback: {feedback}")

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelToStep()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
