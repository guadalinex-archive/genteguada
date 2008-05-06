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
    for key in self.__valuesServer.keys():
      var += "\n\t"+str(key)+" :: "
      var += str(self.__valuesServer[key]["count"]) +" :: "
      var += str(self.__valuesServer[key]["size"]) +" :: "+ str(self.__valuesServer[key]["totalSize"])+ " :: "
      var += str(self.__valuesServer[key]["time"]) +" :: "+ str(self.__valuesServer[key]["totalTime"])+ " :: "
    var += "\n"
    print var

  def strClient(self):
    var = ""
    var += "\n<Stadistc side: "+self.__side+">"
    var += "\nValues ::"
    for key in self.__valuesClient.keys():
      var += "\n\t"+str(key)+" :: "
      var += str(self.__valuesClient[key]["count"]) +" :: "
      var += str(self.__valuesClient[key]["time"]) +" :: "+ str(self.__valuesClient[key]["totalTime"])+ " :: "
    var += "\n"
    print var

  def countServer(self, key, size, execTime):
    if key in self.__valuesServer.keys():
      self.__valuesServer[key]["count"] += 1
      self.__valuesServer[key]["totalSize"] += size
      self.__valuesServer[key]["totalTime"] += execTime
      self.__valuesServer[key]["size"] = self.__valuesServer[key]["totalSize"] / self.__valuesServer[key]["count"]
      self.__valuesServer[key]["time"] = self.__valuesServer[key]["totalTime"] / self.__valuesServer[key]["count"]
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
    if key in self.__valuesClient.keys():
      self.__valuesClient[key]["count"] += 1
      self.__valuesClient[key]["totalTime"] += execTime
      self.__valuesClient[key]["time"] = self.__valuesClient[key]["totalTime"] / self.__valuesClient[key]["count"]
    else:
      data = {"count":1, "totalTime":execTime, "time":execTime}
      self.__valuesClient[key] = data

  def addEvent(self, key):
    if key in self.__valuesEvent.keys():
      self.__valuesEvent[key] += 1
    else:
      self.__valuesEvent[key] = 1

  def strEvent(self):
    var = ""
    var += "\n<Stadistc side: "+self.__side+">"
    var += "\nValues ::"
    for key in self.__valuesEvent.keys():
      var += "\n\t"+str(key)+" :: "
      var += str(self.__valuesEvent[key]) +" :: "
    var += "\n"
    print var

    
    
