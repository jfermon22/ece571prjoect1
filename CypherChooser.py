import operator
from FrequencyAnalyzer import FrequencyAnalyzer

#class to analyze a cypher text and return a guess for what type of cypher it is.
class CypherChooser:

    def __init__(self, cypherText):
        self.cypherText = cypherText
        self.freqAnalyzer =  FrequencyAnalyzer(cypherText)
        
    def getCypherType(self):
        type = ""
        if self.freqAnalyzer.englishLetterMatch > 90:
            if self.freqAnalyzer.rawFreqMatchOrderToEngish > 80:
                #possibly permutation
                type = "PERMUTATION"
            else:
                #possibly shift or substitution
                type = "SHIFT OR SUBSTITUTION"   
        else:
            #possibly vignere or one time pad
                type = "VIGENERE or ONE-TIME PAD"   
                
        return type        
        
    def printCypherStats(self):
        self.freqAnalyzer.printStats()
 