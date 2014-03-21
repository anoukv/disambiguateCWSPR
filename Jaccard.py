from __future__ import division
import sys
import pickle, math
import numpy as np
from collections import defaultdict
from scipy import stats

questions = "QuestionsAnswers/word_relationship.questions"

# Written by Remi
# Approved by Anouk
def save_answers(answers, filename):
	f = open(filename, 'w')
	f.write( "".join([ word + "\n" for word in answers]) )
	f.close()

# Written by Remi
# Approved and edited by Anouk (made all words lower case)
def load_questions(filename=questions):
	f = open(filename, 'r')
	c = [ tuple(l.lower().replace("\n","").split(" ")) for l in f.readlines()]
	f.close()
	return c

# Written by Remi
# Approved by Anouk
def normalizeString(vec):
	vec = [ float(x) for x in vec]
	total = math.sqrt( sum([v**2 for v in vec]) )
	new_vec = []
	for v in vec:
		new_vec.append(v/total)
	return tuple(new_vec)

def normalize(vec):
	total = math.sqrt( sum([v**2 for v in vec]) )
	new_vec = []
	for v in vec:
		new_vec.append(v/total)
	return tuple(new_vec)

# written by Remi
# Approved and edited by Anouk (made all words lower case and took out internal normalize function)
def load_vectors(filename):
	f = open(filename,'r')
	f.readline()
	content = [ filter( lambda x : not x in ["\n",""], l.replace("\n", "").split(" ")) for l in f.readlines() ]
	content = [ (l[0], normalizeString(l[1:])) for l in content ]
	content = filter(lambda x : not x[1] == None, content)
	words = defaultdict(list)
	for (word, vector) in content:
		if "_" in word:
			words[word.lower().split("_")[0]].append(vector)
		else:
			words[word.lower()].append(vector)
	return words

# Written by Anouk based on qa.c
def qa(wordvectors, questions):
	
	# initialize empty answers list
	answers = []
	
	# iterate over all questions
	for question in questions:

		# get representations for a, b and c, only if they actually exist
		if question[0] in wordvectors and question[1] in wordvectors and question[2] in wordvectors:
			
			# get the word projections, this is in wordvectors[word], we assume for now that 
			# there is only one word projection, but the content of wordvectors[word] is a list
			# so we have to ask for index 0
			a = wordvectors[question[0]][0]
			b = wordvectors[question[1]][0]
			c = wordvectors[question[2]][0]

			# compute v, normalize it. Result is a tuple
			y = normalize([b[i] - a[i] + c[i] for i in xrange(len(a))])

			# initialize bestSim and bestWord
			# sim ranges between -1 and 1, where 1 is most similar
			bestSim = 0
			bestWord = "nothing"
			
			# look at all word representations to find the answer to a:b c:bestWord
			# except for a, b and c
			for word in wordvectors:
				if word not in question:

					# again assume that there is only one projection for the word
					wordRep = wordvectors[word][0]
                                        
					#Compute similary between the two vectors
                                        #sim = CosineSimilarity(y, wordRep)  
                                        #sim = EuclideanDistance(y, wordRep)
					sim = JaccardDistance(y, wordRep)
                                        #sim = PearsonCorrelation(y, wordRep)
                                        #sim = SpearmanCorrelation(y, wordRep)
					#sim = MahalanobisDist(y, wordRep)
					                                        
					# save result if it is better than the previous best result
					if sim > bestSim:
						bestSim = sim
						bestWord = word
		
		# If we don't have a projection for a, b, or c, we won't be answering the question.
		else:
			bestWord = 'nothing'
		answers.append(bestWord)
		print question[0], ' ', question[1], ' ', question[2], ' ', bestWord
	return answers

def CosineSimilarity(vec1, vec2):
        # similarity is defined as the cosine similarity
	# cosine similarity normaly is (a (dot product) b) / (norm(a) * norm(b))
	# we have normalized a and b, so the denominator is always one and can be discarded
        return sum([vec1[i] * vec2[i] for i in xrange(len(vec1))])

def EuclideanDistance(vec1, vec2):
        return 1/(1 + math.sqrt(sum([(vec1[i] - vec2[i])**2 for i in xrange(len(vec1))])))

def JaccardDistance(vec1, vec2):
        #Jaccard / Tanimoto Coefficient
        #vec3 = list(set(vec1).intersection(set(vec2)))
        #return float(len(vec3)) / (len(vec1) + len(vec2) - len(vec3))
        
        n = len(set(vec1).intersection(set(vec2)))
        return 1+ (1 + n / float(len(vec1) + len(vec2) - n))

def average(x):
        assert len(x) > 0
        return float(sum(x)) / len(x)

def PearsonCorrelation(x, y):
        assert len(x) == len(y)
        n = len(x)
        assert n > 0
        avg_x = average(x)
        avg_y = average(y)
        diffprod = 0
        xdiff2 = 0
        ydiff2 = 0
        for i in range(n):
                xdiff = x[i] - avg_x
                ydiff = y[i] - avg_y
                diffprod += xdiff * ydiff
                xdiff2 += xdiff * xdiff
                ydiff2 += ydiff * ydiff

        return diffprod / math.sqrt(xdiff2 * ydiff2)

def SpearmanCorrelation(x,y):
    return stats.stats.spearmanr(x, y)[0]

def MahalanobisDist(x, y):
        covariance_xy = np.cov(x,y, rowvar=0)
        inv_covariance_xy = np.linalg.inv(covariance_xy)
        xy_mean = np.mean(x),np.mean(y)
        x_diff = np.array([x_i - xy_mean[0] for x_i in x])
        y_diff = np.array([y_i - xy_mean[1] for y_i in y])
        diff_xy = np.transpose([x_diff, y_diff])

        md = []
        dist = 0
        for i in range(len(diff_xy)):
                md.append(np.sqrt(np.dot(np.dot(np.transpose(diff_xy[i]),inv_covariance_xy),diff_xy[i])))
                dist += md[i]
        return dist/len(md)
        
if __name__ == "__main__":
	if not len(sys.argv) == 2:
		print "Call me as:"
		print "python qa_cristina.py wordvectors.txt"
		sys.exit()

	print "Loading questions..."
	questions = load_questions()
	
	print "Loading word projections"
	vecs = load_vectors(sys.argv[1])
	
	print "Answering questions"
	answers = qa(vecs, questions)
	
	print "Saving answers to file"
	save_answers(answers, "precomputedAnswers/testCristinaJaccardDistance.answered")
















