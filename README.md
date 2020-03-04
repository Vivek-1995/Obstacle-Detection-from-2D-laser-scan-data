# Obstacle-Detection-from-2D-laser-scan-data
First change the directory, where the sensor bag file is placed, then run the below command in terminal:<br />
`rosbag play sensor.bag -l`<br />
after executing the above command the Angle range of the obstacles and number of obstacles will be displayed.

The node to launch the package is 'scan_value' and below command in another terminal will run the node:<br />
`roslaunch task_1 task_1.launch`

After running above command, to see the node publishing to /front_distance topic by executing following command in new terminal:<br />
`rostopic echo /front_distance`

After running above command, to see the node publishing to /lateral_distances topic by following command in new terminal:<br />
`rostopic echo /lateral_distances`

To visualize the topic /scan (laser data) in rviz, in new terminal use following command:<br />
`rosrun rviz rviz`<br />
and add LaserScan (/scan topic) topic and Pose (sl_position)
