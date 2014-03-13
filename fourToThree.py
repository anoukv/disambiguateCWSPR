import sys

file_name = sys.argv[1]

file = open(file_name, 'rb')
questions = open('questions_extended', 'w')
answers = open('answers_extended', 'w')

for line in file:
	words = line.split(' ')
	if words[0] != ":":
		# print "Question: ", words[0], words[1], words[2], " Answer: ", words[3]
		questions.write(words[0] + " " + words[1] + " " + words[2] + "\n")
		answers.write(words[3])

print "Done"

