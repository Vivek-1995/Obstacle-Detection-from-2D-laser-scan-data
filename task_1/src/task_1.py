#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
from custom_message.msg import LateralDistance          # importing the custom message created for the left and right lateral distances
import math

front = 0.0                   # variable to store front distance at 0 degree
right = 0.0                   # variable to store distance at -90 degree
left = 0.0                    # variable to store distance at +90 degree
lateral_dist_ = 0.0           # variable to store the total lateral distance
sp = 0.0                      # variable to store start point of obstacles
ep = 0.0                      # variable to store end point of obstacles
rang = []                     # List to store the range of the Laser Scan
region = []                   # List to store the index value in rang list whose distance is less than 50 cm/ 0.5m
angle_list = []               # list to store the angle range of the laser scan data from -118 degree to 118 degree
front_msg = Float32()         # Create a variable to store front distance data of type Float32()
lateral_dist_msg = LateralDistance() # Create a variable to store the left and right lateral distances of type LateralDistance()
left_dist = 0.0               # variable to store the left distance
right_dist = 0.0              # variable to store the right distance

# callback function used to get the data from /scan topic Subscriber

def callback_laser(msg):
    global front, lateral_dist_,rang,left_dist, right_dist
    rang = msg.ranges               # storing ranges value to rang list
    front = msg.ranges[472]         # assigning the value at 0 degree in the range at 472 index
    left_dist= (msg.ranges[111])    # assigning the element with index value 111 to the left_dist
    right_dist = (msg.ranges[832])  # assigning the element with index value 832 to the right_dist

def main():
    # initiate the node 'scan_value'
    rospy.init_node('scan_value')   # initiating the scan_value node

    # Handle to publish the front distance to /front_distance topic
    front_pub = rospy.Publisher('front_distance', Float32, queue_size = 10)


    # Handle to publish the left and right distance on /seperate_lateral_distance using the LateralDistance custom message
    lateral_pub = rospy.Publisher('lateral_distances', LateralDistance, queue_size = 10)

    # Subscriber reads  message type LaserScan from /scan topic and passes them as an argument to callback_laser
    sub = rospy.Subscriber('/scan', LaserScan, callback_laser)
    rate= rospy.Rate(2) # frequency set to subscribe and publish to the topics

    while not rospy.is_shutdown():
        front_msg.data = front              # assigning the front value to the variable front_msg.data
        lateral_dist_msg.left_distance = left_dist
        lateral_dist_msg.right_distance = right_dist
        front_pub.publish(front_msg)        # publishing the front distance to the /front_distance topic
        lateral_pub.publish(lateral_dist_msg)      # publishing the left and right distance to /seperate_lateral_distance topic
        region = []                         # List to store the index value in rang list whose distance is less than 50 cm/ 0.5m
        i = 0
        obstacle = 0                        # variable to store the number of obstacles detected in 0.5m range
        angle_list = []                     # list to store the angle range of the laser scan data from -118 degree to 118 degree

        if len(rang) == 945:
            for i in range(0, 945):
                angle_list.append(-118 + (0.24999 * i))  # appending with 0.24999 degree increment from range -118 degree to 118 degree
                #print(len(angle_list))
                if rang[i] <= 0.5:          # CONDITION 1 to detect the obstacle in range of 50 cm/ 0.5 meter
                    region.append(i)        # appending the index values of the obstacles in range of 50 cm
            #print(len(angle_list))
            region.append(1000)             # appending one extra element for the while loop below to avoid "invalid index error"
            sp = 0.0                        # variable to store the index of the start point of the obstacles
            l= 0                            # conter for the while loop
            obstacle = 0
            while l < (len(region)-2):              # to access the index value stored in the region list to sort out obstacles
                if (region[l] + 1) == (region[l + 1]):      # Condition to check the obstacles in region list
                    sp = region[l]                  # assigning the starting point if it satisfy above if condition
                    ep = 0.0                        # variable to store the end index of the obstacles
                    while (region[l] + 1) == region[l + 1]:     # recursive method to check the continuity of the obstacles
                        l = l + 1                   # increment in the counter l
                        ep = region[l]              # assigning the end index of the obstacle if it satisfy recursive method
                    if (ep - sp) >= 100:            # CONDITION 2: if obstacles obstruct the FOV greater the 25 degree or over range of 100 elements
                        obstacle = obstacle + 1     # increment in obstacle counter if it meet CONDITION 1 and CONDITION 2
                        print("ALERT:Obstacle in angle range of {} degree to {} degree".format(angle_list[sp],angle_list[ep]))   #print the range in which the obstacles are detected
                elif l == (len(region) - 1):        # else if condition to check the that the index don't go out of the index
                    break                           # break if above contion are met
                else:
                    l = l + 1                       # add one to the counter if the if condition is not met
            print("Number of Obstacles is {}".format(obstacle))     # print the number of obstacles detected


        rate.sleep()




if __name__ == "__main__":
    main()
