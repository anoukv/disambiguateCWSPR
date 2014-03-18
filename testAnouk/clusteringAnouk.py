import pickle
from math import sqrt
from kmeans import kmeans_process
from collections import defaultdict
import sys
from copy import copy

def deleteSomeKeys(keysToKeep, dic):
	keys = dic.keys()
	for key in keys:
		if key not in keysToKeep:
			dic.pop(key)

def test(cocvoc):
	coc = cocvoc['rel']

	# get all words
	allWords = coc.keys()
	allWords = ['apple']#, 'jaguar', 'bank', 'memory', 'process']
	
	# we will be evaluating the ambiguousness of every single word
	for word in allWords:
		print "\n\nMaking sense of: ", word

		if word != '':
			listOfDatapoints = []

			# get co-occurences for the word
			wordCOC = copy(coc[word])

			# cut of half of this thing...
			# is there a better heuristic available? 
			tupleList = sorted(wordCOC.items(), key=lambda x: x[1], reverse = True)
			
			relevantCocWords = tupleList[:len(tupleList)/2]
			theRest = tupleList[len(tupleList)/2:]

			
			cocWords = [elem[0] for elem in relevantCocWords]
			relevantToAll = [elem[0] for elem in theRest]

			print "Found ", len(wordCOC.keys()), " co-occuring words, only ", len(cocWords), " remain"

			for cocWord in cocWords:
				vector = copy(coc[cocWord])
				deleteSomeKeys(cocWords, vector)
				listOfDatapoints.append(vector)
						
			if len(listOfDatapoints) > 1:
				# cluster all co-occurence vectors
				clusters = kmeans_process(listOfDatapoints)
				
				# find out which term belongs to which cluster
				wordAssignemnts = defaultdict(list)
				for i, cocWord in enumerate(cocWords):
					bestClusterID = "NONE"
					bestDistance = 2
					for clusterID in clusters:
						dist = clusters[clusterID].distance(listOfDatapoints[i])
						if dist < bestDistance:
							bestDistance = dist
							bestClusterID = clusterID
					wordAssignemnts[bestClusterID].append(cocWord)
				
				senses = dict()

				for key in wordAssignemnts:
					sense = copy(coc[word])
					deleteSomeKeys(wordAssignemnts[key]+relevantToAll, sense)
					senses[key] = sense

				print senses



			# now this words needs to be splitted


print "Welcome to the clustering method designed by Anouk. You'll enjoy your time here."
file_name = sys.argv[1]
co_occurences = pickle.load(open(file_name, 'rb'))
test(co_occurences)






