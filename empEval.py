# A tool for empirical evaluation of the clusters
# Anouk Visser 

import sys
import shelve

if not len(sys.argv) > 1:
	print "Call me as:"
	print "python empEval.py <sensesOfCOCFile>"
	sys.exit()

inputfile = sys.argv[1]
print "Opening: ", inputfile

coc = shelve.open(inputfile)
while True:
	word = raw_input('Which word would you like to inspect? (type q to quit): ').lower()
	if word == 'q':
		break
	if word in coc:
		wordRep = coc[word]
		sense0 = sorted(wordRep[0].items(), key = lambda x: x[1], reverse=True)
		sense1 = sorted(wordRep[1].items(), key = lambda x: x[1], reverse=True)
		commonTerms = set(sense0).intersection(set(sense1))
		print
		print "Sense 1: "
		one = []
		for term in sense0:
			if term not in commonTerms:
				one.append(term[0])
		print one
		print
		print " ----------------- "
		print

		print "Sense 2: "
		two = []
		for term in sense1:
			if term not in commonTerms:
				two.append(term[0])
		print two
		print
		print "Cluster distance: ", wordRep['clusterDistance']

	else:
		print "This word was not disambiguated..."
	print

print "Goodbye"
