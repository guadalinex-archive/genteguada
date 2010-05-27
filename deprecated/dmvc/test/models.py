import sys
import dMVC.model

class TestPlayer(dMVC.model.Model): #{{{
    
  def __init__(self):
    dMVC.model.Model.__init__(self)
    self.constHeredada = "Constante heredada"

  def variablesToSerialize(self):
    return ['constHeredada']

  @dMVC.model.localMethod
  def getConstHeredada(self):
    return self.constHeredada

  def name(self):
    return 'maradona'

  @dMVC.model.localMethod
  def localMethod(self):
    print '----> executing model local method in ' + str(self)

#}}}

class TestSubPlayer(TestPlayer):
  
  def __init__(self):
    TestPlayer.__init__(self)
    self.noFunciona = "PUFF"

  def variablesToSerialize(self): 
    return TestPlayer.variablesToSerialize(self) + ['noFunciona']

class TestModel(dMVC.model.Model): #{{{
    
  def __init__(self):
    dMVC.model.Model.__init__(self)
    self._player = TestPlayer()
    self._subPlayer = TestSubPlayer()
    self._position = [0,0]
    self._name = ''
    self._constant = 'CONSTANT'

  def variablesToSerialize(self):
    return ['_constant']

  @dMVC.model.localMethod
  def getConstant(self):
    return self._constant

  def getSubPlayer(self):
    return self._subPlayer

  def getListPlayer(self):
    return self._listPlayer

  def newPlayer(self,player):
    self._listPlayer.remove(player)

  def deletePlayer(self,player):
    self._listPlayer.append(player)

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


  @dMVC.model.localMethod
  def localFunctionExecution(self, func):
    func()

#}}}
