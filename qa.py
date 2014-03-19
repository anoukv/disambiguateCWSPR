import sys
import pickle
from collections import defaultdict
from math import sqrt

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
	total = sqrt( sum([v**2 for v in vec]) )
	new_vec = []
	for v in vec:
		new_vec.append(v/total)
	return tuple(new_vec)

def normalize(vec):
	total = sqrt( sum([v**2 for v in vec]) )
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

					# similarity is defined as the cosine similarity
					# cosine similarity normaly is (a (dot product) b) / (norm(a) * norm(b))
					# we have normalized a and b, so the denominator is always one and can be discarded
					sim = sum([y[i] * wordRep[i] for i in xrange(len(y))])

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


# Written by Anouk based on qa.c
def qa_ambiguous(wordvectors, questions):
	
	# initialize empty answers list
	answers = []
	
	# iterate over all questions
	for question in questions:

		# get representations for a, b and c, only if they actually exist
		if question[0] in wordvectors and question[1] in wordvectors and question[2] in wordvectors:
			
			# get the word projections, this is in wordvectors[word]
			# it is a list of tuples
			a_projections = wordvectors[question[0]]
			b_projections = wordvectors[question[1]]
			c_projections = wordvectors[question[2]]

			# y_projections is a list of tuples
			# NOTE: Remi does not want to have all combinations of b-a, but just the 
			# b - a that are close to each other, this could lead to more efficiency
			# but I think using all possible combinations is more sound, for now 
			y_projections = []
			for a in a_projections:
				for b in b_projections:
					for c in c_projections:
						y_projections.append(normalize([b[i] - a[i] + c[i] for i in xrange(len(a))]))

			# initialize bestSim and bestWord
			# sim ranges between -1 and 1, where 1 is most similar
			bestSim = 0
			bestWord = "nothing"
			
			# look at all senses of the word representations to find the answer to a:b c:bestWord
			# except for a, b and c
			for word in wordvectors:
				if word not in question:
					wordReps = wordvectors[word]
					
					# for every word_projection of word, we will compute the similarity 
					# with every y_projection and save the best!
					for wordRep in wordReps:
						for y in y_projections:
							
							# similarity is defined as the cosine similarity
							# cosine similarity normaly is (a (dot product) b) / (norm(a) * norm(b))
							# we have normalized a and b, so the denominator is always one and can be discarded
							sim = sum([y[i] * wordRep[i] for i in xrange(len(y))])

							# save result if it is better than the previous best result
							if sim > bestSim:
								bestSim = sim
								bestWord = word
		
		# If we don't have a projection for a, b, or c, we won't be answering the question.
			print question[0], ' ', question[1], ' ', question[2], ' ', bestWord

		else:
			print "UNSEEN!"
			bestWord = 'nothing'
		answers.append(bestWord)
	return answers


if __name__ == "__main__":
	if not len(sys.argv) == 2:
		print "Call me as:"
		print "python amb_eval.py wordvectors.txt"
		sys.exit()

	print "Loading questions..."
	questions = load_questions()
	
	print "Loading word projections"
	vecs = load_vectors(sys.argv[1])
	
	print "Answering questions"
	answers = qa_ambiguous(vecs, questions)
	
	print "Saving answers to file"
	save_answers(answers, "precomputedAnswers/" + sys.argv[1].split("/")[-1] + ".answered")
	#save_answers(answers, "precomputedAnswers/vectors80.anouk.small.answered")
