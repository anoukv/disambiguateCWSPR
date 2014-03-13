import sys

# to split the file of a b c d to a file quesions_extended with a b c and answers_extended with d
file_name = sys.argv[1]

file = open(file_name, 'rb')
questions = open('questions_extended', 'w')
answers = open('answers_extended', 'w')

for line in file:
	words = line.split(' ')
	if words[0] != ":":
		questions.write(words[0] + " " + words[1] + " " + words[2] + "\n")
		answers.write(words[3])

print "Done"

