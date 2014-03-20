import sys
import pickle
from collections import defaultdict
from math import sqrt


# Written by Remi
# Approved by Anouk
def save_answers(answers, filename):
	f = open(filename, 'w')
	f.write( "".join([ str(answer[0])+" "+answer[1][0]+":"+answer[1][1]+"\n" for answer in answers]) )
	f.close()

def load_questions(filename):
	f = open(filename, 'r')
	questions = []
	for _ in xrange(4):
		f.readline()
	while True:
		l = f.readline()
		if l not in ["", "\n", "\r\n"]:
			questions.append(tuple(l.lower().replace("\n", "").split(":")))
		else:
			break
	f.close()
	return questions

def load_answers(filename):
	f = open(filename, 'r')
	answers = [ tuple(l.lower().replace("\n","").replace('"', '').split(":")) for l in f.readlines()]
	f.close()
	return answers 

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
def qa(wordvectors, questions, answers):
	
	# initialize empty answers list
	ranking = []

	for answer in answers:
		# compute cosine similarity with all questions
		sim = 0
		for question in questions:
			if question[0] in wordvectors and question[1] in wordvectors and answer[0] in wordvectors and answer[1] in wordvectors:
				a = wordvectors[question[0]][0]
				b = wordvectors[question[1]][0]
				c = wordvectors[answer[0]][0]
				d = wordvectors[answer[1]][0]

				y = normalize([b[i] - a[i] + c[i] for i in xrange(len(a))])
				sim += sum([y[i] * d[i] for i in xrange(len(y))])
			else:
				sim = -10
		sim = sim / float(len(questions))
		ranking.append((sim, answer))
	return sorted(ranking, key = lambda x: x[0], reverse = True)


if __name__ == "__main__":
	if not len(sys.argv) == 4:
		print "Call me as:"
		print "python semEvalQA.py <wordvectors> <questions> <answers>"
		sys.exit()

	projections = sys.argv[1]
	questionsFile = sys.argv[2]
	answersFile = sys.argv[3]

	print "Loading questions..."
	questions = load_questions(questionsFile)
	print "Loaded ", len(questions), " questions."

	print "Loading answers..."
	answers = load_answers(answersFile)
	print "Loaded ", len(answers), " answers"
	
	print "Loading word projections"
	vecs = load_vectors(projections)
	
	print "Answering questions"
	ranking = qa(vecs, questions, answers)
	
	print "Saving answers to file"
	save_answers(ranking, "SemEvalRankings/" + projections.split("/")[-1] + "." + questionsFile.split("/")[-1].split(".")[0] + ".answered")
	#save_answers(ranking, "test")
