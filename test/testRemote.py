import sys
import unittest

sys.path.append("../client")
sys.path.append("../common")
#sys.path.append("../server")

import ggclient.remoteclient
import ggcommon.remotemodel
import time

class TestRemoteObject(unittest.TestCase):
 
  def testConnect(self):
    print "Ejecutando test de conexion"
    ipServer = "127.0.0.1"
    client = ggclient.remoteclient.RClient(ipServer)
    time.sleep(1)
    assert client._thread.socket.getpeername()[0] == ipServer 
    
    print "Ejecutando test de root model"
    model = client.getRootModel()
    assert isinstance(model,ggcommon.remotemodel.RemoteModel)
    
    print "Ejecutamos el metodo foo sin argumentos"
    result = model.foo()
    assert result.__class__ == str
    assert result == "foo"

    print "Ejecutamos el metodo bar sin argumentos"
    result = model.bar()
    assert result.__class__ == str
    assert result== "bar"

    print "Obtenemos un modelo a partir del root model"
    player = model.player()
    assert isinstance(player,ggcommon.remotemodel.RemoteModel)

    print "Ejecutamos un metodo del objeto obtenido a partir del root"
    result = player.name()
    assert result.__class__ == str
    assert result == "maradona"

    print "Ejecutamos un metodo del rootModel pasando un parametro"
    param = "Antonio"
    result = model.saluda(param)
    assert result.__class__ == str
    assert result == "Hola "+str(param)

    print "Ejecutamos un metodo del rootModel pasando dos parametros"
    param1 = "Luis"
    param2 = "Garcia"
    result = model.nombreApellidos(param1,param2)
    assert result.__class__ == str
    assert result == param1+ "  "+ param2

    print "Ejecutamos un metodo que nos da una excepcion ya que no se encuentra definido"
    raisedExceptionMethodNoFound = False
    try:
      result = model.name()
    except:
      raisedExceptionMethodNoFound = True
    assert raisedExceptionMethodNoFound == True

    print "Ejecutamos un metodo que nos da una excepcion por error de codigo del metodo 1/0"
    raisedExceptionMethodError = False
    try:
      result = model.metodoError()
    except:
      raisedExceptionMethodError = True
    assert raisedExceptionMethodError == True

    print "ejecutamos un metodo que nos devuelve una lista"
    result = model.listaJugadores()
    assert result.__class__ == list
    for i in range(len(result)):
      assert isinstance(result[i],ggcommon.remotemodel.RemoteModel)
      name = result[i].name()
      assert name == "maradona"
      
    print "ejecutamos un metodo que nos devuelve una tupla"
    result = model.tuplaJugadores()
    assert result.__class__ == tuple
    for i in range(len(result)):
      assert isinstance(result[i],ggcommon.remotemodel.RemoteModel)
      name = result[i].name()
      assert name == "maradona"

    print "ejecutamos un metodo que nos devuelve un diccionario"
    result = model.dictJugadores()
    assert result.__class__ == dict
    for key in result.keys():
      assert isinstance(result[key],ggcommon.remotemodel.RemoteModel)
      name = result[key].name()
      assert name == "maradona"

    print "ejecutamos un metodo pasando por parametro un remotemodel"
    result = model.getName(player)
    assert result == "maradona"

    print "ejecutamos un metodo pasando por parametro una lista de remotemodel"
    result = model.getListName([player])
    assert result == "maradona"

    print "ejecutamos un metodo pasando por parametro una tupla de remotemodel"
    result = model.getTupleName((player,))
    assert result == "maradona"
    
    print "ejecutamos un metodo pasando por parametro una diccionario de remotemodel"
    result = model.getDictName({"1":player})
    assert result == "maradona"

if __name__ == "__main__":
  test = unittest.main()
