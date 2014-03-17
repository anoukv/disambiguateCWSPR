import pickle

coc = pickle.load(open('clustering/coc.pickle', 'rb'))

print coc['better'].keys()