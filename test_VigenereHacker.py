from VigenereHacker import VigenereHacker
from StdSuites.AppleScript_Suite import string


def main():

    # inF = open(raw_input("Enter Filename: "),'r')
    inF = open("cipher3.txt", 'r')
    dataString = inF.read().replace('\n', '')
    #4print(dataString[:20])
    
    hacker = VigenereHacker(dataString)
    decryption = hacker.hack()
    
    if decryption == None:
       print "Failed to find key. May not be a Vigenere cipher"
    else:
       print decryption
    #print cracker.decryptWithKey();
    #print cracker.printKey();
    #cracker.analysisCrack()
    
    #print "Letter Count:", getLetterCount(dataString), "\n"
    #print "English Freq match score:", englishFreqMatchScore(dataString), "\n"
    

if __name__ == "__main__":
    main()

