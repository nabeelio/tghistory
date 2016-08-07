#
import threading


# use as:
# class Something(metaclass=Singleton)
#
class Singleton(type):

    __instances = {}
    __lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """ thread-safe singleton """
        if cls not in cls.__instances:
            # with cls.__lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]
