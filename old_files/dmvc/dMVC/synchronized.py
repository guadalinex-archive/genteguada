import threading


def synchronized(lockName):
  def decorator(func):
    def wrapper(*args, **kargs):
      self = args[0]
      lock = self.getLockNamed(lockName)
      lock.acquire()
      if self.debug:
        print func.__name__ + ' has acquired the lock "' + lockName + '" for ' + str(self)
      try:
        return func(*args, **kargs)
      finally:
        lock.release()
        if self.debug:
          print func.__name__ + ' has released the lock "' + lockName + '" for ' + str(self)
    wrapper.lockName = lockName
    return wrapper
  return decorator


class Synchronized:
  def __init__(self, debug=False):
    self.debug = debug

    self.__locks = {}
    self.__initLocks()

  def __initLocks(self):
    for key in dir(self):
      function = getattr(self, key)
      if callable(function):
        if 'lockName' in function.__dict__:
          lockName = function.__dict__['lockName']
          if not lockName in self.__locks:
            if self.debug:
              print 'creating the lock ' + lockName + ' in ' + str(self)
            self.__locks[lockName] = threading.RLock()


  def getLockNamed(self, lockName):
    return self.__locks[lockName]
