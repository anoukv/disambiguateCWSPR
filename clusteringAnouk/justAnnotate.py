import sys
import shelve
from random import choice
from multiprocessing import *

# reads the corpus file
def read_file(filename):
	f = open(filename, 'r')
 	inpt = f.readline().replace("\n", "").split(" ")
 	f.close()
 	return inpt

# annotates the corpus using the multiple senses of a word
def annotate(inpt, clustered, vocabulary, skipsize):
	queueSize = skipsize * 2 + 1
	clusteredKeys = set(clustered.keys())

	# two functions
	queueIsReady = lambda x : len(x) == queueSize
	def push(element, queue):
		queue.append(element)
		if len(queue) > queueSize:
			queue.pop(0)

	annotated = []
	queue = []
	total = len(inpt)
	for i, word in enumerate(inpt):
		push(word, queue)
		if queueIsReady(queue) and word in clusteredKeys:	
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
					# instead choice we could for example choose the previous thing
					word = word + "_" + str(choice([0,1]))

		annotated.append(word + " ")
	return annotated

print "Welcome to the clustering method designed by Anouk. You'll enjoy your time here."

if len(sys.argv) < 4:
 		print "Please call me as:"
 		print "python justAnnotate.py <newCOC> <training text> <output file> <vocabulary>"
 		print "python justAnnotate.py ../../newCOC.medium ../../text.medium ../../newAnnotated.medium ../../coc.medium_voc"
 		sys.exit()

input_file = sys.argv[1]
training_text = sys.argv[2]
output_annotated_corpus = sys.argv[3]
vocabulary = sys.argv[4]

# the input is the text file
print "Reading corpus..."
inpt = read_file(training_text)

print input_file
print vocabulary
coc = shelve.open(input_file)
print "opened coc"
voc = shelve.open(vocabulary)

print "Annotating corpus."
annotated = annotate(inpt, coc, voc, 5)

f = open(output_annotated_corpus, 'w')
f.write("".join(annotated))
f.close()


voc.close()
coc.close()


