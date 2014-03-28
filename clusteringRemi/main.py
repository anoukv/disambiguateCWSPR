import sys
from collections import defaultdict
import shelve
from time import time
import pickle
from math import sqrt

from clustering import kmeans_process

def get_document_vocabulary(inpt, minimumOccurence = 5):
	total = defaultdict(int)
	for word in inpt:
		total[word] += 1
	return set([ key for key in total.keys() if total[key] > minimumOccurence ])

def normalize_coc(coc):
	total = sqrt( sum([v**2 for v in coc.values()]) )
	new_coc = dict()
	for key in coc.keys():
		new_coc[key] = coc[key] / total
	return new_coc

def anotate(inpt, skipsize):
	k = 2
	queueSize = skipsize * 2 + 1
	queueMid = skipsize + 1

	queueIsReady = lambda x : len(x) == queueSize
	def push(element, queue):
		queue.append(element)
		if len(queue) > queueSize:
			queue.pop(0)

	def map_append(dic, key, elem):
		if key in dic:
			l = dic[key]
			l.append(elem)
			dic[key] = l
		else:
			dic[key] = [elem]
	
	vocabulary = get_document_vocabulary(inpt)
	vocSize = len(vocabulary) + 1

	totalWords = len(inpt)

	print vocSize, "words in vocabulary."
	print "Starting on determining word co-occurences of", totalWords, "words"


	cocs = defaultdict(list)
	queue = []
	for i in xrange(queueSize):
		word = inpt[i]
		push(word, queue)

	for counter in xrange(queueSize, len(inpt)):
		word = inpt[counter]
		if counter % 100000 == 0:
			print "Part", counter / 100000, "of", totalWords / 100000, "parts."
		push(word, queue)
		mid = queue[queueMid]
		if mid in vocabulary:
			coc = defaultdict(int)
			for i in xrange(skipsize):
				if queue[i] in vocabulary:
					word1 = queue[i]
				else:
					word1 = "_UNKNOWN_"
				if queue[i+1+skipsize] in vocabulary:
					word2 = queue[i+1+skipsize]
				else:
					word2 = "_UNKNOWN_"

				coc[word1] += 1
				coc[word2] += 1

			cocs[mid].append(normalize_coc(coc))

	print "Found",len(cocs),"co-occurence vectors."

	print "Now clustering..."

	clustered = []
	for key in cocs:
		c = kmeans_process(cocs[key])
		if len(c) == 2:
			clustered.append((c[0].cluster_distance(c[1]), key, c))

	clustered = sorted(clustered, key = lambda x : x[0])
	clustered = clustered[0:len(clustered)/2]
	clustered = dict([ (x[1], x[2]) for x in clustered] )

	clustered_words = set(clustered.keys())

	print "Clustered words:", clustered_words

	print "Starting anotating corpus."
	anotated = []
	queue = []
	for i in xrange(queueSize):
		word = inpt[i]
		push(word, queue)


	for counter in xrange(queueSize, len(inpt)):
		word = inpt[counter]
		push(word, queue)
		word = queue[queueMid]
		if word in clustered_words:
			coc = defaultdict(int)
			for i in xrange(skipsize):
				if queue[i] in vocabulary:
					word1 = queue[i]
				else:
					word1 = "_UNKNOWN_"
				if queue[i+1+skipsize] in vocabulary:
					word2 = queue[i+1+skipsize]
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
			word = word + "_" + str(bestIndex)
		anotated.append(word + " ")

	return anotated

def read_args():
	def read_file(filename):
		f = open(filename, 'r')
	 	inpt = f.readline().replace("\n", "").split(" ")
	 	f.close()
	 	return inpt

	if len(sys.argv) < 3:
 		print "Please call me as:"
 		print "python main.py training.txt output.txt (skipsize = 5)"
 		sys.exit()

 	skipsize = 5
 	if len(sys.argv) == 4:
 		skipsize = int(sys.argv[3])

 	return (read_file(sys.argv[1]), sys.argv[2], skipsize)


def main_cluster_remi():
	(inpt, output_file, skipsize) = read_args()

 	print "Preparing data."

 	anotated = anotate(inpt, skipsize)

 	f = open(output_file, 'w')
 	f.write("".join(anotated))
 	f.close()


if __name__ == "__main__":
	start = time()
	main_cluster_remi()
	stop = time()
 	print "I spent", int(stop-start+0.5), "seconds."

