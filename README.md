# F1T
Building a cheap, open-source, autonomous RC-Car
I've been inspired by the F1Tenth tournament for quite a while now. 
I will document my struggles, findings and code in this Repo. 

# Requirements
as of now I'm using
Opencv=4.1.1
python3.6

There can be a few errors popping up but most of them are easily fixed by simply running pip install <missing package> or (mostly gstreamer missing modules) sudo apt-get <missing package>


# HOW TO SETUP PROJECT
In the directory you cloned this project in.

```
cd F1T
pip install -e .
```

This will install the necessary packages for this project as well as make it possbile to avoid Module errors and having to define absolute paths.

# Hardware:
RC-Car: ,
Camera: IMX219-83 Module,
Jetson: 
Lidar:
...:

# IMX219-83 Stereo Camera Module

I've written a python script to have synced frames of both the camera sensors on the Module. 
Information on the internet on how to actually do that is quite sparse, therefore, I hope this will be helpful to you!

Code will be better documented soon, I'm still tinkering with structure. Advice is appreciated.








