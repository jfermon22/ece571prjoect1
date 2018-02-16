import itertools, re
from FrequencyAnalyzer import FrequencyAnalyzer
from HackerReturnValue import HackerReturnValue
import operator

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False  # if set to True, program doesn't print attempts
NUM_MOST_FREQ_LETTERS = 4  # attempts this many letters per subkey
MAX_KEY_LENGTH = 16  # will not attempt keys longer than this
NONLETTERS_PATTERN = re.compile('[^A-Z]')

class VigenereHacker:
    def __init__(self, rawText):
        self.rawText = rawText.upper()

    def findRepeatSequencesSpacings(self):
        # Goes through the message and finds any 3 to 5 letter sequences
        # that are repeated. Returns a dict with the keys of the sequence and
        # values of a list of spacings (num of letters between the repeats).
    
        # Use a regular expression to remove non-letters from the message.
        message = NONLETTERS_PATTERN.sub('', self.rawText)
    
        # Compile a list of seqLen-letter sequences found in the message.
        seqSpacings = {}  # keys are sequences, values are list of int spacings
        for seqLen in range(3, 6):
            for seqStart in range(len(self.rawText) - seqLen):
                # Determine what the sequence is, and store it in seq
                seq = self.rawText[seqStart:seqStart + seqLen]
    
                # Look for this sequence in the rest of the message
                for i in range(seqStart + seqLen, len(self.rawText) - seqLen):
                    if self.rawText[i:i + seqLen] == seq:
                        # Found a repeated sequence.
                        if seq not in seqSpacings:
                            seqSpacings[seq] = []  # initialize blank list
    
                        # Append the spacing distance between the repeated
                        # sequence and the original sequence.
                        seqSpacings[seq].append(i - seqStart)
        return seqSpacings

    def getUsefulFactors(self, num):
        # Returns a list of useful factors of num. By "useful" we mean factors
        # less than MAX_KEY_LENGTH + 1. For example, getUsefulFactors(144)
    
        if num < 2:
            return []  # numbers less than 2 have no useful factors
    
        factors = []  # the list of factors found
    
        # When finding factors, you only need to check the integers up to
        # MAX_KEY_LENGTH.
        for i in range(2, MAX_KEY_LENGTH + 1):  # don't test 1
            if num % i == 0:
                factors.append(i)
                factors.append(int(num / i))
        if 1 in factors:
            factors.remove(1)
        return list(set(factors))
    
    def getItemAtIndexOne(self, x):
        return x[1]
    
    def getMostCommonFactors(self, seqFactors):
        # First, get a count of how many times a factor occurs in seqFactors.
        factorCounts = {}  # key is a factor, value is how often if occurs
    
        # seqFactors keys are sequences, values are lists of factors of the
        # spacings. seqFactors has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
        # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
        for seq in seqFactors:
            factorList = seqFactors[seq]
            for factor in factorList:
                if factor not in factorCounts:
                    factorCounts[factor] = 0
                factorCounts[factor] += 1
    
        # Second, put the factor and its count into a tuple, and make a list
        # of these tuples so we can sort them.
        factorsByCount = []
        for factor in factorCounts:
            # exclude factors larger than MAX_KEY_LENGTH
            if factor <= MAX_KEY_LENGTH:
                # factorsByCount is a list of tuples: (factor, factorCount)
                # factorsByCount has a value like: [(3, 497), (2, 487), ...]
                factorsByCount.append((factor, factorCounts[factor]))
    
        # Sort the list by the factor count.
        factorsByCount.sort(key=self.getItemAtIndexOne, reverse=True)
    
        return factorsByCount
    
    def kasiskiTest(self):
        # Find out the sequences of 3 to 5 letters that occur multiple times
        # in the ciphertext. repeatedSeqSpacings has a value like:
        # {'EXG': [192], 'NAF': [339, 972, 633], ... }
        repeatedSeqSpacings = self.findRepeatSequencesSpacings()
    
        # See getMostCommonFactors() for a description of seqFactors.
        seqOccurances = {}
        seqFactors = {}
        for seq in repeatedSeqSpacings:
            seqFactors[seq] = []
    	    # print seq +": "+ str(repeatedSeqSpacings[seq])
        	# print seq + ": " + str(len(repeatedSeqSpacings[seq]))
    	    occurances = len(repeatedSeqSpacings[seq]) + 1
    	    if occurances >= 3:
    	        seqOccurances.update({seq:occurances})
    	   
            for spacing in repeatedSeqSpacings[seq]:
                seqFactors[seq].extend(self.getUsefulFactors(spacing))
            
        # seqOccurancesSorted = sorted(seqOccurances.items(), key=operator.itemgetter(1),reverse=True)
        # print seqOccurancesSorted
    
        # See getMostCommonFactors() for a description of factorsByCount.
        factorsByCount = self.getMostCommonFactors(seqFactors)
        highestOccurance = (factorsByCount[0])[1]
        
        cutOffIndex = 1
        for index in range(1, len(factorsByCount)):
            factorKey, factorCount = factorsByCount[index]
            percentDiff = (float(highestOccurance) - float(factorCount)) / float(highestOccurance) * 100
            # print str(factorKey) + ": " + str(percentDiff)
            # look for a difference of greater than 50 percent. This is a significant
            # drop from the highest value and is likely a good cut off point
            if percentDiff > 50.0:
                cutOffIndex = index
                break
    
        # Now we extract the factor counts from factorsByCount and
        # put them in allLikelyKeyLengths so that they are easier to
        # use later.
        allLikelyKeyLengths = []
        for twoIntTuple in factorsByCount[:cutOffIndex]:
            allLikelyKeyLengths.append(twoIntTuple[0])
        
        allLikelyKeyLengths.sort(reverse=True)
    
        return allLikelyKeyLengths
    
    def getNthSubkeysLetters(self, n, keyLength, message):
        # Returns every Nth letter for each keyLength set of letters in text.
        # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
        #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
        #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
        #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'
    
        # Use a regular expression to remove non-letters from the message.
        message = NONLETTERS_PATTERN.sub('', message)
    
        i = n - 1
        letters = []
        while i < len(message):
            letters.append(message[i])
            i += keyLength
        return ''.join(letters)
    
    def attemptBruteHackWithKeyLength(self, keyLength):

        # allFreqScores is a list of keyLength number of lists.
        # These inner lists are the freqScores lists.
        allFreqScores = []
        for nth in range(1, keyLength + 1):
            nthLetters = self.getNthSubkeysLetters(nth, keyLength, self.rawText)
    
            # freqScores is a list of tuples like:
            # [(<letter>, <Eng. Freq. match score>), ... ]
            # List is sorted by match score. Higher score means better match.
            # See the englishFreqMatchScore() comments in freqAnalysis.py.
            freqScores = []
            for possibleKey in LETTERS:
                decryptedText = self.decrypt(possibleKey, nthLetters)
                # keyAndFreqMatchTuple = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
                freqAnalyzer = FrequencyAnalyzer(decryptedText)
                
                keyAndFreqMatchTuple = (possibleKey, freqAnalyzer.rawFreqMatchOrderToEngish)
                freqScores.append(keyAndFreqMatchTuple)
            # Sort by match score
            freqScores.sort(key=self.getItemAtIndexOne, reverse=True)
    
            allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])
    
        mostLikelyKey = ''
        if not SILENT_MODE:
            for i in range(len(allFreqScores)):
                # use i + 1 so the first letter is not called the "0th" letter
                print('Possible letters for letter %s of the key: ' % (i + 1))
    	        scoreNum = 0
                for freqScore in allFreqScores[i]:
                    print freqScore[0] + ": " + str(freqScore[1])
    		    if scoreNum == 0:
    		        mostLikelyKey += freqScore[0]
    		    scoreNum += 1
                print  # print a newline
    	   
        
        # Try every combination of the most likely letters for each position
        # in the key.
        for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=keyLength):
            # Create a possible key from the letters in allFreqScores
            possibleKey = ''
            for i in range(keyLength):
                possibleKey += allFreqScores[i][indexes[i]][0]
     
            if not SILENT_MODE:
                print('Attempting with key: %s' % (possibleKey))
     
            decryptedText = self.decrypt(possibleKey, self.rawText)
            freqAnalyzer = FrequencyAnalyzer(decryptedText)
            #if detectEnglish.isEnglish(decryptedText):
            avgScore = (freqAnalyzer.englishLetterMatch + freqAnalyzer.englishBigramMatch + freqAnalyzer.englishTrigramMatch + freqAnalyzer.rawFreqMatchOrderToEngish) / 4
            if freqAnalyzer.englishLetterMatch > 90.0 and avgScore > 80.0:
                print 'Possible key found:' + (mostLikelyKey)
                print "Decryption sample: " + decryptedText[:150]
            
            print 'press enter to quit if decryption sample is correct, or C to continue:' 
            response = raw_input('> ').upper()
            if response != 'C':
                return decryptedText
    
        # No English-looking decryption found, so return None.
        return None
    
    def attemptBestGuessHackWithKeyLength(self, keyLength):

        # allFreqScores is a list of keyLength number of lists.
        # These inner lists are the freqScores lists.
        allFreqScores = []
        for nth in range(1, keyLength + 1):
            nthLetters = self.getNthSubkeysLetters(nth, keyLength, self.rawText)
    
            # freqScores is a list of tuples like:
            # [(<letter>, <Eng. Freq. match score>), ... ]
            # List is sorted by match score. Higher score means better match.
            # See the englishFreqMatchScore() comments in freqAnalysis.py.
            freqScores = []
            for possibleKey in LETTERS:
                decryptedText = self.decrypt(possibleKey, nthLetters)
                # keyAndFreqMatchTuple = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
                freqAnalyzer = FrequencyAnalyzer(decryptedText)
                
                keyAndFreqMatchTuple = (possibleKey, freqAnalyzer.rawFreqMatchOrderToEngish)
                freqScores.append(keyAndFreqMatchTuple)
            # Sort by match score
            freqScores.sort(key=self.getItemAtIndexOne, reverse=True)
    
            allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])
    
        mostLikelyKey = ''
        for i in range(len(allFreqScores)):
            mostLikelyKey += ((allFreqScores[i])[0])[0]
            
        print "Most likely key for size " + str(keyLength) + ": " + mostLikelyKey
        # Try most likey key for this size
            
        decryptedText = self.decrypt(mostLikelyKey, self.rawText)
        freqAnalyzer = FrequencyAnalyzer(decryptedText)
        # print "English letter Freq Match Score: " + str(freqAnalyzer.englishLetterMatch)
        # print "English bigram Freq Match Score: " + str(freqAnalyzer.englishBigramMatch)
        # print "English trigram Freq Match Score: " + str(freqAnalyzer.englishTrigramMatch)
        # print "English ETOAI Match Score: " + str(freqAnalyzer.rawFreqMatchOrderToEngish)
        
        avgScore = (freqAnalyzer.englishLetterMatch + freqAnalyzer.englishBigramMatch + freqAnalyzer.englishTrigramMatch + freqAnalyzer.rawFreqMatchOrderToEngish) / 4
        if freqAnalyzer.englishLetterMatch > 90.0 and avgScore > 80.0 :
            print 'Possible key found:' + (mostLikelyKey)
            print "Decryption sample: " + decryptedText[:150]
            
            print('press enter to quit if decryption sample is correct, or C to continue:')
            response = raw_input('> ').upper()
            if response != 'C':
                return decryptedText
    
        # we failed
        return None
    
    def getMostLikelyHack(self,keyLength):
        # allFreqScores is a list of keyLength number of lists.
        # These inner lists are the freqScores lists.
        allFreqScores = []
        for nth in range(1, keyLength + 1):
            nthLetters = self.getNthSubkeysLetters(nth, keyLength, self.rawText)
            freqScores = []
            for possibleKey in LETTERS:
                decryptedText = self.decrypt(possibleKey, nthLetters)
                freqAnalyzer = FrequencyAnalyzer(decryptedText)
                
                keyAndFreqMatchTuple = (possibleKey, freqAnalyzer.rawFreqMatchOrderToEngish)
                freqScores.append(keyAndFreqMatchTuple)
            # Sort by match score
            freqScores.sort(key=self.getItemAtIndexOne, reverse=True)
    
            allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])
    
        mostLikelyKey = ''
        for i in range(len(allFreqScores)):
            mostLikelyKey += ((allFreqScores[i])[0])[0]
            
        decryptedText = self.decrypt(mostLikelyKey, self.rawText)
        freqAnalyzer = FrequencyAnalyzer(decryptedText)
        
        avgScore = (freqAnalyzer.englishLetterMatch + freqAnalyzer.englishBigramMatch + freqAnalyzer.englishTrigramMatch + freqAnalyzer.rawFreqMatchOrderToEngish) / 4
        if freqAnalyzer.englishLetterMatch > 90.0 and avgScore > 80.0:
            percentConfidence = (freqAnalyzer.englishLetterMatch + avgScore) / 2.0
            return HackerReturnValue(mostLikelyKey,decryptedText, percentConfidence)
    
        #failed
        return None
    
    def hack(self):
        # Find key length for kasiski test
        probableKeyLengths = self.kasiskiTest()
        #print('Kasiski Test results key lengths: ' + str(probableKeyLengths) + '\n')
    
        hackedMessage = None
        # try best guess for each keylength starting with largest
        for keyLength in probableKeyLengths:
            #if not SILENT_MODE:
            #    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
            hackedMessage = self.attemptBestGuessHackWithKeyLength(keyLength)
            if hackedMessage != None:
                break
        
        if hackedMessage == None:
            # The best guesses didn't work, now try brute force with probable key lengths
            for keyLength in probableKeyLengths:
                #if not SILENT_MODE:
                #    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = self.attemptBruteHackWithKeyLength(keyLength)
                if hackedMessage != None:
                    break
                 
        #None of the key lengths worked. Now trying all permutations
        if hackedMessage == None:
            #if not SILENT_MODE:
            print 'Failure to hack with probable keys. Now brute forcing keys. This could take a while'
            for keyLength in range(1, MAX_KEY_LENGTH + 1):
                # don't re-check key lengths already tried from Kasiski
                if keyLength not in probableKeyLengths:
                    #if not SILENT_MODE:
                    #    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                    hackedMessage = self.attemptBruteHackWithKeyLength(keyLength)
                    if hackedMessage != None:
                        break
                    
        return hackedMessage
    
    def isVigenere(self):
        probableKeyLengths = self.kasiskiTest()
        
        hackedMessage = self.getMostLikelyHack(probableKeyLengths[0])
        
        isVigenere = False
        if hackedMessage != None and hackedMessage.percentConfidence > 80:
            isVigenere = True
                    
        return isVigenere
    
    def encrypt(self, key, text):
        return self.translateMessage(key, text, 'encrypt')
    
    def decrypt(self, key, text):
        return self.translateMessage(key, text, 'decrypt')
    
    def translateMessage(self, key, message, mode):
        translated = []  # stores the encrypted/decrypted message string
    
        keyIndex = 0
        key = key.upper()
    
        for symbol in message:  # loop through each character in message
            num = LETTERS.find(symbol.upper())
            if num != -1:  # -1 means symbol.upper() was not found in LETTERS
                if mode == 'encrypt':
                    num += LETTERS.find(key[keyIndex])  # add if encrypting
                elif mode == 'decrypt':
                    num -= LETTERS.find(key[keyIndex])  # subtract if decrypting
    
                num %= len(LETTERS)  # handle the potential wrap-around
    
                # add the encrypted/decrypted symbol to the end of translated.
                if symbol.isupper():
                    translated.append(LETTERS[num])
                elif symbol.islower():
                    translated.append(LETTERS[num].lower())
    
                keyIndex += 1  # move to the next letter in the key
                if keyIndex == len(key):
                    keyIndex = 0
            else:
                # The symbol was not in LETTERS, so add it to translated as is.
                translated.append(symbol)
    
        return ''.join(translated)
