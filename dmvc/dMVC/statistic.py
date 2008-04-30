
class Statistics:

  def __init__(self,side):
    self.__values = {}
    self.__side = side

  def __str__(self):
    var = ""
    var += "\n<Stadistc side: "+self.__side+">"
    var += "\nValues ::"
    for key in self.__values.keys():
      var += "\n\t"+str(key)+" :: "+str(self.__values[key]["count"]) +" :: "+ str(self.__values[key]["size"]) +" :: "+ str(self.__values[key]["totalSize"])
    var += "\n"
    return var

  def count(self,key,size):
    if key in self.__values.keys():
      self.__values[key]["count"] += 1
      self.__values[key]["totalSize"] += size
      self.__values[key]["size"] = self.__values[key]["totalSize"] / self.__values[key]["count"]
    else:
      data = {"count":1,"size":size,"totalSize":size}
      self.__values[key] = data 
