import pickle

coc = pickle.load(open('clustering/coc.pickle', 'rb'))

def makeCustomDic(keysToKeep, dic):
	keys = dic.keys()
	for key in keys:
		if key not in keysToKeep:
			dic.pop(key)


