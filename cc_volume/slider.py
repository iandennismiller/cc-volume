from tkinter.ttk import LabelFrame, Scale


class Slider(LabelFrame):
    def __init__(self, root, chromecast):
        self.chromecast = chromecast
        self.root = root

        super().__init__(
            root,
            text=chromecast.name,
            style='Bold.TLabelframe',
        )

        self.scale = Scale(self,
            from_=100,
            to=0,
            orient="vertical",
            length=300,
        )
        self.scale.bind("<ButtonRelease-1>", self.slider_release_callback)
        self.scale.pack()

    def slider_release_callback(self, v):
        volume = v.widget.get()
        volume_chromecast = volume / 100
        self.chromecast.set_volume(volume_chromecast)

    def update_from_device_info(self):
        volume_chromecast = self.chromecast.status.volume_level
        volume = volume_chromecast * 100
        self.scale.set(volume)
