import os.path
import nltk
import MySQLdb
import re, pickle, csv, os, sys, string
import pprint

featureList = []
stopWords = []
negasi = []
model_klasifikasi = ''

def gantiKataDasar(komentar):
	hsl = komentar
	hsl = re.sub(r'bisa dibuka', r'bisa_buka', hsl)
	hsl = re.sub(r'bisa di buka', r'bisa_buka', hsl)
	hsl = re.sub(r'bisa terbuka', r'bisa_buka', hsl)
	hsl = re.sub(r'bisa membuka', r'bisa_buka', hsl)
	hsl = re.sub(r'bs dibuka', r'bisa_buka', hsl)
	hsl = re.sub(r'bs di buka', r'bisa_buka', hsl)
	hsl = re.sub(r'bs terbuka', r'bisa_buka', hsl)
	hsl = re.sub(r'bs membuka', r'bisa_buka', hsl)
	hsl = re.sub(r'dapat dibuka', r'bisa_buka', hsl)
	hsl = re.sub(r'dapat di buka', r'bisa_buka', hsl)
	hsl = re.sub(r'dapat terbuka', r'bisa_buka', hsl)
	hsl = re.sub(r'dapat membuka', r'bisa_buka', hsl)
	hsl = re.sub(r'dpt dibuka', r'bisa_buka', hsl)
	hsl = re.sub(r'dpt di buka', r'bisa_buka', hsl)
	hsl = re.sub(r'dpt terbuka', r'bisa_buka', hsl)
	hsl = re.sub(r'dpt membuka', r'bisa_buka', hsl)
	hsl = re.sub(r'terbuka', r'bisa_buka', hsl)
	hsl = re.sub(r'dijalankan', r'jalan', hsl)
	hsl = re.sub(r'di jalankan', r'jalan', hsl)
	hsl = re.sub(r'menjalankan', r'jalan', hsl)
	hsl = re.sub(r'bisa dipasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'bisa di pasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'bisa terpasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'bisa memasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'bs dipasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'bs di pasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'bs terpasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'bs memasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'dapat dipasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'dapat di pasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'dapat terpasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'dapat memasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'dpt dipasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'dpt di pasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'dpt terpasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'dpt memasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'terpasang', r'bisa_pasang', hsl)
	hsl = re.sub(r'diproses', r'bisa_proses', hsl)
	hsl = re.sub(r'di proses', r'bisa_proses', hsl)
	hsl = re.sub(r'terproses', r'bisa_proses', hsl)
	hsl = re.sub(r'memproses', r'bisa_proses', hsl)
	hsl = re.sub(r'memroses', r'bisa_proses', hsl)
	hsl = re.sub(r'dikonfirmasi', r'bisa_konfirm', hsl)
	hsl = re.sub(r'di konfirmasi', r'bisa_konfirm', hsl)
	hsl = re.sub(r'terkonfirmasi', r'bisa_konfirm', hsl)
	hsl = re.sub(r'menkonfirmasi', r'bisa_konfirm', hsl)
	hsl = re.sub(r'mengkonfirmasi', r'bisa_konfirm', hsl)
	hsl = re.sub(r'dikonfirm', r'bisa_konfirm', hsl)
	hsl = re.sub(r'di konfirm', r'bisa_konfirm', hsl)
	hsl = re.sub(r'terkonfirm', r'bisa_konfirm', hsl)
	hsl = re.sub(r'menkonfirm', r'bisa_konfirm', hsl)
	hsl = re.sub(r'mengkonfirm', r'bisa_konfirm', hsl)
	hsl = re.sub(r'dibuat', r'bisa_buat', hsl)
	hsl = re.sub(r'di buat', r'bisa_buat', hsl)
	hsl = re.sub(r'menampilkan', r'tampil', hsl)
	hsl = re.sub(r'ditampilkan', r'tampil', hsl)
	hsl = re.sub(r'di tampilkan', r'tampil', hsl)
	hsl = re.sub(r'di tampil kan', r'tampil', hsl)
	hsl = re.sub(r'tertampil', r'tampil', hsl)
	hsl = re.sub(r'mendaftar', r'bisa_daftar', hsl)
	hsl = re.sub(r'didaftar', r'bisa_daftar', hsl)
	hsl = re.sub(r'di daftar', r'bisa_daftar', hsl)
	hsl = re.sub(r'mengakses', r'bisa_akses', hsl)
	hsl = re.sub(r'diakses', r'bisa_akses', hsl)
	hsl = re.sub(r'di akses', r'bisa_akses', hsl)
	hsl = re.sub(r'terakses', r'bisa_akses', hsl)
	hsl = re.sub(r'bisa menginstall', r'bisa_install', hsl)
	hsl = re.sub(r'bisa diinstall', r'bisa_install', hsl)
	hsl = re.sub(r'bisa di install', r'bisa_install', hsl)
	hsl = re.sub(r'bisa terinstall', r'bisa_install', hsl)
	hsl = re.sub(r'bs menginstall', r'bisa_install', hsl)
	hsl = re.sub(r'bs diinstall', r'bisa_install', hsl)
	hsl = re.sub(r'bs di install', r'bisa_install', hsl)
	hsl = re.sub(r'bs terinstall', r'bisa_install', hsl)
	hsl = re.sub(r'dapat menginstall', r'bisa_install', hsl)
	hsl = re.sub(r'dapat diinstall', r'bisa_install', hsl)
	hsl = re.sub(r'dapat di install', r'bisa_install', hsl)
	hsl = re.sub(r'dapat terinstall', r'bisa_install', hsl)
	hsl = re.sub(r'dpt menginstall', r'bisa_install', hsl)
	hsl = re.sub(r'dpt diinstall', r'bisa_install', hsl)
	hsl = re.sub(r'dpt di install', r'bisa_install', hsl)
	hsl = re.sub(r'dpt terinstall', r'bisa_install', hsl)
	hsl = re.sub(r'terinstall', r'bisa_install', hsl)
	hsl = re.sub(r'bisa menginstal', r'bisa_instal', hsl)
	hsl = re.sub(r'bisa diinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'bisa di instal', r'bisa_instal', hsl)
	hsl = re.sub(r'bisa terinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'bs menginstal', r'bisa_instal', hsl)
	hsl = re.sub(r'bs diinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'bs di instal', r'bisa_instal', hsl)
	hsl = re.sub(r'bs terinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'dapat menginstal', r'bisa_instal', hsl)
	hsl = re.sub(r'dapat diinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'dapat di instal', r'bisa_instal', hsl)
	hsl = re.sub(r'dapat terinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'dpt menginstal', r'bisa_instal', hsl)
	hsl = re.sub(r'dpt diinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'dpt di instal', r'bisa_instal', hsl)
	hsl = re.sub(r'dpt terinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'terinstal', r'bisa_instal', hsl)
	hsl = re.sub(r'menyimpan', r'bisa_simpan', hsl)
	hsl = re.sub(r'disimpan', r'bisa_simpan', hsl)
	hsl = re.sub(r'di simpan', r'bisa_simpan', hsl)
	hsl = re.sub(r'tersimpan', r'bisa_simpan', hsl)
	hsl = re.sub(r'terloginkan', r'bisa_login', hsl)
	hsl = re.sub(r'diloginkan', r'bisa_login', hsl)
	hsl = re.sub(r'bisa login', r'bisa_login', hsl)
	hsl = re.sub(r'bs login', r'bisa_login', hsl)
	hsl = re.sub(r'dapat login', r'bisa_login', hsl)
	hsl = re.sub(r'dpt login', r'bisa_login', hsl)
	hsl = re.sub(r'bisa log in', r'bisa_login', hsl)
	hsl = re.sub(r'bs log in', r'bisa_login', hsl)
	hsl = re.sub(r'dapat log in', r'bisa_login', hsl)
	hsl = re.sub(r'dpt log in', r'bisa_login', hsl)
	hsl = re.sub(r'bisa masuk', r'bisa_masuk', hsl)
	hsl = re.sub(r'bs masuk', r'bisa_masuk', hsl)
	hsl = re.sub(r'dapat masuk', r'bisa_masuk', hsl)
	hsl = re.sub(r'dpt masuk', r'bisa_masuk', hsl)
	return hsl
	
def getStopWords():
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
	
def getNegasi():
	db = MySQLdb.connect("localhost","sent_a", "uppi","android_sa")
	cursor = db.cursor()
	qDataSet = "select word from negasi"
	try:
		cursor.execute(qDataSet)
		results = cursor.fetchall()
		kata = []
		negasi = []
		for row in results:
			kata = row[0]
			negasi.append(kata)
			# Now print fetched result
	except:
		print "Error: unable to fecth data"
	db.close()
	return negasi
	
def hapusStopword(komentar):
	querywords = komentar.split()
	resultwords  = [word for word in querywords if word.lower() not in stopWords]
	result = ' '.join(resultwords)
	return result
	
def tagNegasi(komentar):
	hsl = " " + komentar + " "
	for word in negasi:
		hsl = re.sub(" " + word + " ", " NOT_", hsl)
	return hsl

def preprocessing(komentar):
	hsl = re.sub('[\s]+', ' ', komentar)
	hsl = hsl.lower() #case folding
	hsl = hsl.translate(None, string.punctuation) #punctuation removal
	hsl = gantiKataDasar(hsl) #gnti kata
	hsl = hapusStopword(hsl) #hapus stopwords
	hsl = tagNegasi(hsl) #negation tag
	return hsl	

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

def TentukanSentimenME(komentar):
	komentar = preprocessing(komentar)
	print komentar
	sent = model_klasifikasi.classify(EkstraksiFitur(GetFeatureVector(komentar)))
	return sent

if __name__ == '__main__':
	komen = raw_input("Komentar: ")
	dir_path = os.path.dirname(os.path.realpath(__file__))
	featureList = BacaFitur()
	stopWords = getStopWords()
	negasi = getNegasi()
	model_klasifikasi = pickle.load(open(dir_path + "\\" + "me_model.pickle", "r"))
	print TentukanSentimenME(komen)