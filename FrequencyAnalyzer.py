import operator

class FrequencyAnalyzer:
    englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 
                         'H': 06.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 
                         'W': 02.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 
                         'K': 00.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
    englishBigramFreq = {'TH' :  2.71, 'HE' :  2.33, 'IN' :  2.03, 'ER' :  1.78, 'AN' :  1.61, 'RE' :  1.41,  'ES' :  1.32, 'ON' :  1.32,
                         'ST' :  1.25, 'NT' :  1.17, 'EN' :  1.13, 'AT' :  1.12, 'ED' :  1.08, 'ND' :  1.07, 'TO' :  1.07, 'OR' :  1.06,  
                         'EA' :  1.00, 'TI' :  0.99, 'TE' :  0.98, 'AR' :  0.98, 'NG' :  0.89, 'AL' :  0.88, 'IT' :  0.88, 'AS' :  0.87,
                         'IS' :  0.86, 'HA' :  0.83, 'ET' :  0.76, 'SE' :  0.73, 'OU' :  0.72, 'OF' :  0.71}
    englishTrigramFreq = {'THE' :  1.81, 'AND' :  0.73, 'ING' :  0.72, 'ENT' :  0.42, 'ION' :  0.42, 'HER' :  0.36,
                          'FOR' :  0.34, 'THA' :  0.33, 'NTH' :  0.33, 'INT' :  0.32, 'ERE' :  0.31, 'TIO' :  0.31, 
                          'TER' :  0.30, 'EST' :  0.28, 'ERS' :  0.28, 'ATI' :  0.26, 'HAT' :  0.26, 'ATE' :  0.25, 
                          'ALL' :  0.25, 'ETH' :  0.24, 'HES' :  0.24, 'VER' :  0.24, 'HIS' :  0.24, 'OFT' :  0.22, 
                          'ITH' :  0.21, 'FTH' :  0.21, 'STH' :  0.21, 'OTH' :  0.21, 'RES' :  0.21, 'ONT' :  0.20}
    ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def __init__(self, rawText):
        self.rawText = rawText
        self.letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
        self.rawTextLength = 0
        for letter in self.rawText.upper():
            if letter in self.LETTERS:
                self.letterCount[letter] += 1
                self.rawTextLength += 1
                
        self.letterFrequency = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
        for key,value in self.letterCount.items():
            self.letterFrequency[key] = float(self.letterCount[key])/float(self.rawTextLength)*100.0
            
        self.letterFrequency = sorted(self.letterFrequency.items(), key=operator.itemgetter(1),reverse=True)
        self.englishLetterFreq = sorted(self.englishLetterFreq.items(), key=operator.itemgetter(1),reverse=True)
            
        self.bigramCount = {}  
        self.bigramFrequency = {}
        for iii in range(1, len(self.rawText)):
            bigram = self.rawText[iii:iii+2]
            if bigram in self.bigramCount:
               self.bigramCount[bigram] += 1
            else:
               self.bigramCount[bigram] = 1
               
        for key,value in self.bigramCount.items():
            self.bigramFrequency[key] = float(self.bigramCount[key])/float(self.rawTextLength)*100.0
            
        self.bigramFrequency = sorted(self.bigramFrequency.items(), key=operator.itemgetter(1),reverse=True)
        self.englishBigramFreq = sorted(self.englishBigramFreq.items(), key=operator.itemgetter(1),reverse=True)
        self.bigramFrequency = self.bigramFrequency[:len(self.englishBigramFreq)]
            
        self.trigramCount = {}  
        self.trigramFrequency = {}
        for iii in range(1, len(self.rawText)):
            trigram = self.rawText[iii:iii+3]
            if trigram in self.trigramCount:
               self.trigramCount[trigram] += 1
            else:
               self.trigramCount[trigram] = 1
               
        for key,value in self.trigramCount.items():
            self.trigramFrequency[key] = float(self.trigramCount[key])/float(self.rawTextLength)*100.0
        self.trigramFrequency = sorted(self.trigramFrequency.items(), key=operator.itemgetter(1),reverse=True)
        self.englishTrigramFreq = sorted(self.englishTrigramFreq.items(), key=operator.itemgetter(1),reverse=True)
        self.trigramFrequency = self.trigramFrequency[:len(self.englishTrigramFreq)]
        
        self.letterPercentDifference = []
        for i in range(len(self.englishLetterFreq)):
            refKey,refFreq = self.englishLetterFreq[i]
            letKey,letFreq = self.letterFrequency[i]
            newKey = str(i) + " " + refKey + "->" + letKey
            self.letterPercentDifference.append(tuple((newKey,abs(refFreq-letFreq)/refFreq*100.0)))
            
        self.bigramPercentDifference = []
        for i in range(len(self.englishBigramFreq)):
            refKey,refFreq = self.englishBigramFreq[i]
            letKey,letFreq = self.bigramFrequency[i]
            newKey = str(i) + " " + refKey + "->" + letKey
            self.bigramPercentDifference.append(tuple((newKey,abs(refFreq-letFreq)/refFreq*100.0)))
            
        self.trigramPercentDifference = []
        for i in range(len(self.englishTrigramFreq)):
            refKey,refFreq = self.englishTrigramFreq[i]
            letKey,letFreq = self.trigramFrequency[i]
            newKey = str(i) + " " + refKey + "->" + letKey
            self.trigramPercentDifference.append(tuple((newKey,abs(refFreq-letFreq)/refFreq*100.0)))
            
        match = 0.0
        for i in range(len(self.letterPercentDifference[:6])):
            refKey,refFreq = self.letterPercentDifference[i]
            match += refFreq
        self.englishLetterMatch = 100 - ( match / 6 );
            
        match = 0.0
        for i in range(len(self.bigramPercentDifference[:6])):
            refKey,refFreq = self.bigramPercentDifference[i]
            match += refFreq

        self.englishBigramMatch = 100 - ( match / 6 );
        
        match = 0.0
        for i in range(len(self.trigramPercentDifference[:6])):
            refKey,refFreq = self.trigramPercentDifference[i]
            match += refFreq

        self.englishTrigramMatch = 100 - ( match / 6 );
        
        self.rawFreqMatchOrderToEngish = 0;
        for iii in range(1,len(self.letterFrequency[:6])):
            key,value = self.letterFrequency[iii]
            if iii == self.ETAOIN.find(key):
                self.rawFreqMatchOrderToEngish +=1
        for iii in range(len(self.letterFrequency)-6,len(self.letterFrequency)):
            key,value = self.letterFrequency[iii]
            if iii == self.ETAOIN.find(key):
                self.rawFreqMatchOrderToEngish +=1
                
        self.rawFreqMatchOrderToEngish = self.rawFreqMatchOrderToEngish/12.0 *100.0;
           

    def printStats(self):
        print "Raw text: ",self.rawText
        print "raw text length: ",self.rawTextLength
        
       
        #print "letter count: ",sorted(self.letterCount.items(), key=operator.itemgetter(1),reverse=True)
        print "letter frequency: ",self.letterFrequency[:6]
        #print "bigram count : ",sorted(self.bigramCount.items(), key=operator.itemgetter(1),reverse=True)
        print "bigram frequency : ",self.bigramFrequency[:6]
        #print "trigram count : ",sorted(self.trigramCount.items(), key=operator.itemgetter(1),reverse=True)
        print "trigram frequency : ",self.trigramFrequency[:6]
        print "letter percent difference : ",self.letterPercentDifference[:6]
        print "bigram percent difference : ",self.bigramPercentDifference[:6]
        print "trigram percent difference : ",self.trigramPercentDifference[:6]
        print "english letter match : ",self.englishLetterMatch
        print "english bigram match  : ",self.englishBigramMatch
        print "english trigram match : ",self.englishTrigramMatch
        print "english raw frequency order match : ",self.rawFreqMatchOrderToEngish
        
    def getLetterCount(self):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message parameter.
        return self.letterCount
    
    def getLetterFrequency(self):
   # Returns a dictionary with keys of single letters and values of the
   # count of how many times they appear in the message parameter.
        return self.letterFrequency

    def getItemAtIndexZero(self,x):
         return x[0]

    def getFrequencyOrder(self):
    # Returns a string of the alphabet letters arranged in order of most
    # frequently occurring in the message parameter.

    # first, get a dictionary of each letter and its frequency count
         letterToFreq = self.getLetterCount(self.rawText)

     # second, make a dictionary of each frequency count to each letter(s)
     # with that frequency
         freqToLetter = {}
         for letter in self.LETTERS:
            if letterToFreq[letter] not in freqToLetter:
                 freqToLetter[letterToFreq[letter]] = [letter]
            else:
                freqToLetter[letterToFreq[letter]].append(letter)

    # third, put each list of letters in reverse "ETAOIN" order, and then
    # convert it to a string
         for freq in freqToLetter:
             freqToLetter[freq].sort(key=self.ETAOIN.find, reverse=True)
             freqToLetter[freq] = ''.join(freqToLetter[freq])

     # fourth, convert the freqToLetter dictionary to a list of tuple
     # pairs (key, value), then sort them
         freqPairs = list(freqToLetter.items())
         freqPairs.sort(key=self.getItemAtIndexZero, reverse=True)

    # fifth, now that the letters are ordered by frequency, extract all
     # the letters for the final string
         freqOrder = []
         for freqPair in freqPairs:
             freqOrder.append(freqPair[1])

         return ''.join(freqOrder)
