import unittest
import thread
import time
import random
import dMVC.remoteclient

import models


class TestRemoteObject(unittest.TestCase):

  def setUp(self):
    self.lastEvent = None

 
  def testRemoteModel(self):
    print "Conectando con el server"
    client = dMVC.remoteclient.RClient("127.0.0.1")
    
    print "Ejecutando test con model remoto"
    model = client.getRootModel()
    self.useModel(model, "REMOTE: ")

  def testLocalModel(self):
    print "Ejecutando test con model local"
    model = models.TestModel()
    self.useModel(model, "LOCAL: ")

  def useModel(self, model, prefix):
    print prefix + "model class: " + str(model.__class__)
    print prefix + "Ejecutamos el metodo foo sin argumentos"
    result = model.foo()
    assert result == "foo"

    print prefix + "Ejecutamos el metodo bar sin argumentos"
    result = model.bar()
    assert result == "bar"

    print prefix + "Obtenemos un modelo a partir del root model"
    player = model.player()

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
    """
    print prefix + "Ejecucion desde multiples hilos"
    t1 = thread.start_new_thread(self.checkSayHello, (prefix, model, "Luis"))
    t2 = thread.start_new_thread(self.checkSayHello, (prefix, model, "Peter"))
    t3 = thread.start_new_thread(self.checkSayHello, (prefix, model, "Mary"))
    t4 = thread.start_new_thread(self.checkSayHello, (prefix, model, "Ana"))
    t5 = thread.start_new_thread(self.checkSayHello, (prefix, model, "Guido"))
    t6 = thread.start_new_thread(self.checkSayHello, (prefix, model, "Alan Kay"))
    t7 = thread.start_new_thread(self.checkSayHello, (prefix, model, "Gossling"))

    time.sleep(5)
    """

    model.setPosition([0,0])
    model.setName('')
    print prefix + "Nos suscribimos a eventos"
    assert self.lastEvent == None
    model.subscribeEvent('position', self.eventFired)
    model.subscribeEvent('name',     self.eventFired)
    assert self.lastEvent == None


    print prefix + "Cambiamos la posicion"
    model.setPosition([1,2])
    assert self.lastEvent.getName() == 'position'
    assert self.lastEvent.getProducer() == model
    assert self.lastEvent.getParams()['position'] == [1,2]

    print prefix + "Cambiamos la posicion, nuevamente"
    model.setPosition([2,4])
    assert self.lastEvent.getName() == 'position'
    assert self.lastEvent.getProducer() == model
    assert self.lastEvent.getParams()['position'] == [2,4]

    print prefix + "Cambiamos el nombre"
    model.setName('Guido')
    assert self.lastEvent.getName() == 'name'
    assert self.lastEvent.getProducer() == model
    assert self.lastEvent.getParams()['name'] == 'Guido'

  def eventFired(self, event):
    self.lastEvent = event

  def checkSayHello(self, prefix, model, name):
    result1 = model.sayHello(name)
    print prefix + result1
    assert result1 == ("Hello " + name)

    #time.sleep(random.random() * 0.2)

    result2 = model.fullName(name, "Smith")
    print prefix + result2
    assert result2 == (name + " Smith")


if __name__ == "__main__":
  test = unittest.main()
