import kivy
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty

# Importing dependencies
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# set up debug level for gstreamer
import os

os.environ["GST_DEBUG"] = "*:0"


class MyRootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyRootWidget, self).__init__(**kwargs)
        self.mainApp = None

    # property for the label --> changing it's value will change the text of the label
    fileTxt = StringProperty('Test started, press button...')

    # callback for play button
    def playIt(self):
        self.fileTxt = os.path.abspath(self.mainApp.filename) + ' started!'
        self.mainApp.startPlaying()

    # callback for stop button
    def stopIt(self):
        self.fileTxt = os.path.abspath(self.mainApp.filename) + ' stopped!'
        self.mainApp.stopPlaying()


# main application class, kv file with same name (first letter lower case) will be loaded automatically
class KivyGst(App):
    filename = "test.mp3"

    def build(self):
        # self.rootWidget = MyRootWidget(self)
        rootWidget = Builder.load_file('ui.kv')
        rootWidget.mainApp = self

        self.initGst()
        return rootWidget

    def on_stop(self):
        self.pipeline.set_state(Gst.State.NULL)

    def initGst(self):
        # Initializing GStreamer package
        GObject.threads_init()
        Gst.init(None)

        # set up pipeline
        self.pipeline = Gst.Pipeline("mypipeline")

        # get the source and add it to the pipeline
        self.file = Gst.ElementFactory.make("filesrc", "file")
        self.file.set_property("location", self.filename)
        self.pipeline.add(self.file)

        # set up the decoder, the source pad will be generated dynamically,
        # thus we need a callback to link it with the converter
        self.decode = Gst.ElementFactory.make("decodebin", "decode")
        self.decode.connect("pad-added", self.decode_src_created)
        self.pipeline.add(self.decode)

        # set up the converter
        self.convert = Gst.ElementFactory.make("audioconvert", "convert")
        self.pipeline.add(self.convert)

        # set up the output
        self.sink = Gst.ElementFactory.make("autoaudiosink", "sink")
        self.pipeline.add(self.sink)

        # link the things together
        self.file.link(self.decode)
        self.convert.link(self.sink)

    # start playing
    def startPlaying(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    # stop playing
    def stopPlaying(self):
        self.pipeline.set_state(Gst.State.NULL)

    # handler taking care of linking the decoder's newly created source pad to the sink
    def decode_src_created(self, element, pad):
        print("decode pad created")
        pad.link(self.convert.get_static_pad("sink"))


if __name__ == '__main__':
    KivyGst().run()
