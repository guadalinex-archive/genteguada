import time

class Statistics:

  def __init__(self, side):
    self.__valuesServer = {}
    self.__valuesClient = {}
    self.__valuesEvent = {}
    self.__side = side

  def strServer(self):
    var = ""
    var += "\n<Stadistc side: "+self.__side+">"
    var += "\nValues ::"
    for key, value in self.__valuesServer.iteritems():
      var += "\n\t"+str(key)+" :: "
      var += str(value["count"]) +" :: "
      var += str(value["size"]) +" :: "+ str(value["totalSize"])+ " :: "
      var += str(value["time"]) +" :: "+ str(value["totalTime"])+ " :: "
    var += "\n"
    print var

  def strClient(self):
    var = ""
    var += "\n<Stadistc side: "+self.__side+">"
    var += "\nValues ::"
    for key, value in self.__valuesClient.iteritems():
      var += "\n\t"+str(key)+" :: "
      var += str(value["count"]) +" :: "
      var += str(value["time"]) +" :: "+ str(value["totalTime"])+ " :: "
    var += "\n"
    print var

  def countServer(self, key, size, execTime):
    if key in self.__valuesServer:
      value = self.__valuesServer[key]
      value["count"] += 1
      value["totalSize"] += size
      value["totalTime"] += execTime
      value["size"] = value["totalSize"] / value["count"]
      value["time"] = value["totalTime"] / value["count"]
    else:
      data = {"count":1, "size":size, "totalSize":size, "totalTime":execTime, "time":execTime}
      self.__valuesServer[key] = data 

  def initCount(self, key, size):
    return time.time()

  def stopCount(self, key, size, initTime):
    execTime = time.time() - initTime
    self.countServer(key, size, execTime)

  def initClientCount(self):
    return time.time()

  def stopClientCount(self, initTime, key):
    execTime = time.time() - initTime
    self.countClient(key, execTime)

  def countClient(self, key, execTime):
    if key in self.__valuesClient:
      value = self.__valuesClient[key]
      value["count"] += 1
      value["totalTime"] += execTime
      value["time"] = value["totalTime"] / value["count"]
    else:
      data = {"count":1, "totalTime":execTime, "time":execTime}
      self.__valuesClient[key] = data

  def addEvent(self, key):
    if key in self.__valuesEvent:
      self.__valuesEvent[key] += 1
    else:
      self.__valuesEvent[key] = 1

  def strEvent(self):
    var = ""
    var += "\n<Stadistc side: "+self.__side+">"
    var += "\nValues ::"
    for key, value in self.__valuesEvent.iteritems():
      var += "\n\t"+str(key)+" :: "
      var += str(value) +" :: "
    var += "\n"
    print var

    
    
