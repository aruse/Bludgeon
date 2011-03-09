# Copyright (c) 2011, Andy Ruse

class Timer:
    """Used to count down to a specific event."""

    def __init__(self, clock, event):
        """clock is the amount of time until the event happens."""
        self.clock = clock
        self.event = event

    def countdown(self, amt=1):
        """Countdown by a the givent amt."""
        pass

    def trigger():
        """Trigger the event."""
        self.event()
