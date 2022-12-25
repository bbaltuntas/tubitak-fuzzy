import pandas as pd
import numpy as np
import copy

"""
def split(array, nrows, ncols):
	r, h = array.shape
	return (array.reshape(h//nrows, nrows, -1, ncols)
				 .swapaxes(1, 2)
				 .reshape(-1, nrows, ncols))

matris = pd.read_excel("bireyselmatris.xlsx",header=None)
print(matris.shape)
kararvericisayisi=3
kritersayisi=len(matris)//kararvericisayisi

yenihali = split(matris.to_numpy(), 3, kararvericisayisi)
yenihali = np.reshape(yenihali, newshape=(kritersayisi,kritersayisi,3,kararvericisayisi))
print(yenihali.shape)
print(yenihali)
"""
def tutarlilikhesapla(matris, tip="m"):
	print("Tutarlilik hesabi")
	"""
	matris = [[1,	1.1967,	1.0536,	0.4],
		[0.8862,	1,	3,	1.3694],
		[1.0506,	0.3,	1,	0.5292],
		[2.5449,	0.7837,	1.9968,	1]]
	"""
	matris = np.array(matris)
	print("matris",matris)
	normalizematris = copy.deepcopy(matris)

	for i in range(len(matris)):
		for j in range(len(matris)):
			normalizematris[i,j] = matris[i,j]/np.sum(matris[:,j])
	print("normalize matris",normalizematris)

	satirortalamasi = [0 for i in range(len(matris))]
	satirortalamasi = np.array(satirortalamasi)

	satirortalamasi = np.mean(normalizematris, axis=1)
	print("satir ortalamasi",satirortalamasi)

	carpim= np.dot(matris, satirortalamasi)
	print("carpim",carpim)
	carpim/=satirortalamasi
	carpim/=len(matris)
	print("carpim",carpim)
	toplam = np.sum(carpim)
	print("toplam",toplam)
	ci = (toplam-len(matris))/(len(matris)-1)
	print("ci",ci)
	if tip == "m":
		rimatrisi = [9999, 9999, 0.4889, 0.7937, 1.072, 1.1996, 1.2874, 1.341, 1.3793, 1.4095, 1.4181, 1.4462, 1.4555, 1.4913, 1.4986]
	else:
		rimatrisi = [9999,	9999, 0.1796,	0.2627,	0.3597,	0.3818,	0.409,	0.4164,	0.4348,	0.4455,	0.4536,	0.4776,	0.4691,	0.4804,	0.488]
	sonuc = ci/rimatrisi[len(matris)-1]
	print("sonuc",sonuc)
	return sonuc

def agirlikhesapla(veri, kritersayisi):
	print("Agirlik hesabi")
	#veri = pd.read_excel("veri.xlsx", header=None)
	print("veri:")
	print(veri)

	kritersayisi = kritersayisi#len(veri)
	print("\nkriter sayisi:", kritersayisi)
	veri = np.asarray(veri).reshape((kritersayisi, 3*kritersayisi))
	si=np.zeros(shape=(kritersayisi, 3))
	for i in range(kritersayisi):
		for j in range(3):
			toplam=0
			for k in range(kritersayisi):
				toplam += veri[i,j+3*k]
			#print(toplam)
			si[i, j] = toplam
	print("\nsi matrisi:")
	print(si)
	si_toplam = np.sum(si, axis=0)
	print("\nsi matrisinin toplami:")
	print(si_toplam)
	tersi = np.flip(1/si_toplam)
	degerler = si*tersi
	print("\ndegerler matrisi:")
	print(degerler)
	V=np.zeros(shape=(kritersayisi,kritersayisi))
	V=1-V
	for i in range(kritersayisi):
		for j in range(kritersayisi):
			if i!=j:
				olasilik = (degerler[j,0]-degerler[i,2])/((degerler[i,1]-degerler[i,2])-(degerler[j,1]-degerler[j,0]))
				if olasilik>1:
					olasilik=1
				if olasilik < 0:
					olasilik=0
				#print(olasilik)
				V[i,j]=olasilik
	print("\nV olasiliklari:")
	print(V)

	deger=np.zeros(shape=(kritersayisi))
	for i in range(kritersayisi):
		deger[i] = np.min(V[i])
	print("\nd degerleri:")
	print(deger)

	toplamdeger = np.sum(deger)
	normalizedeger = deger/toplamdeger
	print("\nnormalize degerler:")
	print(normalizedeger)
	return normalizedeger
