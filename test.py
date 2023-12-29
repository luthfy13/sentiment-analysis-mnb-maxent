import os.path
import nltk
import MySQLdb
import re, pickle, csv, os, sys, string
import pprint

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
	
def tagNegasi(komentar):
	hsl = " " + komentar + " "
	for word in getNegasi():
		hsl = re.sub(" " + word + " ", " NOT_", hsl)
	return hsl
	
print tagNegasi("Udah diperbaharui kok gak bisa di buka?")