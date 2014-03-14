import os, sys

if not len(sys.argv) == 3:
	print "Call me as:"
	print "python cmp.py ../wordvectors/vectors80.large ../wordvectors/vectors320.small"
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

vecs1 = sys.argv[1]
vecs2 = sys.argv[2]
quest = "QuestionsAnswers/word_relationship.questions"
anser = "QuestionsAnswers/word_relationship.answers"

os.system("./qa " + vecs1 + " " + quest + " tmp1")
os.system("./qa " + vecs2 + " " + quest + " tmp2")

answers = open(anser, 'r')
reference1 = open("tmp1", 'r')
reference2 = open("tmp2", 'r')

ans = answers.readlines()
ref1 = [ l.lower() for l in reference1.readlines() ]
ref2 = [ l.lower() for l in reference2.readlines() ]

answers.close()
reference1.close()
reference2.close()

os.remove("tmp1")
os.remove("tmp2")

print "\nFirst accuracy:   ", compare(zip(ref1,ans))
print "Second accuracy:  ", compare(zip(ref2,ans))