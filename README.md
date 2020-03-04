# Obstacle-Detection-from-2D-laser-scan-data

The node to launch the package is 'scan_value' and below command in another terminal will run the node:<br />
`roslaunch task_1 task_1.launch`

After running above command, to see the node publishing to /front_distance topic by executing following command in new terminal:<br />
`rostopic echo /front_distance`

After running above command, to see the node publishing to /lateral_distances topic by following command in new terminal:<br />
`rostopic echo /lateral_distances`

To visualize the topic /scan (laser data) in rviz, in new terminal use following command:<br />
`rosrun rviz rviz`<br />
and add LaserScan (/scan topic) topic and Pose (sl_position)
