import model

class TestPlayer(model.Model): #{{{
    
  def __init__(self):
    model.Model.__init__(self)

  def name(self):
    print 'server side execution of name'
    return 'maradona'
#}}}

class TestModel(model.Model): #{{{
    
  def __init__(self):
    model.Model.__init__(self)
    self._player = TestPlayer()

  def foo(self):
    print 'server side execution of foo'
    return 'foo'

  def bar(self):
    print 'server side execution of bar'
    return 'bar'

  def player(self):
    print 'server side execution of player'
    return self._player

  def saluda(self,name):
    return  "Hola "+name

  def metodoError(self):
    result = 1/0
    return result

  def nombreApellidos(self,nombre,apellidos):
    return nombre +"  "+apellidos

  def listaJugadores(self):
    return [TestPlayer(),TestPlayer()]

  def tuplaJugadores(self):
    return (TestPlayer(),TestPlayer())

  def dictJugadores(self):
    return {"1":TestPlayer(),"2":TestPlayer()}

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

