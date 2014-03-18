import pickle
from math import sqrt
from kmeans import kmeans_process
from collections import defaultdict
import sys
from copy import copy

# deletes all the keys from dic that are not in keysToKeep
def deleteSomeKeys(keysToKeep, dic):
	keys = dic.keys()
	for key in keys:
		if key not in keysToKeep:
			dic.pop(key)

def anotate(inpt, skipsize):
	k = 2
	queueSize = skipsize * 2 + 1
	queueMid = skipsize + 1

	queueIsReady = lambda x : len(x) == queueSize
	def push(element, queue):
		queue.append(element)
		if len(queue) > queueSize:
			queue.pop(0)
	
	vocabulary = get_document_vocabulary(inpt)
	vocSize = len(vocabulary) + 1

	print "Starting anotating corpus."
	anotated = []
	queue = []
	for word in inpt:
		push(word, queue)
		if queueIsReady(queue) and word in clustered and len(clustered[word]) > 1:
			coc = defaultdict(int)
			for i in xrange(skipsize):
				if queue[i] in vocabulary:
					word1 = queue[1]
				else:
					word1 = "_UNKNOWN_"
				if queue[i+1+skipsize] in vocabulary:
					word2 = queue[1]
				else:
					word2 = "_UNKNOWN_"

				coc[word1] += 1
				coc[word2] += 1

			coc = normalize_coc(coc)
			# Now get the best cluster
			bestValue = 1
			bestIndex = -1
			for i in xrange(k):
				distance = clustered[word][i].distance(coc)
				if distance < bestValue:
					bestValue = distance
					bestIndex = i
			word = word + "_" + str(bestIndex) + " "

		anotated.append(word)

	return (clustered, anotated)



# gives us a new dictionary with multiple senses of the words
# not all words will be in this dictionary, only the words for which 
# multiple senses were actually found
def makeNewCOCS(cocvoc):
	
	# get the coc (actually 'rel')
	coc = cocvoc['rel']
	
	# inititate return object
	newCOC = dict()

	# get all words
	allWords = coc.keys()
	allWords = ['apple', 'microsoft', 'jaguar', 'road', 'walk', 'bank', 'to', 'and', 'it', 'firm']
	
	numberOfWords = len(allWords)
	print allWords

	# we will be evaluating the ambiguousness of every single word excpet for ''
	for counter, word in enumerate(allWords):
		
		print counter,  "/", numberOfWords
		print "\n\nMaking sense of: ", word

		if word != '':
			listOfDatapoints = []

			# get co-occurences for the word
			wordCOC = copy(coc[word])

			# sort from high relatedness to low relatedness
			# cut off half, top half will be used, other half will be things that are relevant to all sensess
			tupleList = sorted(wordCOC.items(), key=lambda x: x[1], reverse = True)
			
			relevantCocWords = tupleList[:len(tupleList)/2]
			theRest = tupleList[len(tupleList)/2:]

			cocWords = [elem[0] for elem in relevantCocWords]
			relevantToAll = [elem[0] for elem in theRest]

			# for every co-occuring word with the word
			# we save the vector with co-occuring words (only containing words from cocWords)
			# this collection will be datapoints
			for cocWord in cocWords:
				vector = copy(coc[cocWord])
				deleteSomeKeys(cocWords, vector)
				listOfDatapoints.append(vector)
						
			# only if more than one datapoint was found, the word will be called ambiguous
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
				
				# get the cluster distance
				clusterDistance = clusters[0].cluster_distance(clusters[1])
				
				# make a new representations for the different senses of the words
				# save also the cluster distance for future reference
				senses = dict()
				senses['clusterDistance'] = clusterDistance

				# for all clusters, we will now make a new sense of the word
				# the sense will contain the relevantToAll words and the words assigned to the specific cluster
				for key in wordAssignemnts:
					sense = copy(coc[word])
					deleteSomeKeys(wordAssignemnts[key]+relevantToAll, sense)
					senses[key] = sense

				# save the different sences of the word
				newCOC[word] = senses

	return newCOC

print "Welcome to the clustering method designed by Anouk. You'll enjoy your time here."
file_name = sys.argv[1]
co_occurences = pickle.load(open(file_name, 'rb'))
new = makeNewCOCS(co_occurences)
pickle.dump(new, open('../../testingCOC.small', 'wb'))





