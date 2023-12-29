#!/usr/bin/python
import os.path
import nltk
import MySQLdb
import re, pickle, csv, os, sys
import pprint
import svm
from svmutil import *

dir_path = os.path.dirname(os.path.realpath(__file__))

def getFeatureVector(komentar):
	fitur = []
	kata = komentar.split()
	for w in kata:
		fitur.append(w)
	return fitur
	
def ekstraksiFitur(komentar):
	commentWords = set(komentar)
	features = {}
	for word in featureList:
		features['contains(%s)' % word] = (word in commentWords)
	print type(features)
	return features

def bacaFitur():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	crFeatureList = db.cursor()
	qFeatureList = "select distinct fitur from fitur order by fitur asc"
	try:
		crFeatureList.execute(qFeatureList)
		rsFeatureList = crFeatureList.fetchall()
		fitur = []
		featureList = []
		for row in rsFeatureList:
			fitur = row[0]
			featureList.append(fitur)
	except:
		print "Ekstraksi fitur gagal"
	db.close
	return featureList
	
def makeDataSet():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cursor = db.cursor()
	qDataSet = "select * from hsl_prep"	
	try:
	   cursor.execute(qDataSet)
	   results = cursor.fetchall()
	   id = []
	   komentar = []
	   rating = []
	   vektorFitur = []
	   dataSet = []
	   komen = []
	   for row in results:
		  id = row[0]
		  komentar = row[1]
		  sentimen = row[2]
		  vektorFitur = getFeatureVector(komentar)
		  dataSet.append((vektorFitur, sentimen))
	except:
	   print "Error: unable to fecth data"
	cursor.close
	db.close()
	return dataSet


def trainingClassifierME(dataSet):
	trainingSet = nltk.classify.util.apply_features(ekstraksiFitur, dataSet)
	MaxEntClassifier = nltk.classify.maxent.MaxentClassifier.train(trainingSet, 'GIS', trace=3, \
	                   encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 10)
	outfile = open('me_model.pickle', 'w')
	pickle.dump(MaxEntClassifier, outfile)        
	outfile.close()
	
def konversiLabel(angka):
	if (angka==0.0):
		return "Positif"
	elif (angka==1.0):
		return "Negatif"
	elif (angka==2.0):
		return "Crash"

if __name__ == '__main__':
	featureList = bacaFitur()
	dataSet = makeDataSet()
	trainingClassifierME(dataSet)