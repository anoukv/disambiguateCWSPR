from math import sqrt
from kmeans import kmeans_process
from collections import defaultdict
import sys
from copy import copy
from random import choice
import shelve
from multiprocessing import *

# deletes all the keys from dic that are not in keysToKeep
def deleteSomeKeys(keysToKeep, dic):
	intersection = keysToKeep.intersection(set(dic.keys()))
	new_dic = dict()
	for key in intersection:
		new_dic[key] = dic[key]
	return new_dic

# reads the corpus file
def read_file(filename):
	f = open(filename, 'r')
 	inpt = f.readline().replace("\n", "").split(" ")
 	f.close()
 	return inpt

# annotates the corpus using the multiple senses of a word
def annotate(inpt, clustered, vocabulary, skipsize):
	queueSize = skipsize * 2 + 1

	# two functions
	queueIsReady = lambda x : len(x) == queueSize
	def push(element, queue):
		queue.append(element)
		if len(queue) > queueSize:
			queue.pop(0)

	annotated = []
	queue = []
	for word in inpt:
		push(word, queue)
		if queueIsReady(queue) and word in clustered:	
			coc = set()
			for i in xrange(skipsize):
				if queue[i] in vocabulary:
					word1 = queue[i]
				else:
					word1 = "_UNKNOWN_"
				if queue[i+1+skipsize] in vocabulary:
					word2 = queue[i+1+skipsize]
				else:
					word2 = "_UNKNOWN_"

				coc.add(word1)
				coc.add(word2)

			# Now get the best cluster			
			sense0 = set(clustered[word][0].keys())
			sense1 = set(clustered[word][1].keys())
			intersectionSense0 = len(coc.intersection(sense0))
			intersectionSense1 = len(coc.intersection(sense1))
			if intersectionSense0 > 0 and intersectionSense1 > 0:
				if intersectionSense0 > intersectionSense1:
					word = word + "_" + str(0)
				elif intersectionSense1 > intersectionSense0:
					word = word + "_" + str(1)
				else:
					word = word + "_" + str(choice([0,1]))

		annotated.append(word + " ")
	return annotated

# prepares the data for a word, that is necessary to create the two senses
def prepareExtraction(word, coc):

	# get co-occurences for the word
	wordCOC = copy(coc[word])
	coOccuringWords = set(wordCOC.keys())

	cococ = dict()
	for bla in wordCOC:
		vector = copy(coc[bla])
		vector = deleteSomeKeys(coOccuringWords, vector)
		cococ[bla] =  vector

	return (wordCOC, cococ)

# extracts the two senses of a word
def extractSenses((word, preparation)):
	(wordCOC, cococ) = preparation
	# only if more than one datapoint was found, the word will be called ambiguous


	# sort from high relatedness to low relatedness
	# cut off half, top half will be used, other half will be things that are relevant to all sensess
	tupleList = sorted(wordCOC.items(), key=lambda x: x[1], reverse = True)
	
	relevantCocWords = tupleList[:len(tupleList)/2]
	theRest = tupleList[len(tupleList)/2:]

	cocWords = [ elem[0] for elem in relevantCocWords ]
	relevantToAll = [elem[0] for elem in theRest]

	# for every co-occuring word with the word
	# we save the vector with co-occuring words (only containing words from cocWords)
	# this collection will be datapoints
	listOfDatapoints = [ cococ[elem] for elem in cocWords ]

	# Garbage collection
	cococ = None

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
		sense = copy(wordCOC)
		sense = deleteSomeKeys(set(wordAssignemnts[key]+relevantToAll), sense)
		senses[key] = sense

	# save the different sences of the word
	return (word, senses)

# returns a list of words that have a unique frequency or are in the top 25 of most frequent words
def pruneVocabulary(voc):
	print "Running some statistics on the vocabulary to find which words won't be clustered!"
	wordsToCut = set()	
	vocTups = voc.items()
	sortedVocTups = sorted(vocTups, key = lambda x: x[1], reverse = True)

	for i in range(10):
		wordsToCut.add(sortedVocTups[i][0])
	print

	return wordsToCut

# gives us a new dictionary with multiple senses of the words
# not all words will be in this dictionary, only the words for which 
# multiple senses were actually found
def makeNewCOCS(coc, outputfile, voc):	

	# inititate return object
	print "Writing results to: ", outputfile
	newCOC = shelve.open(outputfile)
	
	#wordsToCut = pruneVocabulary(voc)
	wordsToCut = set()

	print "Not disambiguating: ", len(wordsToCut), " words"
	# we will be evaluating the ambiguousness of every single word excpet for ''
	p = Pool(processes=6)

	counter = 0
	instructions = []
	wordsToDisambiguate = ['apple', 'queen', 'jaguar']
	for word in wordsToDisambiguate:
		counter += 1

		# we don't want nothing
		# we don't want words that occur less than 20 times
		if (word != '' and voc[word] > 0 and  word not in wordsToCut) or True:
		 	print word, counter,  "/ ~50.000"
			# here we cluster! 
			if len(coc[word].keys()) > 5: 
				instructions.append((word, prepareExtraction(word,coc)))
				if len(instructions) == 8:
					print "Agregated instructions, executing..."
					results = p.map(extractSenses, instructions)
					for (w,s) in results:
						newCOC[w] = s
					instructions = []

	print "Executing rest of length", len(instructions)
	results = p.map(extractSenses, instructions)
	for (w,s) in results:
		newCOC[w] = s
	return newCOC

print "Welcome to the clustering method designed by Anouk. You'll enjoy your time here."

if len(sys.argv) < 6:
 		print "Usage: python newCorpus.py <original coc> <new coc (output)> <training text> <new coc half (output)> <annotated corpus>"
 		sys.exit()

input_file_coc = sys.argv[1]
output_file_new_coc = sys.argv[2]
training_text = sys.argv[3]
output_file_new_coc_half = sys.argv[4]
output_annotated_corpus = sys.argv[5]

# this is the original co-occurence thing, with 'rel', 'coc' and 'voc' as keys
print "Reading global co-occurences (relative frequencies, relatedness scores and vocabulary)"
co_occurences = shelve.open(input_file_coc + "_rel")
voc = shelve.open(input_file_coc + "_voc")

# This thing actually makes a co occurence thing with multiple senses of the word
print "Making new co-occurence dictionary, with multiple senses of all words... This might take a while."
new = makeNewCOCS(co_occurences, output_file_new_coc, voc)


# annotate the corpus 
# we might want to decrease new based on cluster distances
# for example, we might only take 50% of the words in here, that have
# the highest cluster distances
print "Throwing away half of the words... "
clustered = sorted(new.items(), key=lambda x: x[1]['clusterDistance'], reverse = True)
halfCOC = shelve.open(output_file_new_coc_half)
halfCOC.update(dict(clustered[:len(clustered)/2]))

# we can close the new one and the original one now.
new.close()
co_occurences.close()
clustered = None

# the input is the text file
print "Reading corpus..."
inpt = read_file(training_text)

print "Annotating corpus."
annotated = annotate(inpt, halfCOC, voc, 5)

f = open(output_annotated_corpus, 'w')
f.write("".join(annotated))
f.close()


voc.close()
halfCOC.close()


