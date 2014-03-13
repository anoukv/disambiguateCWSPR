# hello

import sys

file_name_answers = sys.argv[1]
file_name_reference = sys.argv[2]

answers = open(file_name_answers, 'rb')
reference = open(file_name_reference, 'rb')

ans = answers.readlines()
ref = reference.readlines()

together = zip(ans, ref)

correct = 0
for i in together:
	answer = i[0]
	realAnswer = i[1].split(' ')[1]
	# print answer, realAnswer
	if answer == realAnswer:
		correct += 1

accuracy = correct / float(len(together)) * 100
print accuracy
