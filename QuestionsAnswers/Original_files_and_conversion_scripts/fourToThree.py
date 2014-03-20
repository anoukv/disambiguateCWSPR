import sys

# to split the file of a b c d to a file quesions_extended with a b c and answers_extended with Done
file_name = sys.argv[1]

file = open(file_name, 'rb')

questions = None
answers = None

for line in file:
	words = line.split(' ')
	if words[0] != ":":
		questions.write(words[0].lower() + " " + words[1].lower() + " " + words[2].lower() + "\n")
		answers.write(words[3].lower())
	else:
		if questions != None and answers != None: 
			questions.close()
			answers.close()
		
		questions = open(words[1].replace("\n", "") + ".questions", 'w')
		answers = open(words[1].replace("\n", "")  + ".answers", 'w')
		
		print words

questions.close()
answers.close()
print "Done"
