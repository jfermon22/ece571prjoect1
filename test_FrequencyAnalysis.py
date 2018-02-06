import FrequencyAnalysis
from StdSuites.AppleScript_Suite import string
from FrequencyAnalysis import getLetterCount
from FrequencyAnalysis import englishFreqMatchScore

def main():

    #inF = open(raw_input("Enter Filename: "),'r')
    inF = open("cipher1.txt",'r')
    dataString=inF.read().replace('\n', '')
    print(dataString)
    
    print "Letter Count:",getLetterCount(dataString),"\n"
    print "English Freq match score:",englishFreqMatchScore(dataString),"\n"
    

if __name__ == "__main__":
    main()