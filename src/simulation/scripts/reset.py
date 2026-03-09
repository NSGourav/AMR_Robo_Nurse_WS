#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseWithCovarianceStamped
import tf_transformations
from std_srvs.srv import Trigger  

class ResetClient(Node):
    def __init__(self):
        super().__init__('reset_imu_odom_client')

        # Create clients for both services
        # self.imu_client = self.create_client(Trigger, '/reset_imu')
        # self.odom_client = self.create_client(Trigger, '/reset_odom')

        self.nav = BasicNavigator()
        self.nav.waitUntilNav2Active() 

        # #Create a publisher for /initialpose
        self.initial_pose_pub = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
        self.timer = self.create_timer(1.0, self.publish_pose)  # Publish pose once

    def publish_pose(self):
        """Publishes initial pose to /initialpose"""
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, 3.14)
        
        initial_pose = PoseWithCovarianceStamped()
        initial_pose.header.stamp = self.get_clock().now().to_msg()
        initial_pose.header.frame_id = "map"

        initial_pose.pose.pose.position.x = 0.0
        initial_pose.pose.pose.position.y = 0.0
        initial_pose.pose.pose.position.z = 0.0  

        initial_pose.pose.pose.orientation.x = q_x
        initial_pose.pose.pose.orientation.y = q_y
        initial_pose.pose.pose.orientation.z = q_z
        initial_pose.pose.pose.orientation.w = q_w

        # Set covariance (uncertainty in position & orientation)
        initial_pose.pose.covariance = [
            0.25, 0.0,  0.0,  0.0,  0.0,  0.0,
            0.0,  0.25, 0.0,  0.0,  0.0,  0.0,
            0.0,  0.0,  0.25, 0.0,  0.0,  0.0,
            0.0,  0.0,  0.0,  0.25, 0.0,  0.0,
            0.0,  0.0,  0.0,  0.0,  0.25, 0.0,
            0.0,  0.0,  0.0,  0.0,  0.0,  0.068
        ]


        self.initial_pose_pub.publish(initial_pose)
        self.get_logger().info("Published Initial Pose Estimate")
        
        self.timer.cancel()  # Stop publishing after one time

    def send_request(self, client, service_name):
        """Sends a request to a service and handles the response"""
        req = Trigger.Request()
        future = client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f'{service_name} -> Success: {future.result().success}, Message: {future.result().message}')
        else:
            self.get_logger().error(f'Failed to call service {service_name}')

    def reset_all(self):
        """Resets IMU and odometry"""
        self.publish_pose()
        # self.send_request(self.imu_client, "/reset_imu")
        # self.send_request(self.odom_client, "/reset_odom")

def main():
    rclpy.init()
    reset_client = ResetClient()
    reset_client.reset_all()
    reset_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()