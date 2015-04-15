from threading import Timer

import collect

from datetime import datetime


class periodicTask(object):
    
    def __init__(self, interval , callback, daemon = False, **kwargs):
        
        self.interval = interval
        self.callback = callback
        self.daemon = daemon
        self.kwargs = kwargs

    def throttle(self):

        self.callback(**self.kwargs)

        for key in self.kwargs:
            print 'ARG LIST:', key, self.kwargs[key]
        
        # interval in seconds
        t = Timer(self.interval, self.throttle)
        t.daemon = self.daemon
        t.start()
        
        value = self.callback(**self.kwargs)
        print 'timestamp = ', value, datetime.now()

# test case: non-parameterized
def print_hw():

    print 'hello world!'
    return 1

# test case: parameterized
def print_hw2(name, timestamp):

    print 'hello world 2!'.format(name)
    timestamp += 2
    return timestamp


if __name__ == '__main__':

    task = periodicTask(interval=1, callback=print_hw)
    print 'func1\n', task.throttle()

    task = periodicTask(interval=1, callback=print_hw2, name='syan', timestamp=33)
    print 'func2\n', task.throttle()

