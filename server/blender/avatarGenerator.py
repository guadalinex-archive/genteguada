import Blender.Object
import Blender.Scene
import Blender.Mesh
import Blender.Image
import Blender.Scene
import Blender.Draw
import os

#Rotamos el objeto tantos grados como señala el parametro de entrada
def rotateObject(nameObject,rotation):
  obj = Blender.Object.Get(nameObject)
  obj.RotZ = float(rotation) * (3.1416/180)		#Convertimos a radianes

#Renderiza la escena
def renderScene(renderFileName):
  scn = Blender.Scene.GetCurrent()
  context = scn.getRenderingContext()
  context.setRenderPath(os.path.join("imagesGenerated/"))
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
def changeTexture(objectName,pathNewTexture,defaultTexture):  
	if gender == "female":
		defaultTexture = "g" + defaultTexture[0].upper() + defaultTexture[1:]
	newTexture = Blender.Image.Load(pathNewTexture)
	me = Blender.Mesh.Get(objectName)
	faces = me.faces
	for f in faces:
		if f.image.getName() == defaultTexture:
			f.image = newTexture

#Situa el tipo de peinado en la capa 1 para ser renderizado
def hairSelection(typeHair):
	hair = Blender.Object.Get(typeHair)
	hair.layers = [1]
	
#Escala el objeto dentro de unos limites minimos y maximos
def scaleObject(nameObject, dimX, dimY, dimZ):
  obj = Blender.Object.Get(nameObject)
  if float(dimX) >= 1 and float(dimX) <= 2:
		print "escalamos X"
	  #size = (float(dimX),) + size[1:]
		obj.SizeX = float(dimX)
  if float(dimY) >= 1 and float(dimY) <= 2:
		print "escalamos Y"
		#auxsize = size
		#size = size[:1] + (float(dimY),) + auxsize[-1:]
		obj.SizeY = float(dimY)
  if float(dimZ) >= 1 and float(dimZ) <= 1.2:
    print "escalamos Z"
    #size = size[:2] + (float(dimZ),)
    obj.SizeZ = float(dimZ)
  Blender.Redraw()


#Asignacion de argumentos a las variables locales

gender = os.getenv('gender')
dimX = os.getenv('dimX')
dimY = os.getenv('dimY')
dimZ = os.getenv('dimZ')
face = os.getenv('face')
hair = os.getenv('hair')
skin = os.getenv('skin')
sleeve = os.getenv('sleeve')
shirt = os.getenv('shirt')
typetrousers = os.getenv('typetrousers')
trousers = os.getenv('trousers')
skirt = os.getenv('skirt')
shoes = os.getenv('shoes')

if gender == "male":
	print "Genero seleccionado male"
	avatar= "boy"
	avatarParts = ["boyHead","boyBody","boyLeftArm","boyRightArm","boyLeftLeg","boyRightLeg"]
elif gender == "female":
	print "Genero seleccionado female"
	avatar = "girl"
	avatarParts = ["girlHead","girlBody","girlLeftArm","girlRightArm","girlLeftLeg","girlRightLeg"]

#Activamos el avatar seleccionado en la capa 1 para realizar el render	
for part in avatarParts:
  obj = Blender.Object.Get(part)
  obj.layers = [1]


if dimX <> "" and dimY <> "" and dimZ <> "":
  print "Escalamos cabeza"
  scaleObject(avatar + "Head",dimX,dimY,dimZ)

if face <> "":
  print "Cambiamos textura cara"
  texturePath = face
  objectName = avatar + "Head"
  changeTexture(objectName, texturePath, "defaultFace.tga")
	
if hair <> "":
  print "Cambiamos textura pelo"
  texturePath = os.path.join(os.path.abspath("."), "textures/" + gender + "/hair/" + hair)
  changeTexture(avatar + "Head", texturePath, "defaultHair.tga")
	
if skin <> "":
  print "Cambiamos textura piel"
  texturePath = os.path.join(os.path.abspath("."), "textures/" + gender +"/skin/" + skin)
  changeTexture(avatar + "Head", texturePath, "defaultFaceSkin.tga")
  changeTexture(avatar + "LeftArm", texturePath, "defaultSkin.tga")
  changeTexture(avatar + "RightArm", texturePath, "defaultSkin.tga")
  changeTexture(avatar + "LeftLeg", texturePath, "defaultSkin.tga")
  changeTexture(avatar + "RightLeg", texturePath, "defaultSkin.tga")
	
if shirt <> "" and gender == "male":
  print "Cambiamos textura cuerpo chico"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
  changeTexture("boyBody", texturePath, "defaultShirt.tga")

if skirt <> "" and gender == "female":
  print "Cambiamos textura cuerpo chica"
  texturePath = os.path.join(os.path.abspath("."), "textures/female/skirt/" + skirt)
  changeTexture("girlBody", texturePath, "defaultSkirt.tga")
	
if sleeve == "0":  #Manga corta
	if skin <> "":
		print "Cambiamos textura manga corta"
		if gender == "male":
			texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
			changeTexture("boyLeftArm", texturePath, "defaultShirt.tga")
			changeTexture("boyRightArm", texturePath, "defaultShirt.tga")
		elif gender == "female":
			texturePath = os.path.join(os.path.abspath("."), "textures/female/skirt/" + shirt)
			changeTexture("girlLeftArm", texturePath, "defaultSkirt.tga")
			changeTexture("girlRightArm", texturePath, "defaultSkirt.tga")
		
		texturePath = os.path.join(os.path.abspath("."), "textures/" + gender + "/skin/" + skin)
		changeTexture(avatar + "LeftArm", texturePath, "undefined.tga")
		changeTexture(avatar + "RightArm", texturePath, "undefined.tga")
		
elif sleeve == "1": #Manga larga
	if skin <> "": 
		print "Cambiamos textura manga larga"
		if gender == "male":
			texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
			changeTexture("boyLeftArm", texturePath, "defaultShirt.tga")
			changeTexture("boyRightArm", texturePath, "defaultShirt.tga")
			changeTexture(avatar + "LeftArm", texturePath, "undefined.tga")
			changeTexture(avatar + "RightArm", texturePath, "undefined.tga")
		elif gender == "female":
			texturePath = os.path.join(os.path.abspath("."), "textures/female/skirt/" + skirt)
			changeTexture("girlLeftArm", texturePath, "defaultSkirt.tga")
			changeTexture("girlRightArm", texturePath, "defaultSkirt.tga")
			changeTexture(avatar + "LeftArm", texturePath, "undefined.tga")
			changeTexture(avatar + "RightArm", texturePath, "undefined.tga")
	
if trousers <> "":
  print "Cambiamos textura pantalon"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
  changeTexture("boyBody", texturePath, "defaultTrousers.tga")
	
if typetrousers == "0" and gender == "male":
	if skin <> "": #Pantalon corto
	  print "Cambiamos textura pantalon corto"
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
	  changeTexture("boyLeftLeg", texturePath, "defaultTrousers.tga")
	  changeTexture("boyRightLeg", texturePath, "defaultTrousers.tga")
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/skin/" + skin)
	  changeTexture("boyLeftLeg", texturePath, "undefined.tga")
	  changeTexture("boyRightLeg", texturePath, "undefined.tga")
elif typetrousers == "1" and gender == "male":
	if skin <> "": #Pantalon largo
	  print "Cambiamos textura pantalon largo"
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
	  changeTexture("boyLeftLeg", texturePath, "defaultTrousers.tga")
	  changeTexture("boyRightLeg", texturePath, "defaultTrousers.tga")
	  changeTexture("boyLeftLeg", texturePath, "undefined.tga")
	  changeTexture("boyRightLeg",texturePath,"undefined.tga")
	
if shoes <> "":
  print "Cambiamos textura zapatos"
  texturePath = os.path.join(os.path.abspath("."), "textures/" + gender + "/shoes/" + shoes)
  changeTexture(avatar + "LeftLeg", texturePath, "defaultShoes.tga")
  changeTexture(avatar + "RightLeg", texturePath, "defaultShoes.tga")
	
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




