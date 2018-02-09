from FrequencyAnalyzer import FrequencyAnalyzer
from StdSuites.AppleScript_Suite import string


def main():

    # inF = open(raw_input("Enter Filename: "),'r')
    inF = open("cipher1.txt", 'r')
    dataString = inF.read().replace('\n', '')
   # print(dataString)
    
    freqAnalyze = FrequencyAnalyzer(dataString)
    freqAnalyze.printStats()
    
    #print "Letter Count:", getLetterCount(dataString), "\n"
    #print "English Freq match score:", englishFreqMatchScore(dataString), "\n"
    

if __name__ == "__main__":
    main()