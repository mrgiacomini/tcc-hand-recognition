import numpy as np

arffCadeia = {}

def codigoCadeia(largestContour):
	l = len(largestContour)
	cadeia = np.zeros(8, np.int32)

	for index, p in enumerate(largestContour):
		if index < (l - 1):
			pNext = largestContour[index + 1]

			if (p[0][0] + 1 == pNext[0][0]) and (p[0][1] == pNext[0][1]):
				cadeia[0] += 1

			elif (p[0][0] + 1 == pNext[0][0]) and (p[0][1] - 1 == pNext[0][1]):
				cadeia[1] += 1

			elif (p[0][0] == pNext[0][0]) and (p[0][1] - 1 == pNext[0][1]):
				cadeia[2] += 1

			elif (p[0][0] - 1 == pNext[0][0]) and (p[0][1] - 1 == pNext[0][1]):
				cadeia[3] += 1

			elif (p[0][0] - 1 == pNext[0][0]) and (p[0][1] == pNext[0][1]):
				cadeia[4] += 1

			elif (p[0][0] - 1 == pNext[0][0]) and (p[0][1] + 1 == pNext[0][1]):
				cadeia[5] += 1

			elif (p[0][0] == pNext[0][0]) and (p[0][1] + 1 == pNext[0][1]):
				cadeia[6] += 1

			else:
				cadeia[7] += 1

	return cadeia

def openArffCadeia(folders):
	global arffCadeia

	arffCadeia = open("codigoDaCadeia.arff", "w+")

	arffCadeia.write("@relation cadeia\n")
	arffCadeia.write("\n")
	for i in range(0,7):
		arffCadeia.write("@ATTRIBUTE h" + str(i) +" NUMERIC\n")

	classes = ""
	for i, classe in enumerate(folders):
		if (i == len(folders) - 1):
			classes += classe
		else:
			classes += classe + " ,"

	arffCadeia.write("@ATTRIBUTE class {" + classes + "}\n")
	arffCadeia.write("@data\n")

def writeDataCadeia(cadeia, folder):
	global arffCadeia

	for index, numero in enumerate(cadeia):
		if (index == cadeia.size - 1):
			arffCadeia.write(folder)
		else:
			arffCadeia.write(str(numero))
			arffCadeia.write(" , ")
	arffCadeia.write("\n")

def closeArff():
	global arffCadeia
	arffCadeia.close()