import tkinter as tk

class CountdownTimer:
    def __init__(self, label, stop_btn, on_finish=None):
        """
        Initializes the CountdownTimer.

        :param label: tk.Label widget to display the time
        :param stop_btn: tk.Button widget to act as the stop/resume control
        :param on_finish: Optional callback function called when timer reaches zero
        """
        self.label = label
        self.stop_button = stop_btn  # Button used to stop/resume the timer
        self.on_finish = on_finish  # Callback for when timer finishes
        self.total_seconds = 0  # Total countdown time in seconds
        self.remaining_seconds = 0  # Remaining time in seconds
        self._job = None  # Reference to the scheduled `after` job
        self.running = False  # Whether the timer is actively running
        self.paused = False  # Whether the timer is paused

    def start(self, minutes=None):
        """
        Starts the countdown timer from the given number of minutes.

        :param minutes: The number of minutes to count down from
        """
        if not self.running and not self.paused:
            self.total_seconds = int(float(minutes) * 60)  # Convert minutes to seconds
            self.remaining_seconds = self.total_seconds
        self.running = True
        self.paused = False
        self._countdown()  # Begin the countdown loop
        self.stop_button.config(text="Stop", command=self.stop)  # Set stop button

    def _countdown(self):
        """
        Internal method to handle the countdown logic and UI updates.
        Called every 1000 ms (1 second) via Tkinter's `after`.
        """
        if self.remaining_seconds > 0 and self.running:
            mins, secs = divmod(self.remaining_seconds, 60)  # Split into minutes and seconds
            self.label.config(text=f"{mins:02d}:{secs:02d}")  # Update label
            self.remaining_seconds -= 1
            self._job = self.label.after(1000, self._countdown)  # Schedule next tick
        else:
            if self.remaining_seconds <= 0:
                self.label.config(text="Time's up!")
                if self.on_finish:
                    self.on_finish()  # Call finish callback if provided
            self.running = False
            self.paused = False
            self.stop_button.config(text="Stop", command=self.stop)

    def stop(self):
        """
        Stops (pauses) the countdown timer.
        Allows the user to resume it later.
        """
        if self._job:
            self.label.after_cancel(self._job)  # Cancel the scheduled countdown tick
            self._job = None
        self.running = False
        self.paused = True
        self.stop_button.config(text="Resume", command=self.resume)  # Change button to resume

    def resume(self):
        """
        Resumes the countdown timer if it was paused.
        """
        if self.paused:
            self.running = True
            self.paused = False
            self._countdown()  # Restart countdown
            self.stop_button.config(text="Stop", command=self.stop)

    def reset(self):
        """
        Resets the countdown timer to 00:00 and clears state.
        """
        if self._job:
            self.label.after_cancel(self._job)
        self.label.config(text="00:00")
        self._job = None
        self.running = False
        self.paused = False
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.stop_button.config(text="Stop", command=self.stop)  # Reset button state
