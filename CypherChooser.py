import operator
from FrequencyAnalyzer import FrequencyAnalyzer
from ShiftCracker import ShiftCracker
from VigenereHacker import VigenereHacker

#class to analyze a cypher text and return a guess for what type of cypher it is.
class CypherChooser:
    SUBST = "SUBSTITUTION"
    SHIFT = "SHIFT"
    PERMU = "PERMUTATION"
    VIGENERE = "VIGENERE"
    OTP = "ONE_TIME_PAD"

    def __init__(self, cypherText):
        self.cypherText = cypherText
        self.freqAnalyzer =  FrequencyAnalyzer(cypherText)
        
    def getCypherType(self):
        type = ""
        if self.freqAnalyzer.englishLetterMatch > 90:
            if self.freqAnalyzer.rawFreqMatchOrderToEngish > 80:
                #possibly permutation
                type = self.PERMU
            else:
                #possibly shift or substitution
                hacker = ShiftCracker(self.cypherText)
                retVal = hacker.analysisHack()
                if retVal.percentConfidence > 80:
                    type = self.SHIFT
                else:
                    type = self.SUBST
        else:
            #possibly vignere or one time pad
            hacker = VigenereHacker(self.cypherText)
            if hacker.isVigenere():
                type = self.VIGENERE  
            else:
                type = self.OTP
                
        return type        
        
    def printCypherStats(self):
        self.freqAnalyzer.printStats()
 