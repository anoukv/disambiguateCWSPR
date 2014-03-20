import os, glob

questionList = glob.glob("../SemVal/Testing/Phase1Questions/*.txt")
answerList = glob.glob("../SemVal/Testing/Phase1Answers/*.txt")


if(len(questionList) == len(answerList)):
  for i in range(len(questionList)):
    for j in range(len(answerList)):
      if(questionList[i][questionList[i].rfind('/') + 1:] == answerList[j][answerList[j].rfind('/') + 1:].replace('Answers','Questions')):
        print questionList[i], answerList[j]
        os.system("pypy semEvalQA.py ../wordvectors/vectors80.broadcast " + questionList[i] + " " + answerList[j])


