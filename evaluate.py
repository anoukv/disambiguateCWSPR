import sys

# Get the answers and answer reference (i.e real answers) file names
file_name_answers = sys.argv[1]
file_name_reference = sys.argv[2]

answers = open(file_name_answers, 'rb')
reference = open(file_name_reference, 'rb')

ans = answers.readlines()
ref = reference.readlines()

# Make tuples of given answers and reference answers
together = zip(ans, ref)

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
accuracy = correct / float(len(together)) * 100

# Report overall accuracy
print "Overall correct: ", accuracy, "%"
