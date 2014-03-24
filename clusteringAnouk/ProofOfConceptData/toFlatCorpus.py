# transforms a corpus to a one line corpus without punctuation, numbers and everything lowercased

import string, sys

if len(sys.argv) < 3:
 		print "Usage: python toFlatCorpus.py input.txt output.txt"
 		sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]
inpt = open(input_file, 'r')

txt = []
# This is the punctuation
exclude = set(string.punctuation)

for elem in inpt:
	y = elem.lower().replace("\n", "").replace("[", " ").replace("]", " ").split(" ")
	for em in y:
		for punct in exclude:
			if punct in em:
				em = em.replace(punct, "")
		txt.append(em + " ")

inpt.close()

outpt = open(output_file, 'w')

outpt.write("".join(txt))

print "DONE!"
