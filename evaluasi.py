#!/usr/bin/python
import os.path
import nltk
import MySQLdb
import re, pickle, csv, os, sys
import pprint
import svm
from svmutil import *

dir_path = os.path.dirname(os.path.realpath(__file__))

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
	
def EkstraksiFiturTestSet(komentar):
	comment_words = set(komentar)
	features = {}
	for word in komentar:
		features['contains(%s)' % word] = (word in comment_words)
	return features

def BacaFitur():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	crFeatureList = db.cursor()
	qFeatureList = "select distinct fitur from test_fitur order by fitur asc"
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
	qDataSet = "select * from test_hsl_prep where jenis = 'training_set'"	
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
	
def BacaHslPrepTest():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cursor = db.cursor()
	qDataSet = "select komentar from test_hsl_prep where jenis='test_set' order by sentimen asc"
	try:
		cursor.execute(qDataSet)
		results = cursor.fetchall()
		komentar = []
		hslprep = []
		for row in results:
			komentar = row[0]
			hslprep.append(komentar)
			# Now print fetched result
	except:
		print "Error: unable to fecth data"
	db.close()
	return hslprep

def getSVMFeatureVectorAndLabels(data_set):
	sortedFeatures = sorted(featureList)
	map = {}
	feature_vector = []
	labels = []
	for t in data_set:
		label = 0
		map = {}
		for w in sortedFeatures:
			map[w] = 0
		tweet_words = t[0]
		tweet_opinion = t[1]
		for word in tweet_words:
			if word in map:
				map[word] = 1
		values = map.values()
		feature_vector.append(values)
		if(tweet_opinion == 'Positif'):
			label = 0
		elif(tweet_opinion == 'Negatif'):
			label = 1
		elif(tweet_opinion == 'Crash'):
			label = 2
		labels.append(label)            
	return {'feature_vector' : feature_vector, 'labels': labels}
	
def getSVMFeatureVector(komentar):
#	featureList = BacaFitur()
	sortedFeatures = sorted(featureList)
	map = {}
	feature_vector = []
	for t in komentar:
		label = 0
		map = {}
		for w in sortedFeatures:
			map[w] = 0
		for word in t:
			if word in map:
				map[word] = 1
		values = map.values()
		feature_vector.append(values)                    
	return feature_vector	
	
def KomentarForSVM(komentar):
	hasil = []
	for komen in komentar:
		kata = komen.split()
		hasil.append(kata)
	return hasil
	
def TrainingClassifierNB(data_set):
	training_set = nltk.classify.util.apply_features(EkstraksiFitur, data_set)
	NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
	return NBClassifier

def TrainingClassifierME(data_set):
	training_set = nltk.classify.util.apply_features(EkstraksiFitur, data_set)
	MaxEntClassifier = nltk.classify.maxent.MaxentClassifier.train(training_set, 'GIS', trace=3, encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 10)
	#algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
	#MaxEntClassifier = nltk.MaxentClassifier.train(trainfeats, algorithm,max_iter=3)
	# if not(os.path.exists('me_model1.pickle')):
		# outfile = open('me_model1.pickle', 'w')
	# elif not(os.path.exists('me_model2.pickle')):
		# outfile = open('me_model2.pickle', 'w')
	# elif not(os.path.exists('me_model3.pickle')):
		# outfile = open('me_model3.pickle', 'w')
	# pickle.dump(MaxEntClassifier, outfile)        
	# outfile.close()
	return MaxEntClassifier

def TrainingClassifierSVM(data_set):
	results = getSVMFeatureVectorAndLabels(data_set)
	feature_vectors = results['feature_vector']
	labels = results['labels']
	problem = svm_problem(labels, feature_vectors)
	param = svm_parameter('-q')
	param.kernel_type = LINEAR
	svmClassifier = svm_train(problem, param)
	return svmClassifier
	
def TentukanSentimenNB(model,komentar):
	sent = model.classify(EkstraksiFitur(GetFeatureVector((komentar))))
	return sent
	
def TentukanSentimenSVM(model, komentar):
	komentarSVM = getSVMFeatureVector(KomentarForSVM(komentar))
	p_labels, p_accs, p_vals = svm_predict([0] * len(komentarSVM), komentarSVM, model, "-q")
	return p_labels
	
def TentukanSentimenME(model, komentar):
	sent = model.classify(EkstraksiFitur(GetFeatureVector((komentar))))
	return sent
	
def konversiLabel(angka):
	if (angka==0.0):
		return "Positif"
	elif (angka==1.0):
		return "Negatif"
	elif (angka==2.0):
		return "Crash"

if __name__ == '__main__':
	algorithm = sys.argv[1]
	featureList = BacaFitur()
	data_set = MakeDataSet()
	hsl_prep = BacaHslPrepTest()
	if(algorithm == "naive_bayes"):
		model_klasifikasi = TrainingClassifierNB(data_set)
		for komen in hsl_prep:
			print TentukanSentimenNB(model_klasifikasi, komen)
	elif(algorithm == "svm"):
		model_klasifikasi = TrainingClassifierSVM(data_set)
		hsl = TentukanSentimenSVM(model_klasifikasi, hsl_prep)
		for x in hsl:
			print konversiLabel(x)
	elif(algorithm == "me"):
		model_klasifikasi = TrainingClassifierME(data_set)
		for komen in hsl_prep:
			print TentukanSentimenME(model_klasifikasi, komen)
	# elif(algorithm == "me1"):
		# model_klasifikasi = pickle.load(open(dir_path + "\\" + "me_model1.pickle", "r"))
		# for komen in hsl_prep:
			# print TentukanSentimenME(model_klasifikasi, komen)
	# elif(algorithm == "me2"):
		# model_klasifikasi = pickle.load(open(dir_path + "\\" + "me_model2.pickle", "r"))
		# for komen in hsl_prep:
			# print TentukanSentimenME(model_klasifikasi, komen)
	# elif(algorithm == "me3"):
		# model_klasifikasi = pickle.load(open(dir_path + "\\" + "me_model3.pickle", "r"))
		# for komen in hsl_prep:
			# print TentukanSentimenME(model_klasifikasi, komen)