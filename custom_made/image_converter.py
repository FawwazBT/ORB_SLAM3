#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImageConverter:
    def __init__(self):
        # Initialize the CvBridge class for converting between ROS and OpenCV images
        self.bridge = CvBridge()
        
        # Subscribe to the RGB image topic
        self.image_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)
        
        # Publisher for the grayscale image topic
        self.image_pub = rospy.Publisher("/camera/color/image_raw_grayscale", Image, queue_size=10)

    def image_callback(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image (BGR format)
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

            # Convert the BGR image to a grayscale image
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Convert the 8-bit grayscale image to 12-bit by scaling
            gray_image_12bit = (gray_image.astype('uint16') * 16).clip(0, 4095)

            # Convert the 12-bit grayscale OpenCV image back to a ROS Image message
            gray_image_msg = self.bridge.cv2_to_imgmsg(gray_image_12bit, encoding="mono16")

            # Publish the 12-bit grayscale image to the specified topic
            self.image_pub.publish(gray_image_msg)

        except CvBridgeError as e:
            # Log any conversion errors
            rospy.logerr(f"CvBridge Error: {e}")

def main():
    # Initialize the ROS node
    rospy.init_node('image_converter', anonymous=True)
    
    # Create an instance of the ImageConverter class
    ImageConverter()
    
    try:
        # Keep the node running until interrupted
        rospy.spin()
    except KeyboardInterrupt:
        # Log a message when the node is shutting down
        rospy.loginfo("Shutting down")

if __name__ == '__main__':
    # Entry point of the script
    main()
