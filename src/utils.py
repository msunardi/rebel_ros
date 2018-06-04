# -*- coding: utf-8 -*-
import time
from datetime import timedelta

def elapsed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)  # Call the method
        end = time.time()
        elapsed = end-start
        print('Elapsed: %s' % str(timedelta(seconds=elapsed)))
        return f  # Return whatever the method returns
    return wrapper

def rprint(pattern, *args):
    print(pattern.format(*args))
    