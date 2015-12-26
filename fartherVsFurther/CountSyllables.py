
'''                                                                                                                 
Count Syllables v1.0

A simple class to count syllables using a dictionary method

This class will attempt to calculate syllables of words not found in dictionary
'''

class CountSyllables(object):

        def __init__(self):
		# variables- instantiated
                self.prepareData()

        def generateDict(self):
                # converts a pronunciation dictionary into a syllable count dictionary
                fileName = open("dict.txt", 'r')
                print 'openning file...'
                data = fileName.read()
                fileName.close()

                print 'splitting up data by entries...'
                words = data.split("\n")

                outputFile = open("syllables.txt", 'w')
                for entry in words:
                        entry = entry.split("  ")
                        word = entry[0]
                        pronunciation = entry[1]
                        sections = pronunciation.split(" ")
                        count = 0
                        for section in sections:
                                if self.isVowel(section):
                                        count+=1
                        if count == 0: count = 1
                        
                        outputFile.write(word.lower() + ',' + str(count) + '\n')
                outputFile.close()


        def isVowel(self, word):
                # a simple function to find whether a word contains a vowel or not
                word = word.lower()
                if 'a' in word or 'e' in word or 'i' in word or 'o' in word or 'u' in word:
                        return True
                else: return False
        
        def prepareData(self):
                fileName = open('SyllableCounter/syllables.txt', 'r')
                self.dict = {}                
                data = fileName.read()
                fileName.close()
                lines = data.split('\n')
                for line in lines:
                        entry = line.split(',')
                        
                        if len(entry[0]) < 1: continue
                        if entry[0] in self.dict: continue
                        else: self.dict[entry[0]] = entry[1]
                

        def count(self, word):
                if word in self.dict: return self.dict[word]
                syllCount = 0
                for letter in word:
                        if self.isVowel(letter): syllCount += 1
                if syllCount < 1: return 1
                else: return syllCount
                        
        
def main():
	test = CountSyllables()
	print test.count('elephant')

if __name__ == '__main__':main()
