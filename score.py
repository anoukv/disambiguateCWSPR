import os, sys

if not len(sys.argv) > 2:
	print "Call me as:"
	print "python score.py <projections> <answers>"
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

vecs = sys.argv[1]
answer = sys.argv[2]

vecsname = "precomputedAnswers/" + vecs.split("/")[-1] + "." + answer.split("/")[-1].split(".")[0] + ".answered"

if not os.path.isfile(vecsname):
	print "Need to calculate answers for", vecs
	os.system("pypy qa.py " + vecs + " " + answer)

answers = open(answer, 'r')
reference = open(vecsname, 'r')

ans = [ l.lower().replace("\n","") for l in answers.readlines() ]
ref = [ l.lower().replace("\n","") for l in reference.readlines() ]

answers.close()
reference.close()

print "\nAccuracy:\t", compare(zip(ref,ans))