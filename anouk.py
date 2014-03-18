import sys
from collections import defaultdict
from time import time
import pickle

def get_document_vocabulary(inpt, minimumOccurence = 5):
	total = defaultdict(int)
	for word in inpt:
		total[word] += 1
	s = sum(total.values())
	voc = dict([ (key, total[key]) for key in total.keys() if total[key] > minimumOccurence ])
	voc["_UNKNOWN_"] = s - sum(voc.values())
	return voc


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
						word1 = "_UNKNOWN_"
					if queue[i+1+skipsize] in vocabulary:
						word2 = queue[1]
					else:
						word2 = "_UNKNOWN_"
				
					wordToVec[mid][word1] += 1
					wordToVec[mid][word2] += 1

	normalized_wordToVec = dict()
	for word in wordToVec.keys():
		normalized_wordToVec[word] = normalize_coc(wordToVec[word])

	return dict( {'voc': vocabulary, 'coc' : normalized_wordToVec} )


def read_args():
	def read_file(filename):
		f = open(train, 'r')
	 	inpt = f.readline().replace("\n", "").split(" ")
	 	f.close()
	 	return inpt

	if len(sys.argv) < 3:
 		print "Please call me as:"
 		print "python main.py training.txt output.txt (skipsize = 5)"
 		sys.exit()

	train = sys.argv[1]
 	output_file = sys.argv[2]
 	skipsize = 5
 	if len(sys.argv) == 4:
 		skipsize = int(sys.argv[3])

 	return (read_file(train), output_file, skipsize)


def main_anouk_is_a_charm():
	(inpt, output_file, skipsize) = read_args()

	coc = getCocMatrix(inpt, skipsize)

	pickle.dump(coc, open(output_file, 'wb'))
	

if __name__ == "__main__":
	start = time()
	main_anouk_is_a_charm()
	stop = time()
 	print "I spent", int(stop-start+0.5), "seconds."
