import sys
from collections import defaultdict
from time import time
import pickle
from math import sqrt

from clustering import kmeans_process

def get_document_vocabulary(inpt, minimumOccurence = 5):
	total = defaultdict(int)
	for word in inpt:
		total[word] += 1
	return set([ key for key in total.keys() if total[key] > minimumOccurence ])

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

	print "Starting on determining word co-occurences."

	cocs = defaultdict(list)
	queue = []
	for word in inpt:
		push(word, queue)
		if queueIsReady(queue):
			mid = queue[queueMid]
			#print "mid: " + mid
			if mid in vocabulary:
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
				#print "final co-occurences"
				#print coc
				cocs[mid].append(coc)
				#print "Coc[mid]"
				#print cocs[mid]

	print "Now clustering..."

	clustered = dict()
	for key in cocs.keys():
            print "KEY:" + key
            print "\ncocs[" + key + "]:"
            print cocs[key]
	    clustered[key] = kmeans_process(cocs[key])

	print "Starting anotating corpus."
	anotated = []
	queue = []
	for word in inpt:
		push(word, queue)
		if queueIsReady(queue):
			word = queue[queueMid]
			if word in clustered and len(clustered[word]) > 1:
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
				word = word + "_" + str(bestIndex) + " "
			anotated.append(word)

	return (clustered, anotated)

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

 	(clustered, anotated) = anotate(inpt, skipsize)

 	f = open(output_file, 'w')
 	f.write("".join(anotated))
 	f.close()
 	pickle.dump(clustered, open("clusters.pickle", 'wb'))


if __name__ == "__main__":
	start = time()
	main_cluster_remi()
	stop = time()
 	print "I spent", int(stop-start+0.5), "seconds."

