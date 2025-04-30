import tkinter as tk

class CountdownTimer:
    def __init__(self, label, stop_btn, on_finish=None):
        self.label = label
        self.stop_btn = stop_btn  # Use stop_btn here
        self.on_finish = on_finish
        self.total_seconds = 0
        self.remaining_seconds = 0
        self._job = None
        self.running = False
        self.paused = False


    def start(self, minutes=None):
        if not self.running and not self.paused:
            self.total_seconds = int(float(minutes) * 60)
            self.remaining_seconds = self.total_seconds
        self.running = True
        self.paused = False
        self._countdown()
        self.stop_button.config(text="Stop", command=self.stop)

    def _countdown(self):
        if self.remaining_seconds > 0 and self.running:
            mins, secs = divmod(self.remaining_seconds, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining_seconds -= 1
            self._job = self.label.after(1000, self._countdown)
        else:
            if self.remaining_seconds <= 0:
                self.label.config(text="Time's up!")
                if self.on_finish:
                    self.on_finish()
            self.running = False
            self.paused = False
            self.stop_button.config(text="Stop", command=self.stop)

    def stop(self):
        if self._job:
            self.label.after_cancel(self._job)
            self._job = None
        self.running = False
        self.paused = True
        self.stop_button.config(text="Resume", command=self.resume)

    def resume(self):
        if self.paused:
            self.running = True
            self.paused = False
            self._countdown()
            self.stop_button.config(text="Stop", command=self.stop)

    def reset(self):
        if self._job:
            self.label.after_cancel(self._job)
        self.label.config(text="00:00")
        self._job = None
        self.running = False
        self.paused = False
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.stop_button.config(text="Stop", command=self.stop)
