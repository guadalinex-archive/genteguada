import unittest
import thread
import time
import random
import Queue

import dMVC.remoteclient

import models


class TestRemoteObject(unittest.TestCase):

  def setUp(self):
    self.eventQueue = Queue.Queue()
    self.name = None

 
  def testRemoteModel(self):
    print "Conectando con el server"
    #client = dMVC.remoteclient.RClient("192.168.0.33")
    client = dMVC.remoteclient.RClient("127.0.0.1")
    
    print "Ejecutando test con model remoto"
    model = client.getRootModel()
    self.useModel(model, "REMOTE: ")

  def testLocalModel(self):
    print "Ejecutando test con model local"
    model = models.TestModel()
    self.useModel(model, "LOCAL: ")

  def setLocalExecution(self, bool):
    self.localExecuted = bool

  def useModel(self, model, prefix):
    print prefix + "model class: " + str(model.__class__)

    print prefix + "client side execution"
    self.setLocalExecution(False)
    def localFunc():
      print "********* ejecuting local function **********"
      self.setLocalExecution(True)
    model.localFunctionExecution(localFunc)
    assert self.localExecuted == True

    print prefix + "Ejecutamos el metodo foo sin argumentos"
    result = model.foo()
    assert result == "foo"

    print prefix + "Ejecutamos el metodo foo sin argumentos"
    result = model.foo()
    assert result == "foo"

    print prefix + "Ejecutamos el metodo bar sin argumentos"
    result = model.bar()
    assert result == "bar"

    print prefix + "Obtenemos un modelo a partir del root model"
    player = model.player()

    print prefix + "player client side execution"
    player.localMethod()

    print prefix + "Ejecutamos un metodo del objeto obtenido a partir del root"
    result = player.name()
    assert result == "maradona"

    print prefix + "Ejecutamos un metodo del rootModel pasando un parametro"
    param = "Antonio"
    result = model.sayHello(param)
    assert result == "Hello " + param

    print prefix + "Ejecutamos un metodo del rootModel pasando dos parametros"
    param1 = "Luis"
    param2 = "Garcia"
    result = model.fullName(param1, param2)
    assert result == param1+ " " + param2

    print prefix + "Ejecutamos un metodo que nos da una excepcion ya que no se encuentra definido"
    raisedExceptionMethodNoFound = False
    try:
      result = model.name()
    except:
      raisedExceptionMethodNoFound = True
    assert raisedExceptionMethodNoFound == True

    print prefix + "Ejecutamos un metodo que nos da una excepcion por error de codigo del metodo 1/0"
    raisedExceptionMethodError = False
    try:
      result = model.metodoError()
    except:
      raisedExceptionMethodError = True
    assert raisedExceptionMethodError == True

    print prefix + "ejecutamos un metodo que nos devuelve una lista"
    result = model.listPlayers()
    assert result.__class__ == list
    #assert result.__class__ == tuple
    for i in range(len(result)):
      name = result[i].name()
      assert name == "maradona"
      
    print prefix + "ejecutamos un metodo que nos devuelve una tupla"
    result = model.tuplePlayers()
    assert result.__class__ == tuple
    for i in range(len(result)):
      name = result[i].name()
      assert name == "maradona"

    print prefix + "ejecutamos un metodo que nos devuelve un diccionario"
    result = model.dictPlayers()
    assert result.__class__ == dict
    for key in result.keys():
      name = result[key].name()
      assert name == "maradona"

    print prefix + "ejecutamos un metodo pasando por parametro un remotemodel"
    result = model.getName(player)
    assert result == "maradona"

    print prefix + "ejecutamos un metodo pasando por parametro una lista de remotemodel"
    result = model.getListName([player])
    assert result == "maradona"

    print prefix + "ejecutamos un metodo pasando por parametro una tupla de remotemodel"
    result = model.getTupleName((player,))
    assert result == "maradona"
    
    print prefix + "ejecutamos un metodo pasando por parametro una diccionario de remotemodel"
    result = model.getDictName({"1":player})
    assert result == "maradona"

    model.setPosition([0,0])
    model.setName('')
    print prefix + "Nos suscribimos a eventos"
    assert self.eventQueue.empty()
    model.subscribeEvent('position', self.eventFired)
    model.subscribeEvent('name',     self.eventFired)
    assert self.eventQueue.empty()


    print prefix + "Cambiamos la posicion"
    model.setPosition([1,2])
    lastEvent = self.getLastEvent()
    assert lastEvent.getName() == 'position'
    assert lastEvent.getProducer() == model
    assert lastEvent.getParams()['position'] == [1,2]

    print prefix + "Cambiamos la posicion, nuevamente"
    model.setPosition([2,4])
    lastEvent = self.getLastEvent()
    assert lastEvent.getName() == 'position'
    assert lastEvent.getProducer() == model
    assert lastEvent.getParams()['position'] == [2,4]

    print prefix + "Cambiamos el nombre"
    model.setName('Guido')
    lastEvent = self.getLastEvent()
    assert lastEvent.getName() == 'name'
    assert lastEvent.getProducer() == model
    assert lastEvent.getParams()['name'] == 'Guido'

    model.setPosition([4,8])
    lastEvent = self.getLastEvent()
    assert lastEvent.getName() == 'position'
    assert lastEvent.getProducer() == model
    assert lastEvent.getParams()['position'] == [4,8]
    assert self.name == 'foo'
  
    print prefix + "probamos a desuscribirnos de los eventos"
    model.unsubscribeEventObserver(self)
    model.setPosition([40,80])
    assert self.eventQueue.empty()

    print prefix + "probamos un metodo local sobre una variable local"
    k = model.getConstant()
    assert k == 'CONSTANT'
    #model._constant = 'FOO'

    print prefix + "Herencia de atributos serializados del padre"
    subplayer = model.getSubPlayer()
    constHeredada = subplayer.constHeredada
    assert constHeredada == "Constante heredada"

  
  def eventFired(self, event):
    self.name =  event.getProducer().foo()
    self.eventQueue.put(event)

  def getLastEvent(self):
    result = self.eventQueue.get()
    return result

if __name__ == "__main__":
  test = unittest.main()
