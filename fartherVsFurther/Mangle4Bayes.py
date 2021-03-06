
'''                                                                                                                 
Farther vs Further
Fri Dec 18 11:07:54 AEDT 2015

A simple grammar checker for this single rule.

Wed Dec 23 10:01:10 AEDT 2015
This version will include higher order functions. 
'''
#import nltk
from textblob import TextBlob
import csv 
from Sentence import Sentence
from CountSyllables import CountSyllables


#TODO get rid of lower cases
#TODO add more features.

class TagIt(object):
	"""
	Sun Dec 20 07:43:55 AEDT 2015
	Extract tags from left and right of a key in a sentence.
	"""

	def __init__(self):
		pass

	def tagSentence(self, sentence):
		"""Turn a sentence into an array of (words, tags)"""
		return TextBlob(sentence).tags

	def loadCSV(self, fileName="fartherVsFurther.csv"):
		"""Load training set"""
		f = open(fileName, "rb")
		reader = csv.reader(f)
		newData = []
		for line in reader:
			newData += [line]
		f.close()
		return newData


	def addTags(self, sentence=[("further", "JJ"), ("Elephant", "NNP")], factors=5):	
		""""
		Buffer a list of (word, tag) with NAs of any factor
		[(x1,y1), (x2,y2)], 1 ----> [(na,na), (x1,y1), (x2,y2), (na,na)]
		"""
		newVars = []
		for i in range(factors):
			newVars.append(("na", "na"))
		sentence += newVars
		newVars += sentence
		return newVars

	def extractTags(self, sentence=[("NA","NA"),("run","VB"),("further", "JJ"), ("Elephant", "NNP"),("Hotel","NNP"),("NA","NA")], keys=["further", "farther"], factors=2):
		"""Get tags that surround a key """
		count = 0
		listOfTags = []
		for i in sentence:
			# Wait till you find one of the keys
			if i[0] in keys:
				iterNum = 0
				#Get words before key
				for z in range(factors):

					listOfTags.append(sentence[(count - factors) + iterNum][1])
					iterNum += 1
				iterNum = 1
				#Get words after key
				for z in range(factors):

					listOfTags.append(sentence[count + iterNum][1])
					iterNum += 1
				return listOfTags	
			count += 1
		return listOfTags

	def processWords(self, sentence="I can not take it much farther.", keys=["further", "farther"], factors=5):
		"""Turns a sentence into a list of words with buffer of N factors"""
		#Tag sentence
		X = self.tagSentence(sentence)
		#Add NAs to front and back
		X = self.addTags(X, factors)
		#Reduce to a list of tags
		return self.extractTags(X, keys, factors)

class SyllableIt(TagIt):
	"""
	Extracts syllable counts from either side of a key word.
	"""
	def __init__(self):
		self.syllable = CountSyllables()

	def addTags(self, sentence=["here", "is", "a", "word"], factors=5):	
		""""
		Buffer a list of (word, tag) with NAs of any factor
		[(x1,y1), (x2,y2)], 1 ----> [(na,na), (x1,y1), (x2,y2), (na,na)]
		"""
		newVars = []
		for i in range(factors):
			newVars += ["na"]
		sentence += newVars
		newVars += sentence
		return newVars

	def extractTags(self, sentence, keys, factors):
		"""
		Return the words around a key
		["na", "I", "run", "na"], "run", 1 -----> ["I", "run", "na"]
		"""
		listOfTags = []
		count = 0
		for i in sentence:
			if i in keys:
				iterNum = 0
				#Get words before key
				for z in range(factors):
					listOfTags += [str(self.getSyllable(sentence[(count - factors) + iterNum]))]
					iterNum += 1
				iterNum = 1
				for z in range(factors):
					listOfTags += [str(self.getSyllable(sentence[count + iterNum]))]
					iterNum += 1
				return listOfTags
			count += 1
		return listOfTags

	def processWords(self, sentence="I can not take it much farther.", keys=["further", "farther"], factors=5):
		"""Turns a sentence into a list of syllables with buffer of N factors"""
		#Tag sentence
		X = sentence.lower().split(" ")
		X = [x[0] for x in self.tagSentence(sentence)]
		#Add NAs to front and back
		X = self.addTags(X, factors)
		#Reduce to a list of tags
		return self.extractTags(X, keys, factors)

	def getSyllable(self, word):
		return self.syllable.count(word)


class WordIt(TagIt):
	"""
	Wed Dec 23 11:49:07 AEDT 2015
	Child of TagIt()
	This exracts words from left and right of a key word in a sentence.
	"""

	def __init__(self):
		pass
	
	def addTags(self, sentence=["here", "is", "a", "word"], factors=5):	
		""""
		Buffer a list of (word, tag) with NAs of any factor
		[(x1,y1), (x2,y2)], 1 ----> [(na,na), (x1,y1), (x2,y2), (na,na)]
		"""
		newVars = []
		for i in range(factors):
			newVars += ["na"]
		sentence += newVars
		newVars += sentence
		return newVars

	def extractTags(self, sentence, keys, factors):
		"""
		Return the words around a key
		["na", "I", "run", "na"], "run", 1 -----> ["I", "run", "na"]
		"""
		listOfTags = []
		count = 0
		for i in sentence:
			if i in keys:
				iterNum = 0
				#Get words before key
				for z in range(factors):
					listOfTags += [sentence[(count - factors) + iterNum]]
					iterNum += 1
				iterNum = 1
				for z in range(factors):
					listOfTags += [sentence[count + iterNum]]
					iterNum += 1
				return listOfTags
			count += 1
		return listOfTags

	def processWords(self, sentence="I can not take it much farther.", keys=["further", "farther"], factors=5):
		"""Turns a sentence into a list of words with buffer of N factors"""
		#Tag sentence
		X = sentence.lower().split(" ")
		X = [x[0] for x in self.tagSentence(sentence)]
		#Add NAs to front and back
		X = self.addTags(X, factors)
		#Reduce to a list of tags
		return self.extractTags(X, keys, factors)

	


class CheckGrammar(object):
	"""
	Calculate Naive Bayes on any sample provided.
	This class reads Bayes data and calculates the algorithm based on this data.
	"""
	def __init__(self):
		self.mangle = WordIt()

	def quickLoop(self, fileName, keys, factors, class1, class2):
		while (True):
			x = raw_input(">> ")
			z,y = self.testSentence(x, fileName, keys, factors, class1, class2)
			print z,y

	def testFile(self, fileName, fileName2, keys, factors, class1, class2,class1Focus=True):
		X = open(fileName).read().lower().split('\n')
		class1Tally = 0.0
		class2Tally = 0.0
		for z in X:
			if len(z) > 2:
				b, c = self.testSentence(z, fileName2, keys, factors, class1, class2)
				if b > c: 
					class1Tally += 1
					if not(class1Focus): print z
					#print 1,
				else: 
					class2Tally += 1
					if class1Focus: print z
					#print 0,

		print "True: " + str((class1Tally / (class1Tally + class2Tally)) * 100)
		print "False: " + str((class2Tally / (class1Tally + class2Tally)) * 100)
		

	def testSentence(self, sentence="You could not be further from the truth.", fileName="finalFurther.csv", keys = ["further", "farther"], factors = 2, class1=3192.0, class2=1078.0):
		sentence = sentence.lower()
		# Get the tag list of surrounding words
		X = self.mangle.processWords(sentence, keys, factors)
		#print sentence, X

		# Load dataset with probabilities
		Y = self.mangle.loadCSV(fileName)
		trueCond = 1; falseCond = 1
		# Calculate class probabilities
		trueCond += class1 / (class1 + class2)
		falseCond += class2 / (class1 + class2)

		# Loop over tags
		count = 1
		for z in X:
			# Find tag in dataset
			for i in Y:
				if z == i[0]:
					#print float(i[count]), float(i[count+1])
					trueCond *= float(i[count])
					falseCond *= float(i[count+1])
			count += 2

		return (trueCond / (trueCond + falseCond)), (falseCond / (trueCond + falseCond))

class ComputeBayes(object):
	"""
	Create a CSV spreadsheet of all the Bayes data.
	"""
	#TODO create a dict of dicts to allow for more features to be dynamically added.
	def __init__(self):
		# load MangleData class
		self.mangle = MangleData()
		self.class1Total = 0
		self.class2Total = 0

	def setupDicts(self, factors = 2, fileName = "further.csv", fileName2 = "farther.csv"):
		"""Setup feature dicts for any number of features """
		# Class 1 dict
		self.wordsUsed = {}
		self.features = {}
		self.featuresClass2 = {}
		self.factors = factors
		factors *= 2
		
		# get all words used from files
		X = self.mangle.loadCSV(fileName)
		Y = self.mangle.loadCSV(fileName2)
		for i in X: 
			for z in i:
				#self.class1Total += 1.0
				if z in self.wordsUsed:
					pass
				else:
					self.wordsUsed[z] = 1.0
		for i in Y:
			for z in i:
				#self.class2Total += 1.0
				if z in self.wordsUsed:
					pass
				else:
					self.wordsUsed[z] = 1.0	

		for i in range(factors):
			self.features[i] = {k:v for k,v in self.wordsUsed.items()}
		for i in range(factors):
			self.featuresClass2[i] = {k:v for k,v in self.wordsUsed.items()}
	
		# Create ordered list of items
		self.wordsUsedList = [k for k,v in self.wordsUsed.items()]


	def clearDict(self):
		"""Clears the one dict to rule them all."""
		self.features.clear()

	def countAllFeatures(self, fileName = "farther.csv"):
		"""Create a dict of feature counts"""
		self.class1Name = fileName
		X = self.mangle.loadCSV(fileName)
		# rows - intances
		for i in X:
			count = 0
			# columns - features
			for z in i:
				# Add count for each item according to column and row
				if count < (len(i) - 1): 
					self.features[count][z] += 1
				count += 1

	def countAllFeaturesClass2(self, fileName = "further.csv"):
		"""Create a dict of feature counts"""
		self.class2Name = fileName
		X = self.mangle.loadCSV(fileName)
		# rows - intances
		for i in X:
			count = 0
			# columns - features
			for z in i:
				# Add count for each item according to column and row
				if count < (len(i) - 1): 
					self.featuresClass2[count][z] += 1
				count += 1

	def intersect(self, X, Y):
		"""
		Join two lists in an overlaping fashion 
		[x1, x2, x3], [y1, y2, y3] ----> [x1, y1, x2, y2, x3, y3]
		"""
		result = [None] * (len (X) + len(Y))
		result[::2] = X
		result[1::2] = Y
		return result

	def createSheet(self):
		"""Create spreadsheet of data for (features * tags)"""
		# Create header string
		# e.g. "tag,f1_c1,f1_c2,f2_c1,f2_c2,f3_c1,f3_c2,f4_c1,f4_c2"
		A = ["f" + str(x + 1) + "_c1" for x in range(self.factors * 2)]
		B = ["f" + str(x + 1) + "_c2" for x in range(self.factors * 2)]
		C = ','.join(["tags"] + self.intersect(A, B))
		print C
		self.class1Total = sum([self.features[0][x] for x in self.getTagList()])
		self.class2Total = sum([self.featuresClass2[0][x] for x in self.getTagList()])
		# Loop over every tag in order
		for i in self.getTagList():
			# Get list of features for each class for each tag
			X = [str(self.features[x][i] / self.class1Total) for x in range(self.factors * 2)]
			Y = [str(self.featuresClass2[x][i] / self.class2Total) for x in range(self.factors * 2)]
			Z = ','.join([i] + self.intersect(X, Y))
			print Z

		# Print totals for data
		print "class_1," + str(self.class1Total)
		print "class_2," + str(self.class2Total)

	def getTagList(self):
		return self.wordsUsedList
			
	def printOutTags(self):
		"""Make printable version of tag names"""
		for i in self.feature1:
			print "'" + i + "',",	

class ComputeTags(ComputeBayes):
	"""
	Extension of Compute Bayes, to specifically compute tag counts.
	"""

	def __init__(self):
		self.mangle = WordIt()
		self.feature1 = {"CC": 1.0, "CD": 1.0, "na": 1.0, "DT": 1.0, "EX": 1.0, "FW": 1.0, "IN": 1.0, "JJ": 1.0, "JJR": 1.0, "JJS": 1.0, "LS": 1.0, "MD": 1.0, "NN": 1.0, "NNP": 1.0, "NNPS": 1.0, "NNS": 1.0, "PDT": 1.0, "POS": 1.0, "PRP": 1.0, "PRP$": 1.0, "RB": 1.0, "RBR": 1.0, "RBS": 1.0, "RP": 1.0, "SYM": 1.0, "TO": 1.0, "UH": 1.0, "VB": 1.0, "VBD": 1.0, "VBG": 1.0, "VBN": 1.0, "VBP": 1.0, "VBZ": 1.0, "WDT": 1.0, "WP": 1.0, "WP$": 1.0, "WRB": 1.0, "total": 37.0}

	def setupDicts(self, factors = 2):
		"""Setup feature dicts for any number of features """
		# Class 1 dict
		self.features = {}

		self.factors = factors
		factors *= 2
		for i in range(factors):
			self.features[i] = {k:v for k,v in self.feature1.items()}
				# Class 2 dict
		self.featuresClass2 = {}
		#factors *= 2
		for i in range(factors):
			self.featuresClass2[i] = {k:v for k,v in self.feature1.items()}
	
		self.wordsUsedList = [k for k,v in self.feature1.items()]

	def getTagList(self):
		#TODO Sort tags so that they're easier to view in spreadsheet
		return ['WRB', 'PRP$', 'VBG', 'FW', 'CC', 'PDT', 'RBS', 'PRP', 'CD', 'WP$', 'VBP', 'VBN', 'EX', 'JJ', 'IN', 'WP', 'VBZ', 'DT', 'MD', 'NNPS', 'RP', 'NN', 'na', 'RBR', 'VBD', 'JJS', 'JJR', 'SYM', 'VB', 'TO', 'UH', 'LS', 'RB', 'WDT', 'NNS', 'POS', 'NNP']

class MangleData(object):
	"""
	Convert a raw corpus into a dataset.
	"""  
#TODO I've created better methods to do some of these tasks in the new class called WordMangle()
  
        def __init__(self):
		# use a dictionary to store tags e.g. {"vvb": 1.0, "jj": 2}
		#self.mangle = TagIt()
		pass

	#def getListOfTags(self):
		#"""Use this to get a list of all nltk tags printed 2 screen."""
		#print nltk.help.upenn_tagset()

        def tagSentence(self, sentence):
		"""Turn a sentence into an array of (words, tags)"""
		return TextBlob(sentence).tags

	def loadCSV(self, fileName="fartherVsFurther.csv"):
		"""Load training set"""
		f = open(fileName, "rb")
		reader = csv.reader(f)
		newData = []
		for line in reader:
			newData += [line]

		f.close()
		return newData

	def trainLargeCorpus(self, process, fileName="sentenceExamples/furtherKindleSmall.txt", factors = 2, key = "further"):
		"""Convert a training set to an array of values."""
		X = open(fileName, 'r').read().lower().split("\n")			
		count = 0
		for i in X:
			if len(i) < 2: 
				#count += 1
				continue
			# X[count] = self.mangle.processWords4Words(i, [key], factors)
			#X[count] = self.mangle.processWords(i, [key], factors)
			X[count] = process(i, [key], factors)
			print ','.join(X[count] + [key])
			count += 1

def main():

	"""Step 3: Looping over examples"""
	loopTest = CheckGrammar()
	loopTest.quickLoop("sheet.csv", ["further", "farther"], 2, 118662, 56870)
	#loopTest.testFile("bookExtract/furtherKindleSmall.txt", "model3/sheet.csv", ["further", "farther"], 2, 59829.0, 30171.0, True)

	"""Step 2: Compute Bayes"""
	"""A) Tags """
	#computeBayes = ComputeTags()
	#computeBayes.setupDicts(2)

	#computeBayes = ComputeBayes()
	#computeBayes.setupDicts(2, "furtherTag.txt", "fartherTag.txt")
	#print '@attribute fourleft {' + ','.join(computeBayes.getTagList()) + '}'


	#computeBayes.countAllFeatures("furtherTag.txt")
	#computeBayes.countAllFeaturesClass2("fartherTag.txt")
	#computeBayes.createSheet()
	
	"""Step 1: Mangle Data"""
	#mangleData = MangleData()
	#mangleData2 = MangleData()
	#syllableIt = SyllableIt()
	#wordIt = WordIt()
	#wordIt2 = WordIt()
	#tagIt = TagIt()

	# Tag Corpus
	#mangleData.trainLargeCorpus(tagIt.processWords, "bookExtract/fartherKindleSmall.txt", 2, "farther", )

	# Word Corpus
	#mangleData.trainLargeCorpus(wordIt.processWords, "farther.txt", 2, "farther")
	#mangleData2.trainLargeCorpus(wordIt2.processWords, "fartherText.txt", 2, "farther")

	# Syllable Corpus
	#mangleData.trainLargeCorpus(syllableIt.processWords, "bookExtract/furtherKindleSmall.txt", 15, "further")
	#mangleData.trainLargeCorpus(syllableIt.processWords, "bookExtract/fartherKindleSmall.txt", 15, "farther")

	"""Step 0: Get Data"""
	#getSentences = Sentence()
	#getSentences.findSentence("farther", "booksKindle")


if __name__ == '__main__':main()
