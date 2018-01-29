import threading


# Thanks to luc's answer for this
# https://stackoverflow.com/questions/1072821/is-modifying-a-class-variable-in-python-threadsafe
def threadsafe(fn):
    """decorator making sure that the decorated function is thread safe"""
    lock = threading.Lock()

    def new(*args, **kwargs):
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            lock.release()
        return r

    return new
