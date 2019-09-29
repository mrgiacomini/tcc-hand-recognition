import cv2
import math

arffHu = {}

def huMoments(img):
	moments = cv2.moments(img)
	# Calculate Hu Moments
	huMoments = cv2.HuMoments(moments)
	# Log scale hu moments
	for i in range(0, 7):
		huMoments[i] = -1 * math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))

	return huMoments

def openArffHu(folders):
	global arffHu
	arffHu  = open("huMoments.arff","w+")

	arffHu.write("@relation hu_moments\n\n")
	i=0
	for i in range (0,7):
		arffHu.write("@ATTRIBUTE h" + str(i) + " NUMERIC\n")

	classes=""
	for i, classe in enumerate(folders):
		if (i == len(folders)-1):
			classes+=classe
		else:
			classes+=classe+" ,"

	arffHu.write("@ATTRIBUTE class {"+classes+"}\n@data\n")

def writeDataHu(huMoments, folder):
	global arffHu
	for i,moment in enumerate(huMoments):
		if (i == huMoments.size - 1):
			arffHu.write(folder)
		else:
			arffHu.write(str(moment[0])+", ")

	arffHu.write("\n")

def closeArff():
	global arffHu
	arffHu.close()