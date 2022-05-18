__all__ = ['event', 'timer', 'handle', 'event_filter']

import functools
import threading
import time


class event:
    def __init__(self, owner, name: str = None):
        if name is None:
            self._name = hex(id(self))
        else:
            self._name = name

        self._sender = owner
        self._handlers = list()

    def __repr__(self):
        return f"event<{repr(self._sender)}.{self._name}>"

    def hook(self, handler):
        self._handlers.append(handler)

    def call(self, f, message):
        if message is None:
            f(self._sender)
        else:
            f(self._sender, message)

    def happen(self, message=None):
        for h in self._handlers:
            self.call(h, message)


class timer:
    __id = 0

    def __init__(self, name: str = None, interval: float = 0):
        timer.__id += 1
        self._id = timer.__id

        self.tick = event(self, 'tick')

        self._on = False
        self._interval = 0
        self.interval = interval
        self._thread = None

        if name is not None:
            self._name = name
        else:
            self._name = hex(id(self))

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, val: bool):
        if val:
            self.run()
        else:
            self.stop()

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, val: float):
        if val < 0:
            raise Exception("Can't set interval less than 0")
        self._interval = val

    def __repr__(self):
        return f"timer<{self._name}#{self._id}>"

    def run(self):
        self._on = True
        self._thread = threading.Thread(target=self.__tick)
        self._thread.start()

    def stop(self):
        self._on = False

    def __tick(self):
        while self.on:
            time.sleep(self._interval)
            self.tick.happen()


def handle(*events: event):
    def decorator(f):
        for e in events:
            e.hook(f)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    return decorator


def event_filter(message_handler):
    def _event_filter(*my_filters):
        def decorator(f):
            @functools.wraps(f)
            def wrapper(obj, message):
                success = True
                for fl in my_filters:
                    message_handler(f"....try on filter<{fl.__name__}>")
                    success &= fl(message)

                if success:
                    message_handler(f"....success")
                    return f(obj, message)
                else:
                    message_handler(f"....failed and skip")

            return wrapper

        return decorator

    return _event_filter
