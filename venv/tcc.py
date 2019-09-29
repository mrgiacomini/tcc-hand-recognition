import cv2
from os import listdir
import numpy as np
import elliptic_fourier as fourier
import codigo_cadeia as cadeia
import hu_moments as hu

path = "C:/Users/fabiu/Desktop/mao-preto/"
folders = [pasta for pasta in ["aberta-dorso", "aberta-palma", "fechada-dorso"]]

hMax = 0
hMin = 255
sMax = 0
sMin = 255
vMax = 0
vMin = 255
default = True
cont =0
indexFolder=0
showContour = False
showImg = False

# get all the images on the path
def readingImages():
	fourier.openArffFourier(folders)
	cadeia.openArffCadeia(folders)
	hu.openArffHu(folders)

	for indexFolder, folder in enumerate(folders):
		for indexFile, f in enumerate([arq for arq in listdir(path+folder)]):
			filename = path+folder+"/"+f
			img = cv2.imread(filename)
			if (showImg):
				cv2.imshow("Imagem "+str(indexFile), img)
			# segmentacao a partir do ROI
			imgSegmented = segmentationHand(img)
			# encontra o maior contorno
			largest = largestContour(imgSegmented)
			# constroi o codigo da cadeia e escreve no arff
			cadeia.writeDataCadeia(cadeia.codigoCadeia(largest), folder)
			# encontra os coeficientes elipticos de fourier e escreve no arff
			fourier.writeDataFourier(fourier.coeffFourier(largest), folder)
			# encontra os momentos de Hu e escreve no arff
			hu.writeDataHu(hu.huMoments(imgSegmented), folder)
			global cont
			cont= indexFile
			key = cv2.waitKey(1)
			if key == 27:
				break

	fourier.closeArff()
	cadeia.closeArff()
	hu.closeArff()

def readImage():
	filename = listdir(path+folders[0])
	img = cv2.imread(path+folders[0]+"/"+filename[0])
	# imgOtsu = cv2.imread(path + folders[0] + "/" + filename[0], 0)
	# ret, otsu = cv2.threshold(imgOtsu,0,255,cv2.THRESH_OTSU)
	# cv2.imshow('otsu', otsu)
	cv2.imshow("img", img)
	imgSegmented = segmentationHand(img)
	largest = largestContour(imgSegmented)
	hu.openArffHu(["teste"])
	hu.writeDataHu(hu.huMoments(imgSegmented), "teste")
	# codigoCadeia(largest)
	# openArffFourier()
	# writeDataFourier(coeffFourier(largest))
	# arffFourier.close()
	hu.closeArff()

def selectROI():
	#get first image to select ROI
	imgROI = cv2.imread(path+files[2])
	rectROI = cv2.selectROI(imgROI)  #(x,y,w,h)
	detectHandColor(imgROI, rectROI)
	imgSegmented = segmentationHand(imgROI)
	largest = largestContour(imgSegmented)
	codigoCadeia(largest)
	fourier.openArffFourier()
	fourier.writeDataFourier(fourier.coeffFourier(largest))
	fourier.arffFourier.close()

#detect hand colors from ROI
def detectHandColor(imgROI, rectROI):
	h = 0
	s = 0
	v = 0
	imgHSV = cv2.cvtColor(imgROI, cv2.COLOR_BGR2HSV)
	
	rows,cols = imgROI.shape[:2]
	i = rectROI[0]
	j = rectROI[1]
	
	while(i < rectROI[0] + rectROI[2] and i < cols):
		while (j < rectROI[1] + rectROI[3] and j < rows):
			h = imgHSV[j, i, 0]
			s = imgHSV[j, i, 1]
			v = imgHSV[j, i, 2]
			global hMax
			hMax = h if h > hMax else hMax
			global hMin
			hMin = h if h < hMin else hMin
			global sMax
			sMax = s if s > sMax else sMax
			global sMin
			sMin = s if (s < sMin) else sMin
			global vMax
			vMax = v if (v > vMax) else vMax
			global vMin
			vMin = v if (v < vMin) else vMin

			j+=1
		i+=1

	print(hMax, end = "\n")
	print(hMin, end = "\n")
	print(sMax, end ="\n")
	print(sMin, end ="\n")
	print(vMax, end ="\n")
	print(vMin, end ="\n")
	
#segment the image from the color detected
def segmentationHand(img):
	imgBlur = cv2.blur(img, (5,5))
	imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
	# cv2.imshow("hsv",imgHSV)

	if (default):
		# imgSegLimiar = cv2.inRange(imgHSV, np.array([0, 3, 64]), np.array([177, 85, 205])) #imagens-mao
		imgSegLimiar = cv2.inRange(imgHSV, np.array([0, 0, 0]), np.array([165, 255, 62])) #mao-preto
	else:
		imgSegLimiar = cv2.inRange(imgHSV, np.array([hMin, sMin, vMin]), np.array([hMax, sMax, vMax]))

	# cv2.imshow("limiar",imgSegLimiar)

	_,imgSegLimiar = cv2.threshold(imgSegLimiar, 0, 255, cv2.THRESH_BINARY_INV)

	# cv2.imshow("tresh", imgSegLimiar)
	tam = (9,9)
	kernelErode = np.ones(tam, np.uint8)
	imgDilateErode = cv2.erode(imgSegLimiar, kernelErode, iterations= 1)

	kernelDilate = np.ones(tam,np.uint8)
	imgDilate = cv2.dilate(imgDilateErode,kernelDilate,iterations = 1)

	# cv2.imshow("DilateErode", imgDilate)

	return imgDilate

#find the largest image segmentation contour
def largestContour(img):
	imgCanny = cv2.Canny(img, 0, 255, 3)

	contours1 = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

	mask1 = np.zeros(img.shape, np.uint8)
	cv2.drawContours(mask1, contours1, -1, 255, -1)
	# cv2.imshow("antes"+str(cont), mask1)
	tam = (3, 3)

	kernelDilate = np.ones(tam, np.uint8)
	imgDilate = cv2.dilate(mask1, kernelDilate, iterations=1)
	kernelErode = np.ones(tam, np.uint8)
	imgDilateErode = cv2.erode(imgDilate, kernelErode, iterations=1)
	# cv2.imshow("dilateerode"+str(cont),imgDilateErode)
	imgCanny = cv2.Canny(imgDilateErode, 0, 255, 3)

	contours = cv2.findContours(imgDilateErode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

	largest = contours[0]
	for cnt in contours:
		if cnt.size > largest.size:
			largest = cnt

	mask = np.zeros(img.shape, np.uint8)
	cv2.drawContours(mask, largest, -1, 255, -1)
	cv2.imshow("Result"+str(cont), mask)

	return largest

if __name__ == '__main__' :
	if default:
		# readImage()
		readingImages()
	else:
		selectROI()
		

	while(True):
		key = cv2.waitKey(1)
		if key == 27:
			cv2.destroyAllWindows()
			break