# Li-Fi applied to robotics : automation on disconnection

## Introduction

This project was originally conducted by me and the other three classmates. Below I’ll extract the main points which illustrates the part I took charge in specifically. This project was a collaboration with the company Lucibel that develops the Li-Fi technology (Light-Fidelity). It is a technology still little used and we collaborated with them to help develop its usage for indoor robotics. 

Li-Fi is a kind of wireless communication using light to transmit data, however mobile robots frequently get disconnected from fixed sources. I was responsable for writing scripts (Python, Bash) to make our robot behave correctly during disconnection and direct itself to the nearest source. Our robot is called Turtlebot3 and has led to carry out thorough research on ROS (Robot Operating System).

Since we had some problems with the installation of Li-Fi’s driver, and failed to get help from Lucibel during our project, we tried to use Wi-Fi to simulate the same behavior to get a result close to what we could have obtained with a Li-Fi connection.

## Specificity of problem & Objectives

To stay close to the initial problems, we restricted ourselves to Li-Fi’s contraints :
1. Li-Fi’s covering zone is not connected, thus in some areas the robot cannot receive orders from the network: we must be able to know in real time if it is connected.

2. We need to be able to simulate disconnection and, if necessary, run the robot with an independant script at the same time.

3. We must be able to find a connection and, as soon as it is found, control our robot from the Remote PC. Our two main objectives were: 
	- Write scripts allowing us to control the robot’s movement efficiently.
	- Have a global control of the robot upon connection and disconnection in real time.

The other team worked on the research of good algorithms in Python during the robot’s disconnection in order to find the nearest Li-Fi source, which they simulated with circles, in the most efficient way. The final goal of our project was to combine these two parts so that the robot can behave correctly during its loss of connection.

## Further details

Please refer to **report.pdf** to get further details.