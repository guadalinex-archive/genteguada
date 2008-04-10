import threading

__ID_MUTEX = threading.Semaphore(1)
__ID = 0

def nextID():
  global __ID
  global __ID_MUTEX
  __ID_MUTEX.acquire() 
  __ID += 1
  result = __ID
  __ID_MUTEX.release() 
  return result
  
