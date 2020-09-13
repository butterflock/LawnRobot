# Smart Lawn Robot

A smart robot lawn mower. The robot uses Machine Learning for navigation and grass detection. 

In contrast to most existing robot lawn mowers, this prototype does not require a perimeter wire and the robot can detect obstacles such as children or small animals (e.g. hedgehog) without even touching them.

**Video** https://youtu.be/wq4QNpEY3-k


### Things you need
- Raspberry Pi with Camera
- Arduino Nano for motor control and sensors
- Robot lawn mower platform (I used an old Gardena R70li)

### Run
```shell
sudo python3 app.py 
```

Go to the web interface running on port 80. 

### Web Interface

Select camera and model on the Main Screen

#### Drive Screen
* Camera Image (top left)
* Segmentation (top right)
* Speed Controller (bottom left)
* Joystick for manual control (bottom right)
* Button to start automatic drive (bottom center)

![Image of the Drive Screen](DriveScreen.png)

