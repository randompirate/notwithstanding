import multiprocessing as mp
import sys
import time

#Wordlist module for constant WORDLIST, in-memory
import wordlist as wl


def memo(func):
	"""Decorator for function memoisation"""
	# TODO: Check memoisation sync across threads.

	#Dictionary of called arguments already encountered
	argdict = {}

	def retfun(*args):
		arghash = str(args)
		if arghash not in argdict:
			#If the calling argument is not in the dictionary:
			#	Calculate it and add to the dicionary
			res = func(*args)		
			argdict[arghash] = res

		#Return from the dictinoary
		return argdict[arghash]
	return retfun


def getstarterwords(word):
	"""Return all the words in wl.WORDLIST with which the given word starts.
		For example: 'information' -> 'in', 'info', 'inform'
	"""
	return [w for w in wl.WORDLIST if word[0:len(w)]==w]# and len(w)<len(word)]


def splitword(word, start):
	"""Split a starting string of from a word, return in tuple-form"""
	return [start, word[len(start):]]

@memo 	#Memoisation decorator
def singlesplits(word):
	"""Find all single splits of a word
			Single splits are valid words with which the given word starts
			This function is memoised
	"""
	#All starterwords: Words in the dictionary with which this word begins
	starterwords = getstarterwords(word)
	return [splitword(word, sw) for sw in starterwords]			#Return in tuple form


def compoundgenerator(words):
	"""Generator
		Split a long word into valid subwords.
	 	For example 'without' -> 'with', 'out'
	 				'inasmuch' -> 'in', 'as', 'much'
	"""
	*firstwords, lastword = words #Unpack the last element: [a, b, c, d, e] > [a, b, c, d], e

	#Find all splits for the lastword
	splits = singlesplits(lastword)

	#For each possible split, recursively perform compoundgenerator on the remaining part
	for split in splits:
		yield from compoundgenerator(firstwords + split)

	#If the remainder (after all possible splits) is a word, return it.
	if lastword in wl.WORDLIST:
		yield words


def compoundlist(word):
	"""Iterate a compoundgenerator and return the results as a list in-memory"""
	return list(compoundgenerator([word]))


def list2dict(lst):
	"""Returns a dictionary for a list of results from compoundgenerator."""
	return dict([[r[-1][0], r[0:-1]] for r in lst if r[0:-1]])


#---------------#
# Main entrance #
#---------------#
def main(args):

	"""Main entrance"""

	starttime = time.time()

	#Run the iterFunction in parallel.
	pool = mp.Pool(processes=4)
	results = pool.imap_unordered(compoundlist, wl.WORDLIST)

	# Transform the results into a dictionary. The stream generators turn into in-memory datatypes now.
	resdict = list2dict(results) 

	#Pretty print
	open('output.txt','w').write('\n'.join([k + ' : ' + ' // '.join([' '.join(itm) for itm in itms]) for k, itms in resdict.items()]))

	print('\nTime spent: ', time.time() - starttime )



if __name__ == '__main__':
	if sys.argv:
		main(sys.argv)
	else:
		main(None)

	