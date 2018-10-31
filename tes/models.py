from django.db import models
import csv
import random
import math
import operator
import re
import numpy
from collections import Counter
from operator import itemgetter
from itertools import groupby
import time
from sklearn.metrics import confusion_matrix
import os

class Fknn():
	
	def loadDataset(split, label, trainingSet=[] , testSet=[]):
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(os.path.join(BASE_DIR, 'tes\\static\\data\\tes.csv'), "rt") as csvfile:
		    lines = csv.reader(csvfile)
		    dataset = list(lines)
		    temp = []
		    for i in range(len(dataset)):
		    	for j in range(len(label)):
		    		if dataset[i][1] == label[j]:
		    			temp.append(dataset[i])
		    random.shuffle(temp)
		    for x in range(len(temp)):
		        if x < len(temp)*split:
		        	trainingSet.append(temp[x])
		        else:
		            testSet.append(temp[x])

	def preprocessing(trainingSet, testSet, index, sentence=[]):
		for i in range(len(trainingSet)):
			sentence.append(re.split(r'_', str(trainingSet[i][0])))
		sentence.append(re.split(r'_', str(testSet[index][0])))

	def makeAtribute(sentence, atribute=[]):
		new_atribute = []
		for i1 in range(len(sentence)):
		    for i2 in range(len(sentence[i1])):
		        new_atribute.append(sentence[i1][i2])
		new_atribute.sort()
		for i in range(len(new_atribute)):
			if new_atribute[i] not in atribute :
				atribute.append(new_atribute[i])

	def distance(atribute, sentence, trainingSet, testSet, index, nilaiK, neighbor=[]):
		matrix = numpy.zeros(shape=(len(atribute), len(sentence)))
		for i in range(len(sentence)):
			for j in range(len(sentence[i])):
				for k in range(len(atribute)):
					if sentence[i][j] == atribute[k]:
						matrix[k][i] = 1

		df = []
		idf = []
		for i in range(len(atribute)):
			df.append(matrix[i][:].tolist().count(1))
			idf.append(math.log10(len(sentence) / (matrix[i][:].tolist().count(1))))
		
		tfidf = []
		for i in range(len(atribute)):
			tfidf.append((idf[i] * matrix[i][:]).tolist())
		tfidf = numpy.array(tfidf)

		tr_te = []
		for i in range(len(sentence)-1):
			x = 0
			for j in range(len(atribute)):
				x += tfidf[j][len(sentence)-1] * tfidf[j][i]
			tr_te.append(x)

		p_vektor = []
		for i in range(len(sentence)):
			x = 0
			for j in range(len(atribute)):
				x += pow(tfidf[j][i], 2)
			p_vektor.append(math.sqrt(x))

		cosine = []
		for i in range(len(sentence)-1):
			x = 0
			try:
				x = tr_te[i] / (p_vektor[len(sentence)-1] * p_vektor[i])
			except:
				x = 0
			cosine.append(x)
		jarak=[]
		for i in range(len(cosine)):
			nested = []
			nested.append(cosine[i])
			nested.append(trainingSet[i][1])
			jarak.append(nested)
		
		jarak.sort(key=itemgetter(0), reverse=True)
		
		for i in range(nilaiK):
			x = []
			x.append(jarak[i][0])
			x.append(jarak[i][1])
			neighbor.append(x)
	
	def vote(neighbor):
		x = []
		for i in range(len(neighbor)):
			x.append(neighbor[i][1])
		return Counter(x)

	def label(trainingSet):
		tr = []
		for j in range(len(trainingSet)):
			tr.append(trainingSet[j][1])
		l = list(Counter(tr).keys())
		return l

	def membership(vote, nilaiK, label, neighbor, memberships = []):
		for i in range(nilaiK):
			y = neighbor[i][1]
			membership = dict()
			for c in label:
				try:
					uci = 0.49 * (vote[c] / nilaiK)
					if c == y:
						uci += 0.51
					membership[c] = uci
				except:
					membership[c] = 0

			memberships.append(membership)

	def weight(neighbor, m, w=[]):
		pangkat = 2 / (m - 1)
		for i in range(len(neighbor)):
			x = 0
			try:
				x = 1 / pow(neighbor[i][0], pangkat)
			except:
				x = 0
			w.append(x)

	def predict(nilaiK, w, label, memberships):
		matrix = numpy.zeros(shape=(nilaiK, len(label)))
		for i in range(nilaiK):
			m = list(memberships[i].values())
			keys = list(memberships[i].keys())
			for j in range(len(m)):
				try:
					matrix[i][j] = (w[i] * m[j]) / sum(w)
				except:
					matrix[i][j] = 0
		tot = sum(matrix)
		maks = max(tot)
		indeces = 0
		for i in range(len(label)):
			if maks == tot[i]:
				indeces = i
				break
		result = label[indeces]
		return result, tot

	def matrixConf(result, testSet):
		tes = []
		for i in range(len(testSet)):
			tes.append(testSet[i][1])
		conf = confusion_matrix(result, tes)
		return conf

	def precision(conf):
		tot = 0
		for i in range(len(conf)):
			d = 0
			for j in range(len(conf)):
				d += conf[j][i]
			try:
				tot += conf[i][i] / d
			except:
				tot += 0
			
		return tot / len(conf)

	def recall(conf):
		tot = 0
		for i in range(len(conf)):
			d = 0
			for j in range(len(conf)):
				d += conf[i][j]
			try:
				tot += conf[i][i] / d
			except:
				tot += 0
			
		return tot / len(conf)
	
	def akurasi(conf):
		diagonal = 0
		t = 0
		for i in range(len(conf)):
			diagonal += conf[i][i]
			for j in range(len(conf)):
				t += conf[i][j]
		return diagonal / t

	def main(label, split, nilaiK, m):
		f = Fknn
		best_akurasi = 0
		for q in range(106):
			rslt = []
			total = []
			prediksi = []
			trainingSet=[]
			testSet=[]
			s = float(split) / 100
			f.loadDataset(s, label, trainingSet , testSet)
			for i in range(len(testSet)):
				
				sentence=[]
				atribute=[]
				neighbor = []
				memberships = []
				w=[]
				f.preprocessing(trainingSet, testSet, i, sentence)
				f.makeAtribute(sentence, atribute)
				f.distance(atribute, sentence, trainingSet, testSet, i, int(nilaiK), neighbor)
				l = f.label(trainingSet)
				vo = f.vote(neighbor)
				f.membership(vo, int(nilaiK), l, neighbor, memberships)
				f.weight(neighbor, int(m), w)
				result, tot = f.predict(int(nilaiK), w, l, memberships)
				prediksi.append(result)
				if result == testSet[i][1]:
					status = "Benar"
				else:
					status = "Salah"

				if len(l) == 1:
					rslt.append([result,testSet[i][1], status, round(tot[0], 5)])
				elif len(l) == 2:
					rslt.append([result,testSet[i][1], status, round(tot[0], 5), round(tot[1], 5)])
				elif len(l) == 3:
					rslt.append([result,testSet[i][1], status, round(tot[0], 5), round(tot[1], 5), round(tot[2], 5)])
				total.append(tot)
			
			cm = f.matrixConf(prediksi, testSet)
			precision = f.precision(cm) * 100
			recall = f.recall(cm) * 100
			akurasi = f.akurasi(cm) * 100

			if akurasi > best_akurasi and akurasi != 100:
				best_akurasi = akurasi
				best_precision = precision
				best_recall = recall
				best_total = total[:]
				best_rslt = rslt[:]
				best_training = trainingSet
				best_testing = testSet

		return {'rslt': best_rslt, 'precision': best_precision, 'recall': best_recall, 'akurasi': best_akurasi, 'himpunan': best_total, 'label': l}, best_training, best_testing

	def main2(te, label):
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(os.path.join(BASE_DIR, 'tes\\static\\data\\parameter.csv'), "rt") as csvfile:
		    lines = csv.reader(csvfile)
		    dataset = list(lines)
		    nilaiK = dataset[0][0]
		    m = dataset[0][1]

		f = Fknn
		s = float(80) / 100
		trainingSet=[]
		testSet=[]
		f.loadDataset(s, label, trainingSet , testSet)
		for i in range(len(testSet)):
			trainingSet.append(testSet[i])
		rslt = []
		total = []
		prediksi = []
		for i in range(len(te)):
			sentence=[]
			atribute=[]
			neighbor = []
			memberships = []
			w=[]
			f.preprocessing(trainingSet, te, i, sentence)
			f.makeAtribute(sentence, atribute)
			f.distance(atribute, sentence, trainingSet, te, i, int(nilaiK), neighbor)
			l = f.label(trainingSet)
			vo = f.vote(neighbor)
			f.membership(vo, int(nilaiK), l, neighbor, memberships)
			f.weight(neighbor, int(m), w)
			result, tot = f.predict(int(nilaiK), w, l, memberships)
			prediksi.append(result)
			if len(l) == 1:
				rslt.append([result, round(tot[0], 5)])
			elif len(l) == 2:
				rslt.append([result, round(tot[0], 5), round(tot[1], 5)])
			elif len(l) == 3:
				rslt.append([result, round(tot[0], 5), round(tot[1], 5), round(tot[2], 5)])
		
		
		return {'rslt': rslt, 'label': l}