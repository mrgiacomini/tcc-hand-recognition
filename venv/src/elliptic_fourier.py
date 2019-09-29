from os import listdir
import numpy as np
from pyefd import elliptic_fourier_descriptors

arffFourier = {}
nro_coeficientes = {}

def coeffFourier(contorno):
	global nro_coef
	coeff = elliptic_fourier_descriptors(np.squeeze(contorno), order=nro_coeficientes)
	return coeff.flatten()[3:]

def openArffFourier(folders, nro_coef=10):
	global arffFourier, nro_coeficientes
	nro_coeficientes = nro_coef

	arffFourier = open("fourier.arff", "w+")

	arffFourier.write("@relation fourier\n\n")
	i=0
	while (i < (nro_coeficientes*4)-4):
		arffFourier.write("@ATTRIBUTE c" + str(i) + " NUMERIC\n")
		i+=1

	classes=""
	for i, classe in enumerate(folders):
		if (i == len(folders)-1):
			classes+=classe
		else:
			classes+=classe+" ,"

	arffFourier.write("@ATTRIBUTE class {"+classes+"}\n")
	arffFourier.write("@data\n")

def writeDataFourier(coeficientes, folder):
	global arffFourier

	for i, elem in enumerate(coeficientes):
		if (i == coeficientes.size-1):
			arffFourier.write(folder)
		else:
			arffFourier.write(str(elem))
			arffFourier.write(" , ")
	arffFourier.write("\n")

def closeArff():
	global arffFourier
	arffFourier.close()