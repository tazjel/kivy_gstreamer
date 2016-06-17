# Requirements
This code was tested using the following:

1.- Ubuntu 16.04

2.- Gstreamer 1.8.1.0 with the installed packages by default.

3.- Kivy v1.9.2

# Motivation
I needed to integrate Kivy 1.9.2 with GStreamer using my own pipeline.

According to: https://github.com/kivy/kivy/blob/master/kivy/core/camera/__init__.py

The following line is commented: providers += (('gi', 'camera_gi', 'CameraGi'), )

This line contains the link to the class "CamereGi" located in: https://github.com/kivy/kivy/blob/master/kivy/core/camera/camera_gi.py

This class according to the documentation says: "Implement CameraBase with Gi / Gstreamer, working on both Python 2 and 3"

This class has support for both GStreamers 1.0< and 1.0>. So this should be the kind that is imported as "provider" using Ubuntu 16.04. But that does not happen and the class is imported instead is: https://github.com/kivy/kivy/blob/master/kivy/core/camera/camera_pygst.py, where the implementation is for GStreamer 1.0<. This brings not work CONSEQUENCES integration with GStreamer.

# Solution

1. Create a new provider based on: "CameraGi". To do this we must keep in mind that the implementation of this class is very general and focuses directly on what is captured using the camera "v4l2src".
So it is necessary to redefine the pipeline that is generated from the method execution: init_camera, which it is invoked from the class: "CameraBase".

2. The generated class inherits from: "CameraGi" and has a method: "custom_camera_gi" used as a"Factory" for instantiating the class: "CustomCameraGi"

3. After that, taking advantage of the widget "Camera" inherit from this and create a new class, in this case, "CustomVideoPlayer" this will be the component responsible for displaying the video using the same mechanisms Kivy has by default.
