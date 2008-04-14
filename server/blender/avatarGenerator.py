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
	Blender.Redraw()

#Situa el tipo de peinado en la capa 1 para ser renderizado
#def hairSelection(typeHair):
#	hair = Blender.Object.Get(typeHair)
#	hair.layers = [1]
	
#Escala el objeto dentro de unos limites minimos y maximos
def scaleObject(nameObject, dimX, dimY, dimZ):
  obj = Blender.Object.Get(nameObject)
  print obj.getSize()
  print  obj.SizeX + dimX
  obj.SizeX = obj.SizeX + dimX
  print  obj.SizeY + dimY
  obj.SizeY = obj.SizeY + dimY
  print  obj.SizeZ + dimZ
  obj.SizeZ = obj.SizeZ + dimZ
  Blender.Redraw()
  print obj.getSize()

#Escala el objeto proporcionalemente a la imagen pasada por parametro
def scaleProportionalObject(nameObject, face):
	image = Blender.Image.Load(face)
	width = image.getSize()[0]
	height = image.getSize()[1]

	if height >= width:
		proportion = float(width) / float(height)
		newWidth = 1 * proportion
		newHeight = 1 
	else:
		proportion = float(height) / float(width)
		newWidth = 1
		newHeight = 1 * proportion
	print width,height,proportion,newWidth,newHeight
	scaleObject(nameObject, newWidth, newWidth, newHeight)
	


#Asignacion de argumentos a las variables locales
gender = os.getenv('gender')
headSize = os.getenv('headSize')
mask = os.getenv('mask')
hair = os.getenv('hair')
skin = os.getenv('skin')
bodySize = os.getenv('bodySize')
sleeve = os.getenv('sleeve')
shirt = os.getenv('shirt')
typeTrousers = os.getenv('typeTrousers')
trousers = os.getenv('trousers')
skirt = os.getenv('skirt')
shoes = os.getenv('shoes')

if gender == "male":
	print "Genero seleccionado male"
	avatar= "boy"
	avatarParts = ["boyCenter", "boyHead", "boyHair", "boyMask", "boyBody", "boyLeftArm", "boyRightArm", "boyLeftLeg", "boyRightLeg"]
elif gender == "female":
	print "Genero seleccionado female"
	avatar = "girl"
	avatarParts = ["girlCenter", "girlHead", "girlHair", "girlMask", "girlBody", "girlLeftArm", "girlRightArm", "girlLeftLeg", "girlRightLeg"]

#Activamos el avatar seleccionado en la capa 1 para realizar el render	
for part in avatarParts:
  obj = Blender.Object.Get(part)
  obj.layers = [1]


if headSize <> "":
	print "headSize=",headSize
	valueSizeDefault = 0
	valueSize = 0
	if headSize == "L":
		print "Cambiamos tamaño cabeza L"
 		valueSize = 0.1
	elif headSize == "M":
		print "Cambiamos tamaño cabeza M"
 		valueSize = 0.2
	elif headSize == "XL":
		print "Cambiamos tamaño cabeza XL"
 		valueSize = 0.3
	scaleObject(avatar + "Head", valueSize, valueSize, valueSize)
	scaleObject(avatar + "Hair", valueSize, valueSize, valueSize)
	scaleObject(avatar + "Mask",valueSize, valueSize, valueSize)

if mask <> "":
	print "Cambiamos textura careta"
	texturePath = mask
	changeTexture(avatar + "Mask", texturePath, "defaultMask.tga")
	
if hair <> "":
  print "Cambiamos textura pelo"
  texturePath = os.path.join(os.path.abspath("."), "textures/" + gender + "/hair/" + hair)
  changeTexture(avatar + "Hair", texturePath, "defaultHair.tga")
	
if skin <> "":
  print "Cambiamos textura piel"
  texturePath = os.path.join(os.path.abspath("."), "textures/" + gender +"/skin/" + skin)
  changeTexture(avatar + "Head", texturePath, "defaultSkin.tga")
  changeTexture(avatar + "LeftArm", texturePath, "defaultSkin.tga")
  changeTexture(avatar + "RightArm", texturePath, "defaultSkin.tga")
  if gender == "female":
		changeTexture(avatar + "LeftLeg", texturePath, "undefined.tga")
		changeTexture(avatar + "RightLeg", texturePath, "undefined.tga")

if bodySize <> "":
	valueSizeDefault = 0
	valueSize = 0
	if bodySize == "L":
		print "Cambiamos tamaño cuerpo L"
 		valueSize = 0.1
	elif bodySize == "M":
		print "Cambiamos tamaño cuerpo M"
 		valueSize = 0.2
	elif bodySize == "XL":
		print "Cambiamos tamaño cuerpo XL"
 		valueSize = 0.3
	scaleObject(avatar + "Body", valueSize, valueSizeDefault, valueSize)
	scaleObject(avatar + "LeftArm", valueSize, valueSizeDefault, valueSize)
	scaleObject(avatar + "RightArm",valueSize, valueSizeDefault, valueSize)
	scaleObject(avatar + "LeftLeg", valueSize, valueSize, valueSize)
	scaleObject(avatar + "RightLeg", valueSize, valueSize, valueSize)
	
if shirt <> "" and gender == "male":
  print "Cambiamos textura cuerpo chico"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
  changeTexture("boyBody", texturePath, "defaultShirt.tga")

if skirt <> "" and gender == "female":
  print "Cambiamos textura cuerpo chica"
  texturePath = os.path.join(os.path.abspath("."), "textures/female/skirt/" + skirt)
  changeTexture("girlBody", texturePath, "defaultSkirt.tga")
	
if sleeve == "0":  #Manga corta
	print "Cambiamos textura manga corta"
	if gender == "male":
		texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
		changeTexture("boyLeftArm", texturePath, "defaultShirt.tga")
		changeTexture("boyRightArm", texturePath, "defaultShirt.tga")
	elif gender == "female":
		texturePath = os.path.join(os.path.abspath("."), "textures/female/skirt/" + shirt)
		changeTexture("girlLeftArm", texturePath, "defaultSkirt.tga")
		changeTexture("girlRightArm", texturePath, "defaultSkirt.tga")

	if skin <> "":		
		texturePath = os.path.join(os.path.abspath("."), "textures/" + gender + "/skin/" + skin)
		changeTexture(avatar + "LeftArm", texturePath, "undefined.tga")
		changeTexture(avatar + "RightArm", texturePath, "undefined.tga")
		
elif sleeve == "1": #Manga larga
	print "Cambiamos textura manga larga"
	if gender == "male":
		texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
		changeTexture("boyLeftArm", texturePath, "defaultShirt.tga")
		changeTexture("boyRightArm", texturePath, "defaultShirt.tga")
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
	
if typeTrousers == "0" and gender == "male":
	#Pantalon corto
	print "Cambiamos textura pantalon corto"
	texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
	changeTexture("boyLeftLeg", texturePath, "defaultTrousers.tga")
	changeTexture("boyRightLeg", texturePath, "defaultTrousers.tga")
	if skin <> "": 
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/skin/" + skin)
	  changeTexture("boyLeftLeg", texturePath, "undefined.tga")
	  changeTexture("boyRightLeg", texturePath, "undefined.tga")
elif typeTrousers == "1" and gender == "male":
	#Pantalon largo
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
  rotateObject(avatar + "Center", rot)
  if rot == 0:
	  renderScene("avatarS.png")
#  elif rot == 45:
#	  renderScene("avatarSO.png")
#  elif rot == 90:
#	  renderScene("avatarO.png")
#  elif rot == 135:
#	  renderScene("avatarNO.png")
#  elif rot == 180:
#	  renderScene("avatarN.png")
#  elif rot == 225:
#	  renderScene("avatarNE.png")
#  elif rot == 270:
#	  renderScene("avatarE.png")
#  elif rot == 315:
#	  renderScene("avatarSE.png")



