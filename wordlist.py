

# In-memory constants
IGNORESET = set("""
ness ally ting

ab ac ad ah al aw ax ay bb br ca cc cd cl co cr cs ct db dc dp dx eh el en es et ga ha
hp hr ic id ii iv kb kl lf lh ll lr mb mc md mf mg mn mo mw na ne nj nm nu ob od os ox
oz pa pf pl pm po pp rd rf rh rn sa sc sd se sh si sn sp sr ss st th ti tm tv tx un ut
va vc vs vt wa wk xx ye yr zn

""".split())

def loadwordlist(filename = 'wordsEN.txt'):
	"""Retrieve a wordlist from a file location"""
	words = [word.lower().strip() for word in open('wordsEN.txt','r')] 
	words = [word for word in words if words not in IGNORESET]
	return [w for w in words if w]



WORDLIST = loadwordlist()


	