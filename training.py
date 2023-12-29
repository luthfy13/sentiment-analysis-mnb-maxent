import MySQLdb
import math

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

def EmptyBobot():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "delete from bobot"
	try:
		cs.execute(query)
		db.commit()
	except:
		print "hapus data gagal"
		db.rollback()
	db.close
	
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
	
def FrekFitur():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	query = "SELECT fitur.fitur, COUNT(fitur.fitur) AS frekuensi, hsl_prep.sentimen \
			FROM fitur INNER JOIN hsl_prep ON fitur.id_komentar = hsl_prep.id \
			GROUP BY hsl_prep.sentimen, fitur.fitur ORDER BY fitur.fitur ASC"
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
	query = "SELECT count(fitur.fitur), hsl_prep.sentimen FROM fitur \
			INNER JOIN hsl_prep ON fitur.id_komentar = hsl_prep.id \
			WHERE hsl_prep.sentimen = '%s'" % sentimen
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
	query = "SELECT count(fitur) FROM ( SELECT DISTINCT fitur.fitur FROM fitur ) f"
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
		for fitur in featureList:
			LogCondProb[fitur,sentimen] = math.log(float(DataFrekFitur[fitur,sentimen] + alpha) / float(JumlahFitur[sentimen] + (V*alpha)), 2)
	return LogCondProb
	
def Training():
	EmptyBobot()
	LogCondProb = Pembobotan()
	query = []
	query.append("insert into bobot (fitur,kelas,cond_prob) values")
	for sentimen in sentimenList:
		for fitur in featureList:
			query.append("('%s', '%s', %.16f)," % (fitur, sentimen, LogCondProb[fitur,sentimen]) )
	final_query = ''.join(query)
	final_query = final_query[:-1]
	
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cs = db.cursor()
	try:
		cs.execute(final_query)
		db.commit()
	except:
		print "insert data gagal"
		db.rollback()
	db.close

if __name__ == '__main__':
	featureList = BacaFitur()
	sentimenList = BacaSentimen()
	Training();
	print 'Proses training selesai :D'