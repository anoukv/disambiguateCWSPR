# Anouks statistics
# For a cleaner and better estimation of... things
import shelve
from collections import defaultdict

voc = shelve.open('../coc.small_voc')

# We want to know: 
print
# - how many words are there anyway?
n = sum(voc.values())
print "Number of words: ", n

# - how many UNIQUE words are there?
u = len(voc.keys())
print "Number of unique words: ", u
print

# - top 25 most occuring words
vocTups = voc.items()
sortedVocTups = sorted(vocTups, key = lambda x: x[1], reverse = True)

for i in range(25):
	print i+1, sortedVocTups[i]
print

# - How many words do we loose when we throw out percentages of the data?
percentages = [1/float(2), 1/float(3), 1/float(4), 1/float(5), 1/float(6)]

for per in percentages:
	remove = 0
	for i in range(int(u * per)):
		remove += sortedVocTups[i][1]
	print per, "% of unique words = ", remove * 100 / float(n), " % of all words"
print


# - (frequency of word, how many words) - I really don't know how to call this
# - how many unique frequencies are there? What are the words associated with them?
frequencyCounts = defaultdict(int)
frequencyWord = defaultdict(list)

for word in voc:
	frequencyCounts[voc[word]] += 1
	frequencyWord[voc[word]].append(word)

wordsToCut = []

remove = 0
for freq in frequencyCounts:
	if frequencyCounts[freq] == 1:
		wordsToCut.append(frequencyWord[freq][0])
		remove += freq
print "By removing the ", len(wordsToCut) * 100 / float(u), "% words that have a unique frequency, we would remove ", remove * 100 / float(n), "% of our words..."
print wordsToCut
print

voc.close()