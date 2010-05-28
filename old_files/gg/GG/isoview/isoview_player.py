# -*- coding: utf-8 -*- 

import guiobjects
import isoview_item
import isoview
import GG.utils
import animation
import pygame
import os
import GG

# ======================= CONSTANTS ===========================
JUMP_TIME = 800
JUMP_ANIMATION_TIME = 100
JUMP_DISTANCE = 70
JUMP_OVER_DISTANCE = JUMP_DISTANCE + 50
ANCHOR_PLAYER = [2*GG.utils.CHAR_SZ[0]-57, GG.utils.CHAR_SZ[1]-30]
TOPANCHOR_PLAYER = [0, GG.utils.TILE_SZ[1] + ANCHOR_PLAYER[1] - 20]
# =============================================================

class IsoViewPlayer(isoview_item.IsoViewItem):
  """ IsoViewPlayer class.
  Defines a player view.
  """
  
  def __init__(self, model, screen, room, parent):
    """ Class constructor.
    model: observed object.
    screen: screen handler.
    room: the room where the player is.
    parent: isoview_hud handler.
    """
    isoview_item.IsoViewItem.__init__(self, model, screen, room, parent)
    self.anchor = ANCHOR_PLAYER
    self.topAnchor = TOPANCHOR_PLAYER 
    self.__movieAnimation = None
    self.__destination = None
    infoPackage = model.getPlayerBuildPackage()
    self.__timestamp = infoPackage["timestamp"]
    self.__heading = infoPackage["heading"]
    self.__state = infoPackage["state"]
    self.__path = infoPackage["imagepath"]
    self.__getAvatarImages()
    self.loadAvatarImage(self.__path, self.__timestamp)
    subscriptionList = []
    subscriptionList.append(['heading', self.headingChanged])
    subscriptionList.append(['state', self.stateChanged])
    subscriptionList.append(['jump', self.onJump])
    subscriptionList.append(['jumpOver', self.onJumpOver])
    subscriptionList.append(['avatarConfiguration', self.avatarConfigurationChanged])
    subscriptionList.append(['timestamp', self.timestampChanged])
    self.getModel().subscribeListEvent(subscriptionList)

  def __getAvatarImages(self):
    """ Grabs a new set of images for player's avatar. 
    """  
    if not GG.genteguada.GenteGuada.getInstance().isSingleMode():
      if self.__timestamp == "":
        imageAvatar = os.path.join(self.__path, "standing_bottomright_0001")
      else:
        imageAvatar = os.path.join(self.__path, "standing_bottomright_0001_" + self.__timestamp)
      if not os.path.isfile(os.path.join(GG.utils.LOCAL_DATA_PATH, imageAvatar)):
        if not GG.genteguada.GenteGuada.getInstance().isAvatarDownload(self.getModel()):
          self.__path = os.path.join("avatars", "ghost")
          self.__timestamp = ""
          GG.genteguada.GenteGuada.getInstance().getAvatarImages(self.getModel())
      
  def setDestination(self, destination):
    """ Saves a player's destination local copy.
    destination: new destination.
    """  
    self.__destination = destination
  
  def __del__(self):
    """ Class destructor.
    """  
    isoview.IsoView.__del__(self)
    if self.__movieAnimation:
      self.__movieAnimation.stop()

  def avatarConfigurationChanged(self, event):
    """ Unfinished method.
    event: event info.
    """  
    pass

  def getPath(self):
    """ Returns the data path.
    """  
    return self.__path

  def setPath(self, path):
    """ Sets a new data path value.
    path: new data path.
    """  
    self.__path = path

  def timestampChanged(self, event):
    """ Triggers after receiving a timestamp changed method.
    event: event info.
    """  
    GG.genteguada.GenteGuada.getInstance().getAvatarImages(self.getModel())
        
  def headingChanged(self, event):
    """ Changes the player's sprite heading.
    event: event info.
    """
    self.__heading = event.getParams()["heading"]
    if self.__movieAnimation:
      frames = self.createFrameSet()
      self.__movieAnimation.setFrames(frames, self.__path)
    else:
      cad = GG.utils.getSpriteName(event.getParams()["state"], event.getParams()["heading"], 0, self.__timestamp)
      self.setImg(cad, self.__path)
    
  def inventoryAdded(self, event):
    """ Triggers after receiving an inventory added event.
    event: event info.
    """
    self.getParent().addInventoryItem(event.getParams()["item"])
    
  def inventoryRemoved(self, event):
    """ Triggers after receiving an inventory removed event.
    event: event info.
    """
    self.getParent().removeInventoryItem(event.getParams()["item"])

  def hasMovieAnimation(self):
    """ Checks if there is an active animation.
    """
    return self.__movieAnimation != None
      
  def setMovieAnimation(self, anim=None):
    """ Creates a new movie animation.
    anim: new movie animation.
    """
    if self.__movieAnimation:
      self.__movieAnimation.stop()
    self.__movieAnimation = anim
    if anim != None:
      anim.start()
    
  def setMovieFrames(self, frames):
    """ Sets a new frame set for a movie animation.
    frames: new frame set.
    """
    self.__movieAnimation.setFrames(frames, self.__path)
        
  def createFrameSet(self, dataState=None):
    """ Creates a new frame set.
    dataState: player's state.
    """
    frames = []
    if dataState:
      state = dataState
    else:
      state = self.__state
    if state == GG.utils.STATE[1] or state == GG.utils.STATE[3]:
      string = GG.utils.getSpriteName(state, self.__heading, 0, self.__timestamp)
      frames.append(string)
    else:
      for i in range(1, GG.utils.ANIM_WALKING_COUNT+1):
        string = GG.utils.getSpriteName(state, self.__heading, i, self.__timestamp)  
        frames.append(string)        
    return frames
    
  def animatedSetPosition(self, newPosition):
    """ Sets a new position for the player and creates a new movie animation.
    newPosition: new player's position.
    """
    isoview_item.IsoViewItem.animatedSetPosition(self, newPosition)
    movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet(), self.__path)
    self.setMovieAnimation(movieAnim)
    
  def updateFrame(self, elapsedTime):
    """ Paints a new item frame on screen.
    elapsedTime: elapsed time since the game start.
    """
    isoview_item.IsoViewItem.updateFrame(self, elapsedTime)
    if self.__movieAnimation:
      self.__movieAnimation.step(elapsedTime)  
        
  def restoreImageFrame(self):
    """ Restores the player's image according to its state, heading and timestamp.
    """  
    self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0, self.__timestamp), self.__path)
  
  def restoreImagePosition(self):  
    """ Restores the image position.
    """  
    self.setScreenPosition(GG.utils.p3dToP2d(self.getPosition(), self.anchor))
      
  def stopFallingAndRestore(self):    
    """ Stops the falling movie animation and restores player's image frame.
    """  
    self.setMovieAnimation(None)  
    self.setImg(GG.utils.getSpriteName(self.__state, self.__heading, 0, self.__timestamp), self.__path)
        
  def stateChanged(self, event):
    """ Triggers after receiving a new state change event.
    event: event info.
    """  
    st = event.getParams()["state"]
    self.__state = st
    pos = event.getParams()["position"]
    listItemsTile = event.getParams()["listItemsTiles"]
      
    if st == GG.utils.STATE[1] or st == GG.utils.STATE[3]: # standing, standing_carrying 
      self.getParent().removeMovementDestination()
      self.setAnimation(None)
      self.setMovieAnimation(None)  
      self.setImg(GG.utils.getSpriteName(st, self.__heading, 0, self.__timestamp), self.__path)
      self.getIVRoom().updateScreenPositionsOn(pos, listItemsTile)
      
    elif st == GG.utils.STATE[2] or st == GG.utils.STATE[4]: # walking, walking_carrying
      self.setAnimation(None)
      self.setMovieAnimation(None)  
      movieAnim = animation.MovieAnimation(GG.utils.ANIM_WALKING_TIME, self, self.createFrameSet(st), self.__path)
      self.setMovieAnimation(movieAnim)

  def onJump(self, event):
    """ Triggers after receiving a player jump event.
    event: event info.
    """  
    screenPos = self.getScreenPosition()
    movieAnim = animation.MovieAnimation(JUMP_ANIMATION_TIME, self, self.createFrameSet("walking"), self.__path)
    positionUp = animation.ScreenPositionAnimation(JUMP_TIME, self, \
                            screenPos, [screenPos[0],  screenPos[1] - JUMP_DISTANCE], True)
    positionDown = animation.ScreenPositionAnimation(JUMP_TIME, self, \
                            [screenPos[0],  screenPos[1] - JUMP_DISTANCE], screenPos, True)
    secAnim = animation.SecuenceAnimation()
    secAnim.addAnimation(positionUp)
    secAnim.addAnimation(positionDown)
    secAnim.setOnStop(self.stopMovieAnimation, None)
    self.setAnimation(secAnim)
    self.setMovieAnimation(movieAnim)

  def onJumpOver(self, event):
    """ Triggers after receiving a player jumpOver event.
    event: event info.
    """  
    pos1 = event.getParams()['position']
    startPos = self.getScreenPosition()
    endPos = self.getIVRoom().getFutureScreenPosition(self, pos1, event.getParams()['itemList'])
    cordX = (startPos[0] + endPos[0])/2
    cordY = (startPos[1] + endPos[1])/2 - JUMP_OVER_DISTANCE
    halfPos = [cordX, cordY]
    movieAnim = animation.MovieAnimation(JUMP_ANIMATION_TIME, self, self.createFrameSet("walking"), self.__path)
    positionUp = animation.ScreenPositionAnimation(JUMP_TIME, self, \
                            startPos, halfPos, True)
    positionDown = animation.ScreenPositionAnimation(JUMP_TIME, self, \
                            halfPos, endPos, True)
    positionUp.setOnStop(self.setPosition, pos1)
    positionUp.setOnStop(self.updateZOrderFor, pos1)
    secAnim = animation.SecuenceAnimation()
    secAnim.addAnimation(positionUp)
    secAnim.addAnimation(positionDown)
    secAnim.setOnStop(self.stopMovieAnimation, None)
    secAnim.setOnStop(self.getParent().removeMovementDestination, None)
    self.setAnimation(secAnim)
    self.setMovieAnimation(movieAnim)
    
  def stopMovieAnimation(self):
    """ Stops the movie animation.
    """  
    if self.__movieAnimation:
      self.__movieAnimation.stop()
      self.__movieAnimation = None
      self.setImg(GG.utils.getSpriteName(GG.utils.STATE[1], self.__heading, 0, self.__timestamp), self.__path)
      
  def positionChanged(self, event):
    """ Triggers after receiving a position change event.
    event: event info.
    """
    pos = event.getParams()['position']
    oldPos = event.getParams()['oldPosition']
    itemList = event.getParams()['itemList']
    oldItemList = event.getParams()['oldItemList']
    if pos == self.__destination:
      self.getParent().removeMovementDestination()
    tmpPos = GG.utils.p3dToP2d(oldPos, self.anchor)  
    if len(oldItemList) < 2:
      self.setScreenPosition(tmpPos)
    else:  
      self.getIVRoom().updateScreenPositionsOn(oldPos, oldItemList)
    isoview_item.IsoViewItem.positionChanged(self, event)
    
  def changeAvatarImages(self, path, timestamp):
    """ Changes the avatar image path.
    path: new image set path.
    """  
    self.__path = path
    self.__timestamp = timestamp
    self.setImg(GG.utils.getSpriteName(self.__state, self.__heading, 0, self.__timestamp), self.__path)
    
  def unselected(self):
    """ Restores the item's color and sets it as unselected.
    """
    imageName = os.path.join(self.getModel().getImagePath(),self.getModel().getSpriteName())
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(imageName)
    self.setSprite(pygame.image.load(imgPath).convert_alpha())
      
  def isPlayer(self):
    """ Checks if this item is a player or not.
    """  
    return True  
