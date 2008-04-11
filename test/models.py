import sys

sys.path.append("../server")

import ggserver.model


class TestPlayer(ggserver.model.Model): #{{{
    
  def __init__(self):
    ggserver.model.Model.__init__(self)

  def name(self):
    return 'maradona'
#}}}

class TestModel(ggserver.model.Model): #{{{
    
  def __init__(self):
    ggserver.model.Model.__init__(self)
    self._player = TestPlayer()
    self._position = [0,0]
    self._name = ''

  def setPosition(self, position):
      if self._position == position:
          return

      self._position = position
      self.triggerEvent('position', position=self.getPosition())

  def getPosition(self):
      return self._position

  def setName(self, name):
      if self._name == name:
          return

      self._name = name
      self.triggerEvent('name', name=self.getMyName())

  def getMyName(self):
      return self._name


  def foo(self):
    return 'foo'

  def bar(self):
    return 'bar'

  def player(self):
    return self._player

  def sayHello(self,name):
    return "Hello " + name

  def metodoError(self):
    result = 1/0
    return result

  def fullName(self, name, lastName):
    return name + " " + lastName

  def listPlayers(self):
    return [TestPlayer(), TestPlayer()]

  def tuplePlayers(self):
    return (TestPlayer(), TestPlayer())

  def dictPlayers(self):
    return {"1":TestPlayer(), "2":TestPlayer()}

  def getName(self,player):
    return player.name()

  def getListName(self,listplayer):
    return listplayer[0].name()

  def getTupleName(self,tupleplayer):
    return tupleplayer[0].name()

  def getDictName(self,dictplayer):
    for key in dictplayer.keys():
      name = dictplayer[key].name()
    return name


#}}}
