from SubstitutionHacker import SubstitutionHacker
from StdSuites.AppleScript_Suite import string


def main():

    # inF = open(raw_input("Enter Filename: "),'r')
    inF = open("cipher2.txt", 'r')
    dataString = inF.read().replace('\n', '')
    #4print(dataString[:20])
    
    hacker = SubstitutionHacker(dataString)
    hacker.analysisCrack()
    #print cracker.decryptWithKey();
    #print cracker.printKey();
    #cracker.analysisCrack()
    
    #print "Letter Count:", getLetterCount(dataString), "\n"
    #print "English Freq match score:", englishFreqMatchScore(dataString), "\n"
    

if __name__ == "__main__":
    main()

