"""
Camera Example
==============

"""

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

# For testing open a console and execute the following code:
# gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay !
# udpsink host=127.0.0.1 port=5000

from kivy.app import App
from kivy.lang import Builder

kv = '''
#:import CustomVideoPlayer custom_video_player.CustomVideoPlayer
BoxLayout:
    orientation: 'vertical'
    CustomVideoPlayer:
        id: camera
        resolution: (640, 480)
        port: 5000
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    ToggleButton:
        text: 'Full screen'
        on_press: camera.fullscreen = not camera.fullscreen
        size_hint_y: None
        height: '48dp'
'''


class GstKivyCamera(App):
    title = 'Kivy Camera using GStreamer 1.0.'

    import kivy.core.camera
    from custom_camera_gi import custom_camera_gi
    kivy.core.camera.Camera = custom_camera_gi

    def build(self):
        return Builder.load_string(kv)


GstKivyCamera().run()
