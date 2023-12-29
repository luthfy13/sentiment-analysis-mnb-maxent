import MySQLdb,math,os,re
from flask import Flask, jsonify, request
from decimal import *
app = Flask(__name__)

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
		print "baca data fitur gagal"
	db.close
	return featureList

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
	
def TagNegasi(kalimat):
	for word in Negasi:
		kalimat = ' ' + kalimat + ' '
		kalimat = re.sub(word + ' ','NOT_',kalimat)
	return kalimat
	
def JmlDokumen(sentimen):
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "select count(komentar) from hsl_prep where sentimen = '%s' " % sentimen
	try:
		cs.execute(query)
		rs = cs.fetchall()
		jml = 0
		for row in rs:
			jml = row[0]
	except:
		print "baca data doc gagal"
	db.close
	return jml
	
def JmlSeluruhDokumen():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "select count(komentar) from hsl_prep"
	try:
		cs.execute(query)
		rs = cs.fetchall()
		jml = 0
		for row in rs:
			jml = row[0]
	except:
		print "baca data all doc gagal"
	db.close
	return jml
	
def LogPriorProb(sentimen):
	N_kelas = float(JmlDokumen(sentimen))
	N = float(JmlSeluruhDokumen())
	return math.log(N_kelas/N, 2)
	
def BacaModelKlasifikasi():
	model = {}
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "SELECT fitur, kelas, cond_prob FROM bobot"
	try:
		cs.execute(query)
		rs = cs.fetchall()
		fitur = ''
		sentimen = ''
		bobot = 0.0
		for row in rs:
			fitur = row[0]
			sentimen = row[1]
			bobot = row[2]
			model[fitur,sentimen] = bobot
	except:
		print "baca data doc gagal"
	db.close
	return model
	
def TentukanSentimen(teks):
	print 'Fitur = %s' % teks.split()
	myothercontext = Context(prec=18, rounding=ROUND_HALF_UP)
	setcontext(myothercontext)
	ProbAkhir = {}
	teks = TagNegasi(teks)
	kata = teks.split()
	for sentimen in sentimenList:
		ProbAkhir[sentimen] = Decimal(LogPrior[sentimen])
		for fitur in kata:
			try:
				ProbAkhir[sentimen] = Decimal(ProbAkhir[sentimen]) + Decimal(ModelKlasifikasi[fitur,sentimen])
			except:
				ProbAkhir[sentimen] = Decimal(ProbAkhir[sentimen]) + 0 #(math.log(float(alpha) / float(JumlahFitur[sentimen] + (V*alpha)), 2))
		print 'ProbabilitasAkhir(%s) = %s' % (sentimen,str(ProbAkhir[sentimen]))
	temp = -9999
	hsl = ''
	for sentimen in sentimenList:
		if (ProbAkhir[sentimen] > temp):
			hsl = sentimen
		temp = ProbAkhir[hsl]
	print 'c_map = %s' % ProbAkhir[hsl]
	return hsl

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
	komen = request.get_json(force=True)
	for komentar in komen:
		hsl_sentimen.append(TentukanSentimen(komentar))
	return jsonify( { 'Hasil': hsl_sentimen } )

if __name__ == '__main__':
	LogPrior={}
	Negasi = BacaNegasi()
	featureList = BacaFitur()
	sentimenList = ['Positif','Negatif','Crash']
	for sentimen in sentimenList:
		LogPrior[sentimen] = LogPriorProb(sentimen)
	ModelKlasifikasi = BacaModelKlasifikasi()
	TestKomentar = ['NOT_working right NOT_want follow people', 'boring boring started boring characters', 'just looking great game addictive']
	for komen in TestKomentar:
		print 'Hasil Klasifikasi: %s' % TentukanSentimen(komen)
		print ''