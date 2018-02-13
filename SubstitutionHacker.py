import operator
from FrequencyAnalyzer import FrequencyAnalyzer
from fractions import gcd
import copy


class SubstitutionHacker:
    
    letterMapping = {'A': '', 'B': '', 'C': '', 'D': '', 'E': '',
                     'F': '', 'G': '', 'H': '', 'I': '', 'J': '',
                     'K': '', 'L': '', 'M': '', 'N': '', 'O': '',
                     'P': '', 'Q': '', 'R': '', 'S': '', 'T': '',
                     'U': '', 'V': '', 'W': '', 'X': '', 'Y': '', 'Z': ''}

    LETTERS     = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    KEY_LETTERS = 'ZMAYTXLPRSBWEFQCIUDGHJKNOV'
    
    def __init__(self, rawText):
        self.rawText = rawText
        self.freqAnalyzer = FrequencyAnalyzer(rawText)
        
    def getBlankMap(self):
        return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [],
                     'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
                     'K': [], 'L': [], 'M': [], 'N': [], 'O': [],
                     'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
                     'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
    
    def analysisCrack(self):
              
        if self.freqAnalyzer.englishLetterMatch < 80:
             print "Frequency analysis did not find strong correlation between cypher and English. This is likely not a substitution cypher"
             return False
        
        self.printFreq()
        self.createAnalysisKeyMaps()
        self.printMappedLetters()
        print "\nDecryption vs original ( first 100 letters):\n"
        self.printDecryption(100)
        print self.rawText[:100]
        print "\n"
        self.hack()
          
        #print freqList

#         key0, value0 = freqList[0]
#         key1, value1 = freqList[1]
#         print "Printing best guess:" + str((value0 + (100 - abs(value0 - value1) / value0)) / 2.0) + "% certainty"
#         keyA = key0
#         keyB = key0 % len(self.LETTERS)
#         print self.shiftText(self.rawText, keyA, keyB)
#         print  "Key A: " + str(keyA) + " Key B: " + str(keyB)
          
    def hack(self):
        
        option = 0
        while option != 6:
            option = self.getOption()
           
            if option == 0:
                self.printFreq()
            elif option == 1:
                self.replaceLetter()
            elif option == 2:
                self.printDecryption()
            elif option == 3:
                self.printEncDecSideXSide() 
            elif option == 4:
                self.printMappedLetters() 
            elif option == 5:
                self.printUnmappedLetters()
            
    def printFreq(self):
        print "Common Letter Frequencies"
        print self.freqAnalyzer.letterPercentDifference
        print "----------------------------------------"
        print "Common Bigram Frequencies"
        print self.freqAnalyzer.bigramPercentDifference
        print "----------------------------------------"
        print "Common Trigram Frequencies"
        print self.freqAnalyzer.trigramPercentDifference
         
    def replaceLetter(self):
        encLetter = ''
        while encLetter == '':
            encLetter = raw_input("What encrypted letter do you want to replace?").upper()
            if len(encLetter) != 1 or self.LETTERS.find(encLetter) == -1:
                encLetter = '';
                print "Please enter a valid letter"
            break
    
        decLetter = ''
        while decLetter == '':
            decLetter = raw_input("What is the decrypted value?").upper()
            if len(decLetter) != 1 or self.LETTERS.find(decLetter) == -1:
                decLetter = '';
                print "Please enter a valid letter"
            break
        
        print "Saving: " + decLetter + "->" + encLetter
        
        self.letterMapping[encLetter] = decLetter
 
    def getOption(self):
        print "-------------------------"
        print "Options"
        print "0: Print letter/bigram Frequencies"
        print "1: replace letter"
        print "2: print decrypted text"
        print "3: print encrypted/decrypted text sample"
        print "4: replacement letter mapping" 
        print "5: print unmapped letters" 
        print "6: quit"
        print "-------------------------"
        
        option = ''
        while option == '':
            option = int(input("What would you like to do?"))
            if option < 0 or option > 6:
                option = '';
                print "Please enter a valid option"
            break
        
        return option
        
    def printDecryption(self, numLetters = None):
        decText = ""
        iii = 0;
        for letter in self.rawText.upper():
            if self.letterMapping[letter] != '':
                decText += self.letterMapping[letter]
            else:
                decText += ' '
                
            iii += 1
            if numLetters is None:
                iii
            elif iii == numLetters:
                break
            
        print decText
   
    def printUnmappedLetters(self):
        for key,value in self.letterMapping.items():
            if value == '':
                print key + " "
    
    def printMappedLetters(self):
        for key,value in self.letterMapping.items():
            if value != '':
                print key + "->" + value
    
    def printEncDecSideXSide(self):
        print self.rawText[:50]
        print self.printDecryption(50)

    def decryptWithKey(self):
        textList = []
        for iii in range(len(self.rawText)):
            eLetter = self.rawText[iii:iii+1]
            pos = self.KEY_LETTERS.find(eLetter)
            dLetter = self.LETTERS[pos:pos+1]
            textList.append(dLetter)
        return "".join(textList)
    
    def printKey(self):
        for iii in range(len(self.LETTERS)):
            print self.LETTERS[iii:iii+1] + "->" + self.KEY_LETTERS[iii:iii+1]
    
    def createAnalysisKeyMaps(self):
        monogramMap = self.getBlankMap()
        for iii in range(len(self.freqAnalyzer.letterFrequency)):
            keyText,valueText = self.freqAnalyzer.letterFrequency[iii]
            keyEng,valueEng = self.freqAnalyzer.englishLetterFreq[iii]
            self.letterMapping[keyText] = keyEng
            monogramMap[keyText].append(keyEng)
         
        bigramMap = self.getBlankMap()
        for iii in range(len(self.freqAnalyzer.bigramFrequency[:6])):
            keyText,valueText = self.freqAnalyzer.bigramFrequency[iii]
            keyText0 = keyText[:1]
            keyText1 = keyText[1:]
            keyEng,valueEng = self.freqAnalyzer.englishBigramFreq[iii]
            keyEng0 = keyEng[:1]
            keyEng1 = keyEng[1:]
            bigramMap[keyText0].append(keyEng0)
            bigramMap[keyText1].append(keyEng1)
        
        trigramMap = self.getBlankMap()
        for iii in range(len(self.freqAnalyzer.trigramFrequency[:6])):
            keyText,valueText = self.freqAnalyzer.trigramFrequency[iii]
            keyText0 = keyText[:1]
            keyText1 = keyText[1:2]
            keyText2 = keyText[2:3]
            keyEng,valueEng = self.freqAnalyzer.englishTrigramFreq[iii]
            keyEng0 = keyEng[:1]
            keyEng1 = keyEng[1:2]
            keyEng2 = keyEng[2:3]
            trigramMap[keyText0].append(keyEng0)
            trigramMap[keyText1].append(keyEng1)
            trigramMap[keyText2].append(keyEng2)
        
            
        #print self.letterMapping
        #print monogramMap
        #print bigramMap
        #print trigramMap
        
        self.mergeKeyMaps( monogramMap, bigramMap, trigramMap)
        
    def mergeKeyMaps(self,monogramMap, bigramMap, trigramMap):
        mergeMap = {}
        for key,value in monogramMap.items():
            voteMap = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0,
                     'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
                     'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0,
                     'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
                     'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
            monoLetter = (monogramMap[key])[0]
            if self.freqAnalyzer.ETAOIN.find(monoLetter) < 6: 
               voteMap[monoLetter] += len(self.freqAnalyzer.ETAOIN) - self.freqAnalyzer.ETAOIN.find(monoLetter)
            elif self.freqAnalyzer.ETAOIN.find(monoLetter) > 20:
               voteMap[monoLetter] += len(self.freqAnalyzer.ETAOIN) - self.freqAnalyzer.ETAOIN.find(monoLetter)
            else:
               voteMap[monoLetter] += 1
               
            for iii in range(len(bigramMap[key])):
                votes = len(bigramMap[key]) + 1
                letter = (bigramMap[key])[iii]
                voteMap[letter] += votes
                votes -= 1
                
            for iii in range(len(trigramMap[key])):
                votes = len(trigramMap[key]) + 1
                letter = (trigramMap[key])[iii]
                voteMap[letter] += votes
                votes -= 1
            #remove zeroes from map
            for key1,value in voteMap.items():
                if value == 0:
                    voteMap.pop(key1)
            
            voteMapList = sorted(voteMap.items(), key=operator.itemgetter(1),reverse=True)
            mergeMap[key] = voteMapList
            #print key + ":" + str(mergeMap[key])
        
        mergeMapConst = copy.deepcopy(mergeMap)

        usedLetters = ""
        usedKeys = ""
        unmappedKeys = [];
        unmappedValues = [];
        LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        while len(mergeMap):
            largestKey = ''
            largestValue = 0
            largestDecLet = ''
            for key,value in mergeMap.items():
                keyLet,keyVal = (mergeMap[key])[0]
                if keyVal > largestValue and usedLetters.find(keyLet) == -1:
                    largestValue = keyVal
                    largestKey = key
                    largestDecLet = keyLet
            
            usedLetters += largestDecLet
            usedKeys += largestKey
            #print "Mapping Key:" + largestKey + " -> " + largestDecLet + "," + str(largestValue)
            #print "used:" + usedKeys + " -> " + usedLetters
            self.letterMapping[largestKey] = largestDecLet
            
            if len(largestKey):
                mergeMap.pop(largestKey)
            else:
                #print "Unmapped keys: "
                for iii in range(len(LETTERS)):
                    if usedKeys.find(LETTERS[iii:iii+1]) == -1:
                        #print LETTERS[iii:iii+1]
                        unmappedKeys.append(LETTERS[iii:iii+1])
                #print "Unmapped Values: "
                for iii in range(len(LETTERS)):
                    if usedLetters.find(LETTERS[iii:iii+1]) == -1:
                        #print LETTERS[iii:iii+1]
                        unmappedValues.append(LETTERS[iii:iii+1])
                
                for iii in range(len(unmappedKeys)):
                    tmpList = [(unmappedValues[iii],1)]
                    mergeMap.update({unmappedKeys[iii]:tmpList});    
        