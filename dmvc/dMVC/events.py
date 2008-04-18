import dMVC

class Event:

  def __init__(self, producer, name, params): #{{{
    self.__producer = producer
    self.__name     = name
    self.__params   = params
  #}}}
  
  def objectToSerialize(self, rServer): #{{{
    producerToSerialize = dMVC.objectToSerialize(self.__producer, rServer)
    nameToSerialize     = dMVC.objectToSerialize(self.__name, rServer)
    paramsToSerialize   = dMVC.objectToSerialize(self.__params, rServer)

    eventToSerialize = Event(producerToSerialize, nameToSerialize, paramsToSerialize)

    return eventToSerialize
  #}}}

  def __repr__(self): #{{{
    return "Event: "+str(self.__name)+", producer: "+str(self.__producer)+", params: "+str(self.__params)
  #}}}

  def getProducer(self): #{{{
    return self.__producer
  #}}}

  def getName(self): #{{{
    return self.__name
  #}}}

  def getParams(self): #{{{
    return self.__params
  #}}}
