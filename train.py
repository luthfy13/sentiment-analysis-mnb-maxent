#!/usr/bin/python

import MySQLdb
import re, pickle, csv, os
import pprint
import nltk.classify

def GetFeatureVector(komentar):
	fitur = []
	kata = komentar.split()
	for w in kata:
		fitur.append(w)
	return fitur
	
def EkstraksiFitur(komentar):
    comment_words = set(komentar)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in comment_words)
    return features

def BacaFitur():
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

def MakeDataSet():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cursor = db.cursor()
	qDataSet = "select * from hsl_prep"	
	try:
	   cursor.execute(qDataSet)
	   results = cursor.fetchall()
	   id = []
	   komentar = []
	   rating = []
	   VektorVitur = []
	   data_set = []
	   komen = []
	   for row in results:
		  id = row[0]
		  komentar = row[1]
		  sentimen = row[2]
		  VektorVitur = GetFeatureVector(komentar)
		  data_set.append((VektorVitur, sentimen))
	except:
	   print "Error: unable to fecth data"
	cursor.close
	db.close()
	return data_set
	
def TrainingClassifier(data_set):
	training_set = nltk.classify.util.apply_features(EkstraksiFitur, data_set)
	NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
	return NBClassifier

if __name__ == '__main__':
	apppath = os.path.dirname(os.path.realpath(__file__))
	featureList = BacaFitur()
	data_set = MakeDataSet()
	model_klasifikasi = TrainingClassifier(data_set)
	outfile = open(apppath + '/model.pickle', 'wb')        
	pickle.dump(model_klasifikasi, outfile)        
	outfile.close()
	print "Creating classiffiacation model completed. :)"