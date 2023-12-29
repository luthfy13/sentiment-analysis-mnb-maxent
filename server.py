#!flask/bin/python
#import MySQLdb, pickle, nltk, re
#import nltk.classify
#from flask import Flask, jsonify, request
#import os

import MySQLdb, pickle, re
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

params = ""
Negasi = []
tag = ['VB', 'JJ']

def TagNegasi(kalimat):
	for word in Negasi:
		kalimat = ' ' + kalimat + ' '
		kalimat = re.sub(word + ' ','NOT_',kalimat)
	return kalimat

def POS_tag(komen):
	teks = nltk.word_tokenize(komen)
	hsl = nltk.pos_tag(teks)
	return hsl
	
def CekKomentar(komen):
	hsl = POS_tag(komen)
	ada = ''
	for kata in hsl:
		for i in kata:
			for j in tag:
				if re.search(j, i) is None:
					continue
				else:
					ada = 'true'
	if ada != 'true':
		ada = 'false'
	return ada
	
def FinalKomentar(komen):
	if CekKomentar(komen) == 'true':
		return TagNegasi(komen)
	else:
		return 'null'

def EkstraksiFitur(komentar):
	comment_words = set(komentar)
	features = {}
	for word in komentar:
		features['contains(%s)' % word] = (word in comment_words)
	return features

def GetFeatureVector(komentar):
	fitur = []
	kata = komentar.split()
	for w in kata:
		fitur.append(w)
	return fitur

def TentukanSentimen(komentar):
	sent = model_klasifikasi.classify(EkstraksiFitur(GetFeatureVector(TagNegasi(komentar))))
	return sent
	
def BacaStopWords():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cursor = db.cursor()
	qDataSet = "select word from stopwords"
	try:
		cursor.execute(qDataSet)
		results = cursor.fetchall()
		kata = []
		stopwords = []
		for row in results:
			kata = row[0]
			stopwords.append(kata)
			# Now print fetched result
	except:
		print "Error: unable to fecth data"
	db.close()
	return stopwords

def BacaNegasi():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cursor = db.cursor()
	qDataSet = "select word from negasi"
	try:
		cursor.execute(qDataSet)
		results = cursor.fetchall()
		kata = []
		Negasi = []
		for row in results:
			kata = row[0]
			field = 'word'
			Negasi.append(kata)
			# Now print fetched result
	except:
		print "Error: unable to fecth data"
	db.close()
	return Negasi

@app.route('/stopwords', methods = ['POST'])
def read_stopwords():
	params = request.form['params']
	if params == 'req_stopwords':
		sw = []
		sw = BacaStopWords()
		#sw = unicode(sw)
		return jsonify( { 'stopwords' : sw  } )

@app.route('/sentiment_result', methods = ['POST'])
def sentiment_result():
	hsl_sentimen = []
	komentar2 = request.get_json(force=True)
	for komentar in komentar2:
		hsl_sentimen.append(TentukanSentimen(komentar))
	return jsonify( { 'Hasil': hsl_sentimen } )
		
if __name__ == '__main__':
	apppath = os.path.dirname(os.path.realpath(__file__))
	Negasi = BacaNegasi()
	model = open(apppath + '/model.pickle', 'rb')
	model_klasifikasi = pickle.load(model)
	model.close()
	print 'Server Siap...'
	app.run(host='192.168.43.94', debug = True)
