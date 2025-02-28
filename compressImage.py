from PIL import Image

imageDir = "static//images//"
listeNameBike = ["bike1.jpg", "bike2.jpg", "bike3.jpg", "bike4.jpg"]
maxWidth = 800

# parcour toute les images à compresser
for currentBike in listeNameBike:
    currentImage = Image.open("%s//%s"%(imageDir,currentBike)) # chargement de l'image
    currentImage = currentImage.convert("RGB") # enlève canal alpha et autres conneries

    originalDimensions=currentImage.size # récupère ls dimension originales de l'image

    # on cherche quelle dimension est la plus grande (aka paysage ou portrait) pour calculer le ratio
    if originalDimensions[0] > originalDimensions[1] or originalDimensions[0] == originalDimensions[1]: # paysage ou carré
        ratio = maxWidth/originalDimensions[0]
    elif originalDimensions[1] > originalDimensions[0]: # portrait
        ratio = maxWidth/originalDimensions[1]

    currentImage = currentImage.resize((int(originalDimensions[0]*ratio), int(originalDimensions[1]*ratio))) # resize l'image
    currentImage.save("%s//%s"%(imageDir,currentBike)) #save l'image
