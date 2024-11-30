import time
import threading

from tkinter import TOP, LEFT
from tkinter.ttk import Frame, Label, Style
from ttkthemes import ThemedTk

from .slider import Slider
from .group import ChromecastGroup


class ChromecastGUI():
    def __init__(self, update_interval=15):
        self.update_interval = update_interval
        self.sentinel = threading.Event()

        self.root = ThemedTk(theme="breeze")
        self.root.title("Chromecast Volume")
        self.root.wm_withdraw()
        self.root.update()
        self.root.after(1, self.root.deiconify)

        self.style = Style()
        # bold font for sliders
        self.style.configure(
            'Bold.TLabelframe.Label',
            font=('Helvetica', 12, 'bold')
        )

        def close_button():
            self.sentinel.set()
            self.root.destroy()

        # self.root.protocol("WM_DELETE_WINDOW", root.iconify)
        # self.root.protocol("WM_DELETE_WINDOW", root.withdraw)
        self.root.protocol("WM_DELETE_WINDOW", close_button)

    def start(self):
        self.draw_main_window()

        self.chromecasts = ChromecastGroup().chromecasts

        self.load_label.destroy()
        self.frame_top_line.destroy()

        self.draw_chromecast_sliders()
        self.set_sliders_from_devices()
        
        self.main_loop()

    def draw_main_window(self):
        # add elements of GUI
        self.frame_top_line = Frame(self.root)
        self.frame_top_line.pack(side=TOP)

        self.load_label = Label(
            self.frame_top_line,
            text="Chromecast Volume\n2024 Ian Dennis Miller\nLocating chromecasts...\nFirst run is slow; future runs are faster.",
        )
        self.load_label.pack()

        self.frame = Frame(
            self.root,
            width=200,
            height=60
        )
        self.frame.pack(side=TOP)
        self.refresh()

    def main_loop(self):
        start_time = time.time()

        while not self.sentinel.is_set():
            time.sleep(0.01)
            self.root.update_idletasks()
            self.root.update()

            if time.time() - start_time > self.update_interval:
                self.set_sliders_from_devices()
                start_time = time.time()

    def exit(self):
        self.sentinel.set()
        self.root.destroy()

    def refresh(self):
        self.root.update()
        self.root.update_idletasks()

    def draw_chromecast_sliders(self):
        self.sliders = [ Slider(self.frame, cc) for cc in self.chromecasts ]       

        for sf in self.sliders:
            sf.pack(side=LEFT)

        self.refresh()

    def set_sliders_from_devices(self):
        # update chromecast objects with latest status from actual device
        for chromecast in self.chromecasts:
            chromecast.wait()

        # update GUI percent labels based on chromecast status
        for slider in self.sliders:
            slider.update_from_device_info()

        self.refresh()
