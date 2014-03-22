import sys, os, glob

def add_hyphens(filename):
	f = open(filename, 'r')
	content = filter(lambda x : ":" in x and not " " in x, f.readlines())
	f.close()
	c = []
	change = True
	for line in content:
		if '"' not in line:
			change = True
			c.append( '"' + line.replace("\n","") + '"\n')
		else:
			c.append(line)
	if change:
		f = open(filename, 'w')
		f.write("".join(c))
		f.close()



if __name__ == "__main__":
	if not len(sys.argv) == 2:
		print "Call me as:"
		print "python build_result_file.py <wordvectors>"
		sys.exit()

	questionList = glob.glob("../../SemVal/Testing/Phase1Questions/*.txt")
	answerList = glob.glob("../../SemVal/Testing/Phase1Answers/*.txt")

	vector_filename = sys.argv[1]

	for i in xrange(len(questionList)):
		for j in xrange(len(answerList)):
			if(questionList[i][questionList[i].rfind('/') + 1:] == answerList[j][answerList[j].rfind('/') + 1:].replace('Answers','Questions')):
				print questionList[i], answerList[j]

				add_hyphens(questionList[i])
				add_hyphens(answerList[j])

				# Produce answers:
				os.system("pypy semEvalQA.py " + vector_filename + " " + questionList[i] + " " + answerList[j] + " tmp_files/qa_answers")

				# Produce spearman score
				os.system("./maxdiff_to_scale.pl " + answerList[j] + "  tmp_files/tmp.answers" )
				os.system("./score_scale.pl tmp_files/tmp.answers tmp_files/qa_answers result_files/spearman.score" )
				# os.system("rm tmp_files/tmp.answers")

				# Produce maxdiff
				# os.system("./scale_to_maxdiff.pl " + questionList[i] + " tmp_files/qa_answers tmp_files/tmp.answers")
				# os.system("./score_maxdiff.pl " + answerList[j] + " tmp_files/tmp.answers result_files/maxdiff.score")
				# os.system("rm tmp_files/tmp.answers")

				# os.system("rm tmp_files/qa_answers")

				print "Exiting.."
				sys.exit()
