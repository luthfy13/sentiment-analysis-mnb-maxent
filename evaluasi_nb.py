import MySQLdb
import math

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
		print "baca data fitur gagal"
	db.close
	return featureList

def BacaSentimen():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	csSentimen = db.cursor()
	query = "select sentimen from sentimen order by sentimen desc"
	try:
		csSentimen.execute(query)
		rsSentimen = csSentimen.fetchall()
		sentimen = []
		sentimenList = []
		for row in rsSentimen:
			sentimen = row[0]
			sentimenList.append(sentimen)
	except:
		print "baca data sentimen gagal"
	db.close
	return sentimenList
	
def BacaHslPrepTest():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cursor = db.cursor()
	qDataSet = "select komentar from test_hsl_prep where jenis='test_set'"
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
	
def JmlDokumen(sentimen):
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "select count(komentar) from test_hsl_prep where sentimen = '%s' and jenis='training_set'" % sentimen
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
	query = "select count(komentar) from test_hsl_prep where jenis='training_set'"
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
	
def FrekFitur():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "SELECT test_fitur.fitur, COUNT(test_fitur.fitur) AS frekuensi, test_hsl_prep.sentimen \
			FROM test_fitur INNER JOIN test_hsl_prep ON test_fitur.id_komentar = test_hsl_prep.id \
			where test_hsl_prep.jenis='training_set' \
			GROUP BY test_hsl_prep.sentimen, test_fitur.fitur ORDER BY test_fitur.fitur ASC"
	try:
		cs.execute(query)
		rs = cs.fetchall()
		jml = 0
		fitur = ''
		sentimen = ''
		DataFrekFitur = {}
		for row in rs:
			fitur    = row[0]
			jml      = row[1]
			sentimen = row[2]
			DataFrekFitur[fitur,sentimen] = jml
	except:
		print "baca data doc gagal"
	db.close
	for sentimen in sentimenList:
		for fitur in featureList:
			try:
				DataFrekFitur[fitur,sentimen] = DataFrekFitur[fitur,sentimen]
			except:
				DataFrekFitur[fitur,sentimen] = 0
	return DataFrekFitur

def JmlFitur(sentimen):
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "SELECT count(test_fitur.fitur), test_hsl_prep.sentimen FROM test_fitur \
			INNER JOIN test_hsl_prep ON test_fitur.id_komentar = test_hsl_prep.id \
			WHERE test_hsl_prep.sentimen = '%s' and test_hsl_prep.jenis='training_set'" % sentimen
	try:
		cs.execute(query)
		rs = cs.fetchall()
		jml = 0
		for row in rs:
			jml = row[0]
	except:
		print "baca data gagal"
	db.close
	return jml
	
def JmlVocabulary():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "SELECT count(fitur) FROM ( SELECT DISTINCT test_fitur.fitur FROM test_fitur ) f"
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
	
def Pembobotan():
	alpha = 1
	LogCondProb={}
	DataFrekFitur = FrekFitur()
	JumlahFitur = {}
	V = JmlVocabulary()
	for sentimen in sentimenList:
		JumlahFitur[sentimen] = JmlFitur(sentimen)
	for sentimen in sentimenList:
		for fitur in featureList:
			LogCondProb[fitur,sentimen] = math.log(float(DataFrekFitur[fitur,sentimen] + alpha) / float(JumlahFitur[sentimen] + (V*alpha)), 2)
	return LogCondProb
	
def Klasifikasi(teks):
	bobot = {}
	kata = teks.split()
	for sentimen in sentimenList:
		bobot[sentimen] = float(LogPrior)
		for fitur in kata:
			try:
				bobot[sentimen] = float(bobot[sentimen]) + float(ModelKlasifikasi[fitur,sentimen])
			except:
				bobot[sentimen] = float(bobot[sentimen]) + 0 #(math.log(float(alpha) / float(JumlahFitur[sentimen] + (V*alpha)), 2))
	temp = -9999
	hsl = ''
	for sentimen in sentimenList:
		if (bobot[sentimen] > temp):
			hsl = sentimen
		temp = bobot[hsl]
	return hsl

if __name__ == '__main__':
	featureList = BacaFitur()
	sentimenList = BacaSentimen()
	V = JmlVocabulary()
	JumlahFitur = {}
	for sentimen in sentimenList:
		JumlahFitur[sentimen] = JmlFitur(sentimen)
	LogPrior = LogPriorProb(sentimen)
	ModelKlasifikasi = Pembobotan()
	hsl_prep = BacaHslPrepTest()
	for komentar in hsl_prep:
		print Klasifikasi(komentar)