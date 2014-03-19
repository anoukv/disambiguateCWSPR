import pickle
from math import sqrt
from kmeans import kmeans_process
from collections import defaultdict
import sys
from copy import copy
from random import choice

# deletes all the keys from dic that are not in keysToKeep
def deleteSomeKeys(keysToKeep, dic):
	keys = dic.keys()
	for key in keys:
		if key not in keysToKeep:
			dic.pop(key)

def read_file(filename):
		f = open(filename, 'r')
	 	inpt = f.readline().replace("\n", "").split(" ")
	 	f.close()
	 	return inpt

def annotate(inpt, clustered, vocabulary, skipsize):
	
	queueSize = skipsize * 2 + 1

	# two functions
	queueIsReady = lambda x : len(x) == queueSize
	def push(element, queue):
		queue.append(element)
		if len(queue) > queueSize:
			queue.pop(0)
	
	print "Starting annotating corpus."
	
	annotated = []
	queue = []
	for word in inpt:
		push(word, queue)
		if queueIsReady(queue) and word in clustered:
			coc = []
			for i in xrange(skipsize):
				if queue[i] in vocabulary:
					word1 = queue[i]
				else:
					word1 = "_UNKNOWN_"
				if queue[i+1+skipsize] in vocabulary:
					word2 = queue[i+1+skipsize]
				else:
					word2 = "_UNKNOWN_"

				coc.append(word1)
				coc.append(word2)

			# Now get the best cluster
			coc = set(coc)
			
			sense0 = set(clustered[word][0].keys())
			sense1 = set(clustered[word][1].keys())
			intersectionSense0 = len(coc.intersection(sense0))
			intersectionSense1 = len(coc.intersection(sense1))
			if intersectionSense0 > intersectionSense1:
				word = word + "_" + str(0)
			elif intersectionSense1 > intersectionSense0:
				word = word + "_" + str(1)
			else:
				word = word + "_" + str(choice([0,1]))

		annotated.append(word + " ")
	#print set(annotated)

	return annotated



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
# this is the original co-occurence thing, with 'rel', 'coc' and 'voc' as keys
co_occurences = pickle.load(open(file_name, 'rb'))

# This thing actually makes a co occurence thing with multiple senses of the word
#new = makeNewCOCS(co_occurences)
#pickle.dump(new, open('../../testingCOC.small', 'wb'))

# this thing opens an existing co occurence thing
new = pickle.load(open('../../newCOC.small', 'rb'))

# the input is the text file
inpt = read_file('../../text.small')

# annotate the corpus 
# we might want to decrease new based on cluster distances
# for example, we might only take 50% of the words in here, that have
# the highest cluster distances
annotated = annotate(inpt, new, co_occurences['voc'], 5)

f = open('../../text.anouk.small', 'w')
f.write("".join(annotated))
f.close()

# To run this script without intervention do something like: 
# file_name = sys.argv[1]
# co_occurences = pickle.load(open(file_name, 'rb'))
# new = makeNewCOCS(co_occurences)
# pickle.dump(new, open('../../testingCOC.small', 'wb'))
# inpt = read_file('../../text.small')
# # annotate the corpus 
# # we might want to decrease new based on cluster distances
# # for example, we might only take 50% of the words in here, that have
# # the highest cluster distances
# annotated = annotate(inpt, new, co_occurences['voc'], 5)
# f = open('../../text.anouk.small', 'w')
# f.write("".join(annotated))
# f.close()


