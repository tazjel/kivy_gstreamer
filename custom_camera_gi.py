# Importing dependencies
import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
from kivy.core.camera.camera_gi import CameraGi

# Initializing GStreamer package
GObject.threads_init()
Gst.init(None)


class CustomCameraGi(CameraGi):
    def __init__(self, **kwargs):
        self.port = kwargs.get('port', 0)
        super().__init__(**kwargs)

    def init_camera(self):
        if self._pipeline:
            self._pipeline = None

        video_src = 'udpsrc port=%d' % (self.port, )
        caps = 'video/x-raw,format=RGB'
        pl = '%s ! application/x-rtp,encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec name=decoder ! ' \
             'videoconvert ! appsink name=camerasink emit-signals=True caps=%s'

        self._pipeline = Gst.parse_launch(pl % (video_src, caps))
        self._camerasink = self._pipeline.get_by_name('camerasink')
        self._camerasink.connect('new-sample', self._gst_new_sample)
        self._decodebin = self._pipeline.get_by_name('decoder')

        if self._camerasink and not self.stopped and self.port > 0:
            self.start()


def custom_camera_gi(**kwargs):
    return CustomCameraGi(**kwargs)
