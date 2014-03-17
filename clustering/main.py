import sys
from collections import defaultdict
from time import time

from clustering import kmeans_process

def get_document_vocabulary(inpt, minimumOccurence = 5):
	total = defaultdict(int)
	for word in inpt:
		total[word] += 1
	return set([ key for key in total.keys() if total[key] > minimumOccurence ])

def normalize_coc(coc):
	total = float(sum(coc.values()))
	new_coc = dict()
	for key in coc.keys():
		new_coc[key] = coc[key] / total
	return new_coc

def getCocMatrix(inpt,skipsize):
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

	wordToVec = dict()
	for word in vocabulary:
		wordToVec[word] = defaultdict(int)

	queue = []
	for word in inpt:
		push(word, queue)
		if queueIsReady(queue):
			mid = queue[queueMid]
			if mid in vocabulary:
				for i in xrange(skipsize):
					if queue[i] in vocabulary:
						word1 = queue[1]
					else:
						word1 = "UNKNOWN"
					if queue[i+1+skipsize] in vocabulary:
						word2 = queue[1]
					else:
						word2 = "UNKNOWN"
				
				

				wordToVec[mid][word1] += 1
				wordToVec[mid][word2] += 1

	normalized_wordToVec = dict()
	for word in wordToVec.keys():
		normalized_wordToVec[word] = normalize_coc(wordToVec[word])

	return normalized_wordToVec

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

	wordToIndex = dict()
	for i in xrange(len(vocabulary)):
		wordToIndex[vocabulary[i]] = i 

	print "Starting on determining word co-occurences and clustering."
	clustered = dict()
	for v in vocabulary:
		wordVectorSet = []
		queue = []
		for word in inpt:
			push(word, queue)
			if queueIsReady(queue) and queue[queueMid] == v:
				coc = defaultdict(int)
				for i in xrange(skipsize):
					try:
						index1 = wordToIndex[queue[i]]
					except:
						index1 = vocSize# The 'unknown' category
					try:
						index2 = wordToIndex[queue[i+1+skipsize]]
					except:	
						index2 = vocSize-1 # The 'unknown' category

					coc[index1] += 1
					coc[index2] += 1
				wordVectorSet.append(normalize_coc(coc))
		clustered[v] = kmeans_process(wordVectorSet)

	print "Starting anotating corpus."
	anotated = []
	queue = []
	for word in inpt:
		push(word, queue)
		if queueIsReady(queue) and word in clustered and len(clustered[word]) > 1:
			coc = defaultdict(int)
			for i in xrange(skipsize):
				try:
					index1 = wordToIndex[queue[i]]
				except:
					index1 = vocSize# The 'unknown' category
				try:
					index2 = wordToIndex[queue[i+1+skipsize]]
				except:	
					index2 = vocSize-1 # The 'unknown' category

				coc[index1] += 1
				coc[index2] += 1

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

	return anotated



def read_args():
	def read_file(filename):
		f = open(train, 'r')
	 	inpt = f.readline().replace("\n", "").split(" ")
	 	f.close()
	 	return inpt

	if len(sys.argv) < 3:
 		print "Please call me as:"
 		print "python cluster.py training.txt output.txt (skipsize = 5)"
 		sys.exit()

	train = sys.argv[1]
 	output_file = sys.argv[2]
 	skipsize = 5
 	if len(sys.argv) == 4:
 		skipsize = int(sys.argv[3])

 	return (read_file(train), output_file, skipsize)


def main_cluster_remi():
	(inpt, output_file, skipsize) = read_args()

 	print "Preparing data."

 	anotated = anotate(inpt, skipsize)

 	f = open(output_file, 'w')
 	f.write("".join(anotated))
 	f.close()


def main_anouk_is_a_charm():
	(inpt, output_file, skipsize) = read_args()

	coc = getCocMatrix(inpt, skipsize)

	import pickle
	pickle.dump(coc, open(output_file, 'wb'))


	

if __name__ == "__main__":
	start = time()
	main_anouk_is_a_charm()
	stop = time()
 	print "I spent", int(stop-start+0.5), "seconds."

