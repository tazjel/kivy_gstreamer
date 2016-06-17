from kivy.properties import BooleanProperty, Logger, NumericProperty
from kivy.uix.camera import Camera
from kivy.core.camera import Camera as CoreCamera


class CustomVideoPlayer(Camera):
    fullscreen = BooleanProperty(False)
    '''Switch to fullscreen view. This should be used with care. When
    activated, the widget will remove itself from its parent, remove all
    children from the window and will add itself to it. When fullscreen is
    unset, all the previous children are restored and the widget is restored to
    its previous parent.

    .. warning::

        The re-add operation doesn't care about the index position of it's
        children within the parent.

    :attr:`fullscreen` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    '''

    allow_fullscreen = BooleanProperty(True)
    '''By default, you can double-tap on the video to make it fullscreen. Set
    this property to False to prevent this behavior.

    :attr:`allow_fullscreen` is a :class:`~kivy.properties.BooleanProperty`
    defaults to True.
    '''

    port = NumericProperty(0)

    _fullscreen_state = None

    def __init__(self, **kwargs):
        self._camera = None
        super(Camera, self).__init__(**kwargs)
        if self.index == -1:
            self.index = 0

        self.play = True
        self.allow_stretch = True
        self.reconfigure_camera()

    # noinspection PyUnusedLocal
    def on_index(self, instance, value):
        self.reconfigure_camera()

    # noinspection PyUnusedLocal
    def on_port(self, instance, value):
        self.reconfigure_camera()

    # noinspection PyUnusedLocal
    def on_resolution(self, instance, value):
        self.reconfigure_camera()

    def reconfigure_camera(self):
        self._camera = None
        if self.index < 0:
            return
        if self.resolution[0] < 0 or self.resolution[1] < 0:
            return
        self._camera = CoreCamera(index=self.index, resolution=self.resolution, port=self.port, stopped=True)
        self._camera.bind(on_load=self._camera_loaded)
        if self.play:
            self._camera.start()
            self._camera.bind(on_texture=self.on_tex)

    # noinspection PyUnusedLocal
    def on_fullscreen(self, instance, value):
        window = self.get_parent_window()
        if not window:
            Logger.warning('AliveVideoPlayer: Cannot switch to fullscreen, window not found.')
            if value:
                self.fullscreen = False
            return
        if not self.parent:
            Logger.warning('AliveVideoPlayer: Cannot switch to fullscreen, no parent.')
            if value:
                self.fullscreen = False
            return

        if value:
            self._fullscreen_state = state = {
                'parent': self.parent,
                'pos': self.pos,
                'size': self.size,
                'pos_hint': self.pos_hint,
                'size_hint': self.size_hint,
                'window_children': window.children[:]}

            # remove all window children
            for child in window.children[:]:
                window.remove_widget(child)

            # put the video in fullscreen
            if state['parent'] is not window:
                state['parent'].remove_widget(self)
            window.add_widget(self)

            # ensure the video widget is in 0, 0, and the size will be
            # reajusted
            self.pos = (0, 0)
            self.size = (100, 100)
            self.pos_hint = {}
            self.size_hint = (1, 1)
        else:
            state = self._fullscreen_state
            window.remove_widget(self)
            for child in state['window_children']:
                window.add_widget(child)
            self.pos_hint = state['pos_hint']
            self.size_hint = state['size_hint']
            self.pos = state['pos']
            self.size = state['size']
            if state['parent'] is not window:
                state['parent'].add_widget(self)
