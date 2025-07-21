import sys
import datetime


class Spinner:
    def __init__(self, message="等待中", spinner_type="dots"):
        self.message = message
        self.spinner = self._get_spinner(spinner_type)
        self.index = 0

    def _get_spinner(self, spinner_type):
        spinners = {
            "dots": ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
            "lines": ['|', '/', '-', '\\'],
            "circle": ['◐', '◓', '◑', '◒'],
            "arrows": ['←', '↑', '→', '↓'],
        }
        return spinners.get(spinner_type, spinners["dots"])

    def next(self):
        char = self.spinner[self.index % len(self.spinner)]
        self.index += 1
        now = datetime.datetime.now().strftime("%H:%M:%S")
        sys.stdout.write(f"\r[{now}] {self.message}  {char}   ")
        sys.stdout.flush()

    def clear(self):
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()
