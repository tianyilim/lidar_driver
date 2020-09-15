# diyLIDAR
DIY LIDAR sensor based on spare sensors

## Bill of Materials:
| S/N 	| Part                          	| Qty 	| Function                              	|
|-----	|-------------------------------	|:---:	|---------------------------------------	|
| 1   	| VL53L0X TOF Sensor (Adafruit) 	|  2  	| Fairly accurate, fast distance sensor 	|
| 2   	| Random DC Motor        	        |  1  	| Motor for driving the LIDAR.          	|
| 3   	| DRV8833 Motor Driver Breakout   	|  1  	| Stepper Motor Driver                  	|
| 4   	| TCRT5000 IR sensor            	|  2  	| Negative feedback/crude motor encoder 	|
| 5  	| Arduino Nano                  	|  1  	| Microcontroller                       	|

## Function:
The whole idea is to emulate something like a RPLidar: using an Arduino Nano as an intermediate microcontroller.
Screenshots will be added if the project continues on.

The motor is a small DC motor controlled by a DRV8833 driver board.
The 2 distance sensors are Adafruit VL53L0X sensors controlled using Pololu's library (to save memory space on the Arduino).

## Arduino-side software:
Library dependencies are:
> TODO Add links to other GitHub repos
Additionally, we use a pair of TCRT-5000 IR sensor to provide feedback on disc rotation, wired to an external interrupt.