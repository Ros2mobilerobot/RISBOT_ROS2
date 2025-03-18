#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class MapToOdomTFBroadcaster(Node):
    def __init__(self):
        super().__init__('map_to_odom_tf_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.map_to_odom = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'yaw': 0.0}  # Giá trị cố định
        self.timer = self.create_timer(0.1, self.broadcast_transform)  # 10Hz

    def broadcast_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'odom_frame'
        t.transform.translation.x = self.map_to_odom['x']
        t.transform.translation.y = self.map_to_odom['y']
        t.transform.translation.z = self.map_to_odom['z']
        quaternion = self.yaw_to_quaternion(self.map_to_odom['yaw'])
        t.transform.rotation.x, t.transform.rotation.y, t.transform.rotation.z, t.transform.rotation.w = quaternion
        self.tf_broadcaster.sendTransform(t)

    @staticmethod
    def yaw_to_quaternion(yaw):
        import math
        return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))


def main(args=None):
    rclpy.init(args=args)
    node = MapToOdomTFBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
