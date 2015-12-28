
'''                                                                                                                 
Find example sentences for any word
'''
import re
import glob
from progressbar import ProgressBar
import os

class Sentence(object):
        completed = 0

        def __init__(self):
		# variables- instantiated
                Sentence.completed = 0
                self.tagOptions = 0
                
        def getFiles(self, path="books"):
                self.fileList = glob.glob(os.path.join(path, '*.txt'))
                self.numberOfFiles = len(self.fileList)

        def displayFiles(self):
                for filename in self.fileList:
                        print filename,

        def basicProgressBarTemplate(self):
                # just a template to remember how to use progressbar
                pb = ProgressBar(10)
                pb.start()
                for i in range(10):
                        pb.update(i + 1)
                        for x in xrange(1000): b = 1 + 2

	def getSentences(self, file='austen.txt'):
		self.text = open(file).read()
                self.textWithoutJunk = re.sub('\'\"','', self.text)
		self.textWithoutJunk = re.sub('[^A-Za-z\. ]+',' ',self.textWithoutJunk)
                self.textWithoutJunk = re.sub(' +', ' ', self.textWithoutJunk)
		self.sentences = self.textWithoutJunk.split(".")

        def setWebPage(self, page = "http://google.com.au"):
		# just keep this as an example of creating default values
                self.page = page

        def universalBar(self, n):
                self.progress = ProgressBar(n)
                self.progress.start()

        def testUniversalBar(self):
                n = 10
                self.universalBar(n)
                for i in range(n):
                        self.progress.update(i + 1)
                        for x in xrange(1000): b = 1 + 2 # do something

        def bookTemplate(self):
                # a simple template for analyzing every word, in every sentence, in every n of books
                sentenceCounter = 0
                self.getFiles("booksSmall/")
                for filename in self.fileList:
                        self.getSentences(filename)
                        for sentence in self.sentences:
                                sentenceCounter = sentenceCounter + 1
                                words = sentence.split()
                                for word in words:
                                        # analyze each word
                                        print word,
                                print
                print "" + str(sentenceCounter) + " sentences analyzed"

	def findSentence(self, complexWord, folder="booksKindle"):
                # a simple template for analyzing every word, in every sentence, in every n of books
                self.getFiles(folder)
                for filename in self.fileList:
                        self.getSentences(filename)
                        for sentence in self.sentences:
				breakIt = False
                                words = sentence.split()
                                for word in words:
					if breakIt: break
					if word.lower() == complexWord.lower():
						print sentence;print; breakIt = True 

                                        
def main():
        #print "analyzing books..."
	go = Sentence()
	#wordToLookUp = raw_input("enter word: ")
	#go.findSentence("farther", "booksKindle")

if __name__ == '__main__':main()
