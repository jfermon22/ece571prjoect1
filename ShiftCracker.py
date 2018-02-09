import operator
from FrequencyAnalyzer import FrequencyAnalyzer

class ShiftCracker:
    letterMapping = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J':'J', 'K': 'K', 'L': 'L', 'M': 'M', 
                        'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def __init__(self, rawText):
        self.rawText = rawText
        
    def shiftText(self,text,num):
       textList = []
       for iii in range(0,len(text)):
           textList.append(self.LETTERS[ (self.LETTERS.find(text[iii]) + num) % 26 ])
       return "".join(textList)
           
    def bruteCrack(self):
       textSlice = self.rawText[:20]
       for iii in range(1,26):
           print str(iii) + ": " + self.shiftText(textSlice,iii)
           
       num = 0
       while num == 0:
          num = int(input("Enter number of decrypted text, else 26: "))
          if num < 1 or num > 26:
             print "Please enter valid number from 1-26"
             num = 0
             continue
             
          if num < 26 : 
               print self.shiftText(self.rawText,num)
               ans = raw_input("Is the cypher cracked? yn:")
               if ans == "y":
                  print "Hooray!"
               else:
                  print "Let's try again"
                  num = 0
          else:
               print("Sorry, This may not be a shift cyper")
               
    def analysisCrack(self):
          freqList = []
          for iii in range(1,26):
              shiftedText = self.shiftText(self.rawText,iii)
              freqAnalyzer = FrequencyAnalyzer(shiftedText)
              if freqAnalyzer.englishLetterMatch > 70 and freqAnalyzer.englishBigramMatch > 70:
                 freqList.append(tuple((iii,freqAnalyzer.rawFreqMatchOrderToEngish)))
                 
          if not freqList:
             print "Frequency analysis did not find strong correlation between cypher and English. This is likely not a shift cypher"
             return False
          
          freqList = sorted(freqList, key=operator.itemgetter(1),reverse=True)
          
          #print freqList
          key0,value0 = freqList[0]
          key1,value1 = freqList[1]
          print "Printing best guess:" + str( ( value0 + (100-abs(value0 - value1) /value0 ))/2.0) + "% certainty"
          print self.shiftText(self.rawText,key0)
          
          
 