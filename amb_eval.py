import sys
import pickle
from collections import defaultdict
from math import sqrt

questions = "QuestionsAnswers/word_relationship.questions"

def load_questions(filename=questions):
	f = open(filename, 'r')
	c = [ tuple(l.replace("\n","").split(" ")) for l in f.readlines()]
	f.close()
	return c

def load_vectors(filename):
	def normalize(vec):
		vec = [ float(x) for x in vec]
		total = sqrt( sum([v**2 for v in vec]) )
		new_vec = []
		for v in vec:
			new_vec.append(v/total)
		return tuple(new_vec)

	f = open(filename,'r')
	f.readline()
	content = [ filter( lambda x : not x in ["\n",""], l.split(" ")) for l in f.readlines() ]
	content = [ (l[0], normalize(l[1:])) for l in content ]
	content = filter(lambda x : not x[1] == None, content)
	words = defaultdict(list)
	for (word, vector) in content:
		if "_" in word:
			words[word.split("_")[0]].append((word,vector))
		else:
			words[word].append((word,vector))
	return words

def save_answers(answers, filename):
	f = open(filename, 'w')
	f.write( "".join([ word + "\n" for word in answers]) )
	f.close()

def vector_distance(vec1, vec2):
	return sum([x[0] * x[1] for x in zip(vec1,vec2)])

def vector_add(vec1, vec2):
	return [ x[0] + x[1] for x in zip(vec1, vec2) ]

def answer((a,b,c), vecs):
	for e in (a,b,c):
		if e not in vecs or len(vecs[e[0]]) == 0:
			return "NONE"

	print 
	print "Working..."
	for e in (a,b,c):
		print len(vecs[e]) == 0

	def find_AB_match(a,b,vecs):
		best_distance = 2
		best_tuple = (None,None)
		print len(vecs[a])
		print len(vecs[b])
		for va in vecs[a]:
			for vb in vecs[b]:
				distance = vector_distance(va[1],vb[1])
				print distance
				if distance < best_distance:
					best_distance = distance
					best_tuple = (va[1], vb[1])
		print "Distance:", best_distance
		return best_tuple

	(av, bv) = find_AB_match(a,b,vecs)
	diff = map(lambda x : x[0] - x[1], zip(av,bv))

	cvs = [ v[1] for v in vecs[c] ]

	best_distance = 2
	best_word = "NONE"
	for reference_vec in cvs:
		for key in vecs.keys():
			for v in vecs[key]:
				new_vec = vector_add(v[1], diff)
				distance = vector_distance(reference_vec, new_vec)
				if distance < best_distance:
					best_distance = distance
					best_word = key
	return best_word



if __name__ == "__main__":
	if not len(sys.argv) == 3:
		print "Call me as:"
		print "python amb_eval.py wordvectors.txt outpusfile.txt"
		sys.exit()

	questions = load_questions()
	vecs = load_vectors(sys.argv[1])
	answers = map(lambda x : answer(x, vecs), questions)
	save_answers(answers, sys.argv[2])
	
















