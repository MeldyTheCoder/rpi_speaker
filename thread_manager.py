import asyncio
from _thread import start_new_thread

class ThreadManager:
    def __init__(self):
        self.threads = []
        self.async_threads = []
        self.loop = asyncio.new_event_loop()

    def to_thread(self, func):
        def wrapper(*args, **kwargs):
            thread_id = start_new_thread(func, args, kwargs)
            self.threads.append(thread_id)
            return thread_id
        return wrapper

    def async_thread(self, func):
        def wrapper(*args, **kwargs):
            self.loop.create_task(func, name=func.__name__)
            self.async_threads.append(func.__name__)
            return func.__name__
        return wrapper