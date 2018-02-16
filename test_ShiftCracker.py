from ShiftCracker import ShiftCracker
from StdSuites.AppleScript_Suite import string


def main():

    # inF = open(raw_input("Enter Filename: "),'r')
    inF = open("cipher1.txt", 'r')
    dataString = inF.read().replace('\n', '')
    # print(dataString)
    
    hacker = ShiftCracker(dataString)
    #cracker.bruteCrack()
    retVal = hacker.analysisHack()
    
    if retVal.key < 0 :
        print "Frequency analysis did not find strong correlation between cypher and English. This is likely not a shift cypher"
    else:
        print "Key: " + str(retVal.key)
        print "Percent Confidence: "+ str(retVal.percentConfidence)
        print retVal.decryptedText
    
    #print "Letter Count:", getLetterCount(dataString), "\n"
    #print "English Freq match score:", englishFreqMatchScore(dataString), "\n"
    

if __name__ == "__main__":
    main()

