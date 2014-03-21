from math import sqrt
from kmeans import kmeans_process
from collections import defaultdict
import sys
from copy import copy
from random import choice
import shelve

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
	#print set(annotated)

	return annotated



# gives us a new dictionary with multiple senses of the words
# not all words will be in this dictionary, only the words for which 
# multiple senses were actually found
def makeNewCOCS(coc, outputfile, voc):	
	# inititate return object
	#newCOC = dict()
	newCOC = shelve.open(outputfile)

	# get all words
	allWords = coc.keys()
	#allWords = ['apple', 'microsoft', 'jaguar', 'road', 'walk', 'bank', 'to', 'and', 'it', 'firm']
	
	numberOfWords = len(allWords)
	print allWords

	print "Running some statistics on the vocabulary to find which words won't be clustered!"
	
	# We won't be using words that have a unique frequency
	# this is pretty memory intensive... 

	# use a dict #frequency -> int(count)
	# and a dict #frequency -> [wordsWithFrequency]
	frequencyCounts = defaultdict(int)
	frequencyWord = defaultdict(list)

	for word in voc:
		frequencyCounts[voc[word]] += 1
		frequencyWord[voc[word]].append(word)

	wordsToCut = set()

	remove = 0
	
	for freq in frequencyCounts:
		if frequencyCounts[freq] == 1:
			# we can say 0 here, because we know that there is only one...
			wordsToCut.add(frequencyWord[freq][0])
			remove += freq
	
	# now we also want to ensure we delete the 25 words with the highest frequency

	# make a sorted list of frequencies high - low
	frequencies = sorted(frequencyCounts.keys(), reverse=True)

	# add all words that belong to the 25 highest frequencies
	for i in range(25):
		wordsWithHighestFrequency = frequencyWord[frequencies[i]]
		for w in wordsWithFrequency:
			wordsToCut.add(w)
	
	# clear for memory
	frequencyCounts = None
	frequencyWord = None
	frequencies = None
	
	# we will be evaluating the ambiguousness of every single word excpet for ''
	for counter, word in enumerate(allWords):
		
		print counter,  "/", numberOfWords
		print "\n\nMaking sense of: ", word

		# we don't want nothing
		# we don't want words that occur less than 20 times
		if word != '' and voc[word] > 20 and word not in wordsToCut:
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
		else:
			print "Not clustering word: ", word

	return newCOC

print "Welcome to the clustering method designed by Anouk. You'll enjoy your time here."

# ARGUMENTS: 
# input COC !
# output new COC !
# input corpus !
# output new COC / 2 !
# new annotated coprus


if len(sys.argv) < 6:
 		print "Please call me as:"
 		print "python runRemi.py <original coc> <new coc (output)> <training text> <new coc half (output)> <annotated corpus>"
 		sys.exit()

input_file_coc = sys.argv[1]
output_file_new_coc = sys.argv[2]
training_text = sys.argv[3]
output_file_new_coc_half = sys.argv[4]
output_annotated_corpus = sys.argv[5]

# this is the original co-occurence thing, with 'rel', 'coc' and 'voc' as keys
print "Reading global co-occurences (relative frequencies, relatedness scores and vocabulary)"
print input_file_coc + "_rel"
co_occurences = shelve.open(input_file_coc + "_rel")
voc = shelve.open(input_file_coc + "_voc")

# This thing actually makes a co occurence thing with multiple senses of the word
print "Making new co-occurence dictionary, with multiple senses of all words... This might take a while."
new = makeNewCOCS(co_occurences, voc, output_file_new_coc)


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

voc.close()

f = open(output_annotated_corpus, 'w')
f.write("".join(annotated))
f.close()


