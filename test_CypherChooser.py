from CypherChooser import CypherChooser
from StdSuites.AppleScript_Suite import string


def main():

    filelist  = ["cipher1.txt","cipher2.txt","cipher3.txt","cipher4.txt"]
    for file in filelist: 
        inF = open(file, 'r')
        dataString = inF.read().replace('\n', '')
        #4print(dataString[:20])
        
        chooser = CypherChooser(dataString)
        cyphertype = chooser.getCypherType()
        
        if cyphertype == None:
            print file + ": Failed to find type. Possibly One Time Pad"
        else:
            print file + ": "  + cyphertype
        #print cracker.decryptWithKey();
        #print cracker.printKey();
        #cracker.analysisCrack()
        
        #print "Letter Count:", getLetterCount(dataString), "\n"
        #print "English Freq match score:", englishFreqMatchScore(dataString), "\n"
    

if __name__ == "__main__":
    main()

