import os, glob

questionList = glob.glob("SemVal/Testing/Phase1Questions/*.txt")
answerList = glob.glob("SemVal/Testing/Phase1Answers/*.txt")

#print len(questionList)
#print len(answerList)
#print "hy!" 
if(len(questionList) == len(answerList)):
    for i in range(len(questionList)):
	#print "q de i:" + questionList[i]
	#print "find result:" +  questionList[i][questionList[i].rfind('/') + 1:]
	for j in range(len(answerList)):
        	if(questionList[i][questionList[i].rfind('/') + 1:] == answerList[j][answerList[j].rfind('/') + 1:].replace('Answers','Questions')):
                   #print questionList[i][questionList[i].rfind('\\') + 1:]
                   #print "name of generated file is: " + questionList[i][questionList[i].rfind('\\') + 1:].replace('Questions', 'Similarity')
                   print "results file name: " + " Results/" + questionList[i][questionList[i].rfind('/') + 1:].replace('Questions', 'Similarity').replace(".txt", "")
                   #print "executed command: " + "./SemanticRelations word_projections-80.txt " + questionList[i] + " " + answerList[i] + " Results/" + questionList[i][questionList[i].rfind('\\') + 1:].replace('Questions', 'Similarity').replace(".txt", "")
                   
                   os.system("./SemanticRelations word_projections-80.txt " + questionList[i] + " " + answerList[j] + " Results/" + questionList[i][questionList[i].rfind('/') + 1:].replace('Questions', 'Similarity').replace(".txt", ""))
