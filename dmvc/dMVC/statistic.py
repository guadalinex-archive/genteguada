import time

class Statistics:

  def __init__(self,side):
    self.__values = {}
    self.__side = side

  def __str__(self):
    var = ""
    var += "\n<Stadistc side: "+self.__side+">"
    var += "\nValues ::"
    for key in self.__values.keys():
      var += "\n\t"+str(key)+" :: "
      var += str(self.__values[key]["count"]) +" :: "
      var += str(self.__values[key]["size"]) +" :: "+ str(self.__values[key]["totalSize"])+ " :: "
      var += str(self.__values[key]["time"]) +" :: "+ str(self.__values[key]["totalTime"])+ " :: "
    var += "\n"
    return var

  def count(self,key,size,execTime):
    if key in self.__values.keys():
      self.__values[key]["count"] += 1
      self.__values[key]["totalSize"] += size
      self.__values[key]["totalTime"] += execTime
      self.__values[key]["size"] = self.__values[key]["totalSize"] / self.__values[key]["count"]
      self.__values[key]["time"] = self.__values[key]["totalTime"] / self.__values[key]["count"]
    else:
      data = {"count":1,"size":size,"totalSize":size,"totalTime":execTime,"time":execTime}
      self.__values[key] = data 

  def initCount(self,key,size):
    return time.time()

  def stopCount(self,key,size, initTime):
    execTime = time.time() - initTime
    self.count(key,size,execTime)

  def initClientCount(self):
    return time.time()

  def stopClientCount(self,initTime):
    execTime = time.time() - initTime
    print execTime

