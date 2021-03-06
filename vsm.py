# Vecter Space Model (tf/idf) Search by Joe Williams

import os
import sys
import math
import nltk

from nltk.corpus import stopwords as s

stopwords = set(s.words('english'))
docdir = "./corpus/"
docnames = [a for a in os.listdir(docdir) if not a == ".DS_Store"]

# loads all documents in 'docdir'
def loadDocs(docs):
	if not os.path.exists(docdir):
		print("No folder called '"+docdir+"'. Please create one and put documents inside.")
		exit()
	data = [clean(open( docdir + a, encoding='ISO-8859-1').read()) for a in docs]
	data = [list(filter(lambda a: not a in stopwords and a != '', a.split(" "))) for a in data]
	return data

# Gets rid of special characters
def clean(text):
	l = '\\\t"^`/!@#$%&()}{]|[;:+*<>=~-.,_'
	text = text.replace('\n',' ')
	for a in l:
		if a in text:
			text = text.replace(a,'')
	return text.lower()

# Calculates the score of a term in a doc (cosine to normalize)
def tfidf(corpus, index, term):
	tf = count(corpus[index], term) / len(corpus[index])
	num_docs_with_term = len([b for b in corpus if term in b])
	if num_docs_with_term == 0: idf = 0
	else:
		df = len(corpus) / num_docs_with_term
		idf = math.log(df) if df > 1 else 1
	return math.cos(tf * idf) if tf > 0 and idf > 0 else 0

# Count how many times 'item' occurs in 'arr'
def count(arr,item):
	return len([e for e in arr if e == item])

# Prints query results
def printResults(arr,stem):
	c = sorted(enumerate(arr), key=lambda t: float(t[1]), reverse=0)
	b = [t for t in c if not float(t[1]) == 0]
	if len(b) < 3: l = len(b)
	else: l = 3
	if l > 0: print("Top "+str(l)+" Docs: "+
			', '.join([docnames[i] for i, _ in b[:l]]))
	else:
		print("No matching documents")
	if stem:
		print("Warning: One or more of your words is a stem word!")
	print()

docs = loadDocs(docnames)

# User Interface
while(1):
	print("Enter search query (ex: john doe)")
	sys.stdout.write("'/exit' to close > ")
	words = clean(input()).split(" ")
	if len(words) == 1 and words[0] == "/exit": exit()
	queryAvgs = []
	stem = False
	for i in range(0, len(docs)):
		tot = float(0)
		for word in words:
			if not stem: stem = word in stopwords 
			tot += tfidf(docs,i,word)
		queryAvgs.append(tot/len(words))
	printResults(queryAvgs,stem)
