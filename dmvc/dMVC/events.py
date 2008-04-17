
import utils

class Event:

  def __init__(self, producer, name, params): #{{{
    utils.logger.debug("Event.__init__")
    self.__producer = producer
    self.__name = name
    self.__params = params
  #}}}
  
  def objectToSerialize(self, rServer): #{{{
    utils.logger.debug("Event.objectToSerialize rServer: "+str(rServer))
    eventToSerialize = Event(utils.objectToSerialize(self.__producer, rServer), utils.objectToSerialize(self.__name, rServer), utils.objectToSerialize(self.__params, rServer))
    return eventToSerialize
  #}}}

  def __repr__(self): #{{{
    utils.logger.debug("Event.__repr__")
    return "EVENT Name: "+str(self.__name)+" Producer: "+str(self.__producer)+" Params: "+str(self.__params)
  #}}}

  def getProducer(self): #{{{
    utils.logger.debug("Event.getProducer")
    return self.__producer
  #}}}

  def getName(self): #{{{
    utils.logger.debug("Event.getName")
    return self.__name
  #}}}

  def getParams(self): #{{{
    utils.logger.debug("Event.getParams")
    return self.__params
  #}}}
