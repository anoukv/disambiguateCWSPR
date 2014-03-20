import sys

def stats(inpt):



if __name__ == "__main__":
	if not len(sys.argv) == 2:
		print "Call me as:"
		print "pypy stats.py data_file"

	def read_file(filename):
		f = open(filename, 'r')
	 	inpt = filter(lambda x : not x == "", f.readline().replace("\n", "").split(" "))
	 	f.close()
	 	return inpt

	stats(read_file(sys.argv[1]))


