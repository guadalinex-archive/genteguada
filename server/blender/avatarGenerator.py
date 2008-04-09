import Blender.Object
import Blender.Scene
import Blender.Mesh
import Blender.Image
import Blender.Scene
import os

#Rotamos el objeto tantos grados como señala el parametro de entrada
def rotateObject(nameObject,rotation):
  obj = Blender.Object.Get(nameObject)
  obj.RotZ = float(rotation) * (3.1416/180)		#Convertimos a radianes

#Renderiza la escena
def renderScene(renderFileName):
  scn = Blender.Scene.GetCurrent()
  context = scn.getRenderingContext()
  context.setRenderPath(os.path.join("imagesGenerated/"))#/home/edu/Documentos/GenteGuada/subversion/server/blender/imagesGenerated/')
  context.imageType = Blender.Scene.Render.PNG  
  context.sFrame = 1
  context.eFrame = 1
  context.render()	

  #Renombra la imagen renderizada
  defaultFileName = "0001.png"
  try:
		print "Rendered Image renamed to", renderFileName
		os.rename(context.getRenderPath() + defaultFileName, context.getRenderPath() + renderFileName)
  except:
		pass

#Cambia la textura del objeto
def changeTexture(nameObject,pathNewTexture,defaultTexture):  
	newTexture = Blender.Image.Load(pathNewTexture)
	me = Blender.Mesh.Get(nameObject)
	faces = me.faces
	for f in faces:
		if f.image.getName() == defaultTexture:
			f.image = newTexture

#Situa el tipo de peinado en la capa 1 para ser renderizado
def hairSelection(typeHair):
	hair = Blender.Object.Get(typeHair)
	hair.layers = [1]
	
#Escala el objeto dentro de unos limites minimos y maximos
def scaleObject(nameObject,scaleX,scaleY,scaleZ):
  obj = Blender.Object.Get(nameObject)
  if float(scaleX) > 0.5 and float(scaleX) < 0.8:
    obj.SizeX = float(scaleX)
  if float(scaleY) > 0.5 and float(scaleY) < 0.6:
    obj.SizeY = float(scaleY)
  if float(scaleZ) > 0.5 and float(scaleZ) < 0.6:
    obj.SizeZ = float(scaleZ)

#Asignacion de argumentos a las variables locales
scaleX = os.getenv('scaleX')
scaleY = os.getenv('scaleY')
scaleZ = os.getenv('scaleZ')
face = os.getenv('face')
hair = os.getenv('hair')
skin = os.getenv('skin')
typeshirt = os.getenv('typeshirt')
shirt = os.getenv('shirt')
typetrousers = os.getenv('typetrousers')
trousers = os.getenv('trousers')
shoes = os.getenv('shoes')

if scaleX <> "" and scaleY <> "" and scaleZ <> "":
  print "Escalamos cabeza"
  scaleObject("boyHeadSquare",scaleX,scaleY,scaleZ)

if face <> "":
  print "Cambiamos textura cara"
  texturePath = face
  changeTexture("boyHead",texturePath,"defaultFace.tga")
	
if hair <> "":
  print "Cambiamos textura pelo"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/hair/" + hair)
  changeTexture("boyHead",texturePath,"defaultHair.tga")
	
if skin <> "":
  print "Cambiamos textura piel"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/skin/" + skin)
  changeTexture("boyHead",texturePath,"defaultFaceSkin.tga")
  changeTexture("boyLeftArm",texturePath,"defaultSkin.tga")
  changeTexture("boyRightArm",texturePath,"defaultSkin.tga")
  changeTexture("boyLeftLeg",texturePath,"defaultSkin.tga")
  changeTexture("boyRightLeg",texturePath,"defaultSkin.tga")
	
if shirt <> "":
  print "Cambiamos textura cuerpo"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
  changeTexture("boyBody",texturePath,"defaultShirt.tga")
	
if typeshirt == "0":  #Camisa de manga corta
	if skin <> "":
	  print "Cambiamos textura camiseta corta"
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
	  changeTexture("boyLeftArm",texturePath,"defaultShirt.tga")
	  changeTexture("boyRightArm",texturePath,"defaultShirt.tga")
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/skin/" + skin)
	  changeTexture("boyLeftArm",texturePath,"undefined.tga")
	  changeTexture("boyRightArm",texturePath,"undefined.tga")
else: #Camisa de manga larga
	if skin <> "": 
	  print "Cambiamos textura camiseta larga"
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
	  changeTexture("boyLeftArm",texturePath,"defaultShirt.tga")
	  changeTexture("boyRightArm",texturePath,"defaultShirt.tga")
	  changeTexture("boyLeftArm",texturePath,"undefined.tga")
	  changeTexture("boyRightArm",texturePath,"undefined.tga")
	
if trousers <> "":
  print "Cambiamos textura pantalon"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
  changeTexture("boyBody",texturePath,"defaultTrousers.tga")
	
if typetrousers == "0":
	if skin <> "": #Pantalon corto
	  print "Cambiamos textura pantalon corto"
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
	  changeTexture("boyLeftLeg",texturePath,"defaultTrousers.tga")
	  changeTexture("boyRightLeg",texturePath,"defaultTrousers.tga")
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/skin/" + skin)
	  changeTexture("boyLeftLeg",texturePath,"undefined.tga")
	  changeTexture("boyRightLeg",texturePath,"undefined.tga")
else:
	if skin <> "": #Pantalon largo
	  print "Cambiamos textura pantalon largo"
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
	  changeTexture("boyLeftLeg",texturePath,"defaultTrousers.tga")
	  changeTexture("boyRightLeg",texturePath,"defaultTrousers.tga")
	  changeTexture("boyLeftLeg",texturePath,"undefined.tga")
	  changeTexture("boyRightLeg",texturePath,"undefined.tga")
	
if shoes <> "":
  print "Cambiamos textura zapatos"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/shoes/" + shoes)
  changeTexture("boyLeftLeg",texturePath,"defaultShoes.tga")
  changeTexture("boyRightLeg",texturePath,"defaultShoes.tga")
	
#Generamos una imagen por cada rotacion del personaje
rotations = [0, 45, 90, 135, 180, 225, 270, 315]
for rot in rotations:
  rotateObject("boyBody",rot)
  rotateObject("boyHead",rot)
  if rot == 0:
	  renderScene("avatarS.png")
  elif rot == 45:
	  renderScene("avatarSO.png")
  elif rot == 90:
	  renderScene("avatarO.png")
  elif rot == 135:
	  renderScene("avatarNO.png")
  elif rot == 180:
	  renderScene("avatarN.png")
  elif rot == 225:
	  renderScene("avatarNE.png")
  elif rot == 270:
	  renderScene("avatarE.png")
  elif rot == 315:
	  renderScene("avatarSE.png")




