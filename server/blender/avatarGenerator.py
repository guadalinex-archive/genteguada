import Blender.Object
import Blender.Scene
import Blender.Mesh
import Blender.Image
import Blender.Scene
import Blender.Draw
import os

#The object rotate so many deegrees as the parameter rotation 
def rotateObject(nameObject,rotation):
	print "ROTAMOS EL OBJETO",nameObject, rotation
	obj = Blender.Object.Get(nameObject)
	obj.RotZ = float(rotation) * (3.1416/180)		#Convert degrees to radians

#Renderize the scene
def renderScene(renderPath, startFrame, endFrame):
  scn = Blender.Scene.GetCurrent()
  context = scn.getRenderingContext()
  if os.path.exists(renderPath) == False:
	  print "folder ", renderPath, "was created"
	  os.mkdir(renderPath)
  else:
		print "folder ", renderPath, "already exist"
  context.setRenderPath(os.path.join(renderPath))
  print "apcth actual", context.getRenderPath()
  context.imageType = Blender.Scene.Render.PNG  
  context.sFrame = startFrame
  context.eFrame = endFrame
  context.renderAnim()	

  #Rename the rendered image
#  defaultFileName = "0001.png"
#  try:
#		print "Rendered Image renamed to", renderFileName
#		os.rename(context.getRenderPath() + defaultFileName, context.getRenderPath() + renderFileName)
#  except:
#		pass

#Update the texture object
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
	
#Escale the axis of the object as parameters
def scaleObject(nameObject, dimX, dimY, dimZ):
  obj = Blender.Object.Get(nameObject)
  obj.SizeX = obj.SizeX + dimX
  obj.SizeY = obj.SizeY + dimY
  obj.SizeZ = obj.SizeZ + dimZ
  Blender.Redraw()

#DEPRECATED: Escale the object proportionally to parameter 
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
	
	
	
#Asign the arguments to local variables
gender = os.getenv('gender')
headSize = os.getenv('headSize')
mask = os.getenv('mask')
hairStyle = os.getenv('hairStyle')
hairColour = os.getenv('hairColour')
skin = os.getenv('skin')
bodySize = os.getenv('bodySize')
sleeve = os.getenv('sleeve')
shirt = os.getenv('shirt')
typeTrousers = os.getenv('typeTrousers')
trousers = os.getenv('trousers')
skirt = os.getenv('skirt')
shoes = os.getenv('shoes')

if gender == "male":
	print "Gender selected male"
	avatar= "boy"
	avatarParts = ["boyHead", "boyHair" + hairStyle, "boyMask", "boyBody", "boyLeftArm", "boyRightArm", "boyLeftLeg", "boyRightLeg"]
elif gender == "female":
	print "Gender selected female"
	avatar = "girl"
	avatarParts = ["girlHead", "girlHair" + hairStyle, "girlMask", "girlBody", "girlLeftArm", "girlRightArm", "girlLeftLeg", "girlRightLeg"]


#Active the selected avatar to layer 1 to render	
for part in avatarParts:
  obj = Blender.Object.Get(part)
  obj.layers = [1]


if headSize <> "":
	valueSizeDefault = 0
	valueSize = 0
	if headSize == "L":
		print "Head size selected L"
 		valueSize = 0.1
	elif headSize == "M":
		print "Head size selected M"
 		valueSize = 0.2
	elif headSize == "XL":
		print "Head size selected XL"
 		valueSize = 0.3
	scaleObject(avatar + "Head", valueSize, valueSize, valueSize)
	if hairStyle <> "0":
		scaleObject(avatar + "Hair" + hairStyle, valueSize, valueSize, valueSize)
	scaleObject(avatar + "Mask",valueSize, valueSize, valueSize)

if mask <> "":
	print "Mask texture updated"
	texturePath = mask
	changeTexture(avatar + "Mask", texturePath, "defaultMask.tga")
	
if hairColour <> "" and hairStyle <> "":
  print "Hair texture updated"
  texturePath = os.path.join(os.path.abspath("."), "textures/" + gender + "/hair/" + hairColour)
  changeTexture(avatar + "Hair" + hairStyle, texturePath, "defaultHair.tga")
	
if skin <> "":
  print "Skin texture updated"
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
		print "Body size selected L"
 		valueSize = 0.1
	elif bodySize == "M":
		print "Body size selected M"
 		valueSize = 0.2
	elif bodySize == "XL":
		print "Body size selected XL"
 		valueSize = 0.3
	scaleObject(avatar + "Body", valueSize, valueSizeDefault, valueSize)
	scaleObject(avatar + "LeftArm", valueSize, valueSizeDefault, valueSize)
	scaleObject(avatar + "RightArm",valueSize, valueSizeDefault, valueSize)
	scaleObject(avatar + "LeftLeg", valueSize, valueSize, valueSize)
	scaleObject(avatar + "RightLeg", valueSize, valueSize, valueSize)
	
if shirt <> "" and gender == "male":
  print "Shirt texture updated"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
  changeTexture("boyBody", texturePath, "defaultShirt.tga")

if skirt <> "" and gender == "female":
  print "Skirt texture updated"
  texturePath = os.path.join(os.path.abspath("."), "textures/female/skirt/" + skirt)
  changeTexture("girlBody", texturePath, "defaultSkirt.tga")
	
if sleeve == "0":  #Short sleeve
	print "Short sleeve selected"
	if gender == "male" and shirt <> "":
		texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
		changeTexture("boyLeftArm", texturePath, "defaultShirt.tga")
		changeTexture("boyRightArm", texturePath, "defaultShirt.tga")
	elif gender == "female" and skirt <> "":
		texturePath = os.path.join(os.path.abspath("."), "textures/female/skirt/" + skirt)
		changeTexture("girlLeftArm", texturePath, "defaultSkirt.tga")
		changeTexture("girlRightArm", texturePath, "defaultSkirt.tga")

	if skin <> "":		
		texturePath = os.path.join(os.path.abspath("."), "textures/" + gender + "/skin/" + skin)
		changeTexture(avatar + "LeftArm", texturePath, "undefined.tga")
		changeTexture(avatar + "RightArm", texturePath, "undefined.tga")
		
elif sleeve == "1": #Long sleeve
	print "Long sleeve selected"
	if gender == "male":
		if shirt == "":
	 	  texturePath = os.path.join(os.path.abspath("."), "textures/male/default/defaultShirt.tga")
		else:
		  texturePath = os.path.join(os.path.abspath("."), "textures/male/shirt/" + shirt)
		changeTexture("boyLeftArm", texturePath, "defaultShirt.tga")
		changeTexture("boyRightArm", texturePath, "defaultShirt.tga")
	elif gender == "female":
		if skirt == "":
	 	  texturePath = os.path.join(os.path.abspath("."), "textures/female/default/gDefaultSkirt.tga")
		else:
		  texturePath = os.path.join(os.path.abspath("."), "textures/female/skirt/" + skirt)
		changeTexture("girlLeftArm", texturePath, "defaultSkirt.tga")
		changeTexture("girlRightArm", texturePath, "defaultSkirt.tga")
		
	changeTexture(avatar + "LeftArm", texturePath, "undefined.tga")
	changeTexture(avatar + "RightArm", texturePath, "undefined.tga")
	
if trousers <> "":
  print "Trousers texture update"
  texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
  changeTexture("boyBody", texturePath, "defaultTrousers.tga")
	
if typeTrousers == "0" and gender == "male" and trousers <> "":
	#Shorts
	print "Shorts selected"
	texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
	changeTexture("boyLeftLeg", texturePath, "defaultTrousers.tga")
	changeTexture("boyRightLeg", texturePath, "defaultTrousers.tga")
	if skin <> "": 
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/skin/" + skin)
	  changeTexture("boyLeftLeg", texturePath, "undefined.tga")
	  changeTexture("boyRightLeg", texturePath, "undefined.tga")
elif typeTrousers == "1" and gender == "male":
	#Trousers
	print "Trousers selected"
	if trousers == "":
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/default/defaultTrousers.tga")
	else:
	  texturePath = os.path.join(os.path.abspath("."), "textures/male/trousers/" + trousers)
	changeTexture("boyLeftLeg", texturePath, "defaultTrousers.tga")
	changeTexture("boyRightLeg", texturePath, "defaultTrousers.tga")
	changeTexture("boyLeftLeg", texturePath, "undefined.tga")
	changeTexture("boyRightLeg",texturePath,"undefined.tga")
	
if shoes <> "":
  print "Shoes texture updated"
  texturePath = os.path.join(os.path.abspath("."), "textures/" + gender + "/shoes/" + shoes)
  changeTexture(avatar + "LeftLeg", texturePath, "defaultShoes.tga")
  changeTexture(avatar + "RightLeg", texturePath, "defaultShoes.tga")
	
#Generate one image for each rotation
rotations = [0, 45, 90, 135, 180, 225, 270, 315]
arm = Blender.Object.Get("Armature")
actDict = Blender.Armature.NLA.GetActions()
actList = Blender.Armature.NLA.GetActions().keys()


if os.path.exists("imagesGenerated/") == False:
  os.mkdir("imagesGenerated")
	
for act in actList:
  action = actDict[act]
  action.setActive(arm)
  action.getFrameNumbers()[-1]
  if os.path.exists("imagesGenerated/" + action.getName()) == False:
    os.mkdir("imagesGenerated/" + action.getName())
  for rot in rotations:
    rotateObject("cameraAnchor", rot)
    if rot == 0:
      renderScene("imagesGenerated/" + action.getName() + "/S/", action.getFrameNumbers()[0], action.getFrameNumbers()[-1])
    elif rot == 45:
      renderScene("imagesGenerated/" + action.getName() + "/SO/", action.getFrameNumbers()[0], action.getFrameNumbers()[-1])
    elif rot == 90:
      renderScene("imagesGenerated/" + action.getName() + "/O/", action.getFrameNumbers()[0], action.getFrameNumbers()[-1])
    elif rot == 135:
      renderScene("imagesGenerated/" + action.getName() + "/NO/", action.getFrameNumbers()[0], action.getFrameNumbers()[-1])
    elif rot == 180:
      renderScene("imagesGenerated/" + action.getName() + "/N/", action.getFrameNumbers()[0], action.getFrameNumbers()[-1])
    elif rot == 225:
      renderScene("imagesGenerated/" + action.getName() + "/NE/", action.getFrameNumbers()[0], action.getFrameNumbers()[-1])
    elif rot == 270:
      renderScene("imagesGenerated/" + action.getName() + "/E/", action.getFrameNumbers()[0], action.getFrameNumbers()[-1])
    elif rot == 315:
      renderScene("imagesGenerated/" + action.getName() + "/SE/", action.getFrameNumbers()[0], action.getFrameNumbers()[-1])


	
	