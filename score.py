import os, sys

if not len(sys.argv) > 1:
	print "Call me as:"
	print "python score.py ../wordvectors/vectors80.small"
	sys.exit()

def compare(together):
	correct = 0
	for i in together:
		answer = i[0]

		# for the syntactic test downloaded from http://research.microsoft.com/en-us/projects/rnn/
		# has a different format, so that's where the split is needed
		realAnswer = i[1].split(' ')
		if len(realAnswer) > 1:
			realAnswer = realAnswer[1]
		else:
			realAnswer = realAnswer[0]

		# correct++ if the two answers match
		if answer == realAnswer:
			correct += 1

	# compute accuracy
	return correct / float(len(together)) * 100


quest = "QuestionsAnswers/word_relationship.questions"
anser = "QuestionsAnswers/word_relationship.answers"

vecs = sys.argv[1]
vecsname = "precomputedAnswers/" + vecs.split("/")[-1] + ".answered"

if not os.path.isfile(vecsname):
	print "Need to calculate answers for", vecs
	os.system("./qa " + vecs + " " + quest + " " + vecsname)

answers = open(anser, 'r')
reference = open(vecsname, 'r')

ans = answers.readlines()
ref = [ l.lower() for l in reference.readlines() ]

answers.close()
reference.close()

print "\nAccuracy:\t", compare(zip(ref,ans))