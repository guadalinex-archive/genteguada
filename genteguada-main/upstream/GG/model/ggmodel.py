# -*- coding: utf-8 -*-

import dMVC.model
import os
import GG.utils
import weakref
import pickle
import glob
import sys
import GG.utils 

SAVE_DATA_ROOM = os.path.join(GG.utils.SAVE_DATA, "rooms")
SAVE_DATA_PLAYER = os.path.join(GG.utils.SAVE_DATA, "players")
MODEL_ID_FILE = os.path.join(GG.utils.SAVE_DATA, "modelid.txt")

try:
  f = open(MODEL_ID_FILE, "r")
  ID = int(f.read())
  f.close()
except:
  ID = 0

class EmptyClass:
  pass

class GGModel(dMVC.model.Model):
  """ Model class.
  Defines a generic model, its attributes and behaviour.
  """
 
  def __init__(self):
    """ Class constructor.
    """
    dMVC.model.Model.__init__(self)
    self.idModel = self.__getModelId()
    GGModel.instances[self.idModel] = self

  @staticmethod
  def readAll(obj):
    instanceList = []
    if obj == "room":
      listFile = glob.glob(SAVE_DATA_ROOM + os.sep + "*.serialized")
    else:
      listFile = glob.glob(SAVE_DATA_PLAYER + os.sep + "*.serialized")
    for file in listFile:
      filePath, fileName = os.path.split(file)
      idModel, extFile = os.path.splitext(fileName) 
      instanceList.append(GGModel.read(idModel, obj))
    return instanceList

  @staticmethod
  def read(id, obj, dict = None):
    #syncronizar el acceso a Model.instances
    #if (GGModel.instances.has_key(id)):
    #  return GGModel.instances[id]
    if not dict:
      if obj == "room":
        fileSerialized = os.path.join(SAVE_DATA_ROOM, str(id)+".serialized")
      else:
        fileSerialized = os.path.join(SAVE_DATA_PLAYER, str(id)+".serialized")
      try:
        f = open(fileSerialized, "r")
        dict = pickle.load(f)
        f.close()
      except:
        return None
    __import__(dict["module"])
    mod = sys.modules[dict["module"]]
    klass = getattr(mod, dict["class"])
    instance = EmptyClass()
    instance.__class__ = klass
    instance.load(dict)
    #syncronizar el acceso a Model.instances
    #GGModel.instances[id] = instance
    return instance

  def __getModelId(self):
    global ID 
    ID += 1
    try:
      f = open(MODEL_ID_FILE, "w")
      f.write(str(ID))
      f.close()
    except:
      pass
    return ID

  def save(self, obj):
    if obj == "room":
      fileSerialized = os.path.join(SAVE_DATA_ROOM, str(self.idModel) + ".serialized")
    else:
      fileSerialized = os.path.join(SAVE_DATA_PLAYER, str(self.username) + ".serialized")
    f = open(fileSerialized, "w")
    pickle.dump(self.objectToPersist(), f)

  def objectToPersist(self):
    return {
            "id": self.idModel,
            "class": self.__class__.__name__,
            "module": self.__class__.__module__
            }

  def load(self, dict):
    self.idModel = dict["id"] 
    dMVC.model.Model.__init__(self)

  def deleteObject(self, obj):
    if obj == "room":
      fileSerialized = os.path.join(SAVE_DATA_ROOM, str(self.idModel) + ".serialized")
    else:
      fileSerialized = os.path.join(SAVE_DATA_PLAYER, str(self.username) + ".serialized")
    os.remove(fileSerialized)

  def getPosition(self):
    """ Returns item's default position.
    """  
    return [0, 0]
  
  @dMVC.model.localMethod
  def defaultView(self):
    raise Exception("Metodo no definido en los hijos")
  
GGModel.instances = weakref.WeakValueDictionary()
