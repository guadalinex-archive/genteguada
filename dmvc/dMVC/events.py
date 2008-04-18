import dMVC
#import utils

class Event:

  def __init__(self, producer, name, params): #{{{
    #utils.logger.debug("Event.__init__")
    self.__producer = producer
    self.__name     = name
    self.__params   = params
  #}}}
  
  def objectToSerialize(self, rServer): #{{{
    #utils.logger.debug("Event.objectToSerialize rServer: "+str(rServer))

    producerToSerialize = dMVC.objectToSerialize(self.__producer, rServer)
    nameToSerialize     = dMVC.objectToSerialize(self.__name, rServer)
    paramsToSerialize   = dMVC.objectToSerialize(self.__params, rServer)

    eventToSerialize = Event(producerToSerialize, nameToSerialize, paramsToSerialize)

    return eventToSerialize
  #}}}

  def __repr__(self): #{{{
    #utils.logger.debug("Event.__repr__")
    return "EVENT Name: "+str(self.__name)+", producer: "+str(self.__producer)+", params: "+str(self.__params)
  #}}}

  def getProducer(self): #{{{
    #utils.logger.debug("Event.getProducer")
    return self.__producer
  #}}}

  def getName(self): #{{{
    #utils.logger.debug("Event.getName")
    return self.__name
  #}}}

  def getParams(self): #{{{
    #utils.logger.debug("Event.getParams")
    return self.__params
  #}}}
