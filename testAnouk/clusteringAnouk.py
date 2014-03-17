import pickle
from math import sqrt
from kmeans import kmeans_process
from collections import defaultdict
import sys

def makeCustomDic(keysToKeep, dic):
	keys = dic.keys()
	for key in keys:
		if key not in keysToKeep:
			dic.pop(key)

def prettyPrint(assignments):
	for key in assignments:
		print "Sense ", key
		print assignments[key]
		
def test(cocvoc):
	coc = cocvoc['rel']
	voc = cocvoc['voc']

	# get all words
	allWords = coc.keys()
	allWords = ['apple', 'jaguar', 'bank', 'computer', 'memory', 'process', 'water', 'river', 'rain', 'meaning', 'outside', 'nature', 'science', 'university']
	# we will be evaluating the ambiguousness of every single word
	for word in allWords:
		print "\n\nMaking sense of: ", word

		if word != '':
			listOfDatapoints = []

			# get co-occurences for the word
			wordCOC = coc[word]

			# cut of half of this thing...
			# is there a better heuristic available? 
			tupleList = sorted(wordCOC.items(), key=lambda x: x[1], reverse = True)
			tupleList = tupleList[:len(tupleList)/2]
			cocWords = [elem[0] for elem in tupleList]

			#cocWords = wordCOC.keys()

			# for every co-occuring word, filter out terms that do not apply
			# add the remaining vector to the list of datapoints
			
			print "Found ", len(wordCOC.keys()), " co-occuring words, only ", len(cocWords), " remain"

			for cocWord in cocWords:
				vector = coc[cocWord]
				makeCustomDic(cocWords, vector)
				listOfDatapoints.append(coc[cocWord])
						
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
				
				prettyPrint(wordAssignemnts)

			# now this words needs to be splitted


print "Welcome to the clustering method designed by Anouk. You'll enjoy your time here."
file_name = sys.argv[1]
co_occurences = pickle.load(open(file_name, 'rb'))
test(co_occurences)






