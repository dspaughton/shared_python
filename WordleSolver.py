Copyright (c) 2022 David Spaughton

import sys
import math

WIN32 = True
try:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except Exception as E:
    WIN32 = False



GoGreen    = '\x1b[42m'
GoBrown    = '\x1b[43m'
GoBlue     = '\x1b[44m'
GoBack = '\x1b[0m'


def Show(t,ch):
    if    'G'==t:
        print(GoGreen+ch+GoBack,end='')
    elif 'Y'==t:
        print(GoBrown+ch+GoBack,end='')
    else:
        print(GoBlue+ch+GoBack,end='')
        


# Letter Frequencies
LF = [
  0.929,  0.316,  0.657,  0.529,  1.048,  #ABCDE
  0.258,  0.393,  0.478,  0.878, -0.707,  #FGHIJ
  0.042,  0.740,  0.479,  0.823,  0.855,  #KLMNO
  0.501, -0.707,  0.880,  0.759,  0.842,  #PQRST
  0.560,  0.003,  0.111, -0.537,  0.250,  #UVWXY
 -0.565                                   #Z
]

def LFscore(word):
    score=0
    for i in range(5):
        index = ord(word[i]) - ord('A')
        score +=LF[index]
    return score



#==========================================================
#         Check for an 5-letter upper case word
#==========================================================
CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def Is5LUCW(word):
    if len(word)!=5:
        return False
    for ch in word:
        if ch not in CAPS:
            return False
    return True


#==========================================================
#         Check for valid character in word
#==========================================================
def GoodCharacters(word,CHARS):
    for ch in word:
        if ch not in CHARS:
            return False
    return True

#==========================================================
#              Select words by pattern
#==========================================================
def Select(word,Mask,Incl,Omit):
    for i in range(len(Mask)):
        if Mask[i]!='.' and Mask[i]!=word[i]:
            return False
    for i in range(len(Incl)):
        if -1==word.find(Incl[i]):
            return False
    for i in range(len(Omit)):
        if -1!=word.find(Omit[i]):
            return False
    return True

#==========================================================
#            Load the word list from a file
#==========================================================
def LoadWordList():
    # look for FLW.txt on same path as this python script
    filepath = sys.argv[0].replace('\\','/')
    while len(filepath) and filepath[-1] != '/':
        filepath=filepath[:-1]
    filename =  filepath+'FLW.txt'
    WL=[] # word list
    WD={} # dictionary to avoid duplicates
    with open(filename) as file:
        for line in file:
            W = line.strip().upper()
            if not W in WD: # duplicate?
                WL.append(W)
                WD[W]=WL[-1]
    return WL

#==========================================================
#      Given a word, generate wordle's hint response
#==========================================================
def MakeHint(Word,guess):
    W = Word # make copy, don't change Word
    R = ['.']*5

    # 'G' pass
    for i in range(5):
        if W[i]==guess[i]:
            R[i]='G'
            W = W[:i]+'.'+W[i+1:] # deal with repeated letters

    # 'Y' pass
    for i in range(5):
        if '.' != R[i]:
            continue
        j = W.find(guess[i])
        if -1!=j:
            R[i]='Y'
            W = W[:j]+'.'+W[j+1:] # deal with repeated letters

    # '#' pass
    for i in range(5):
        if '.' != R[i]:
            continue
        j = W.find(guess[i])
        if -1==j:
            R[i]='#'

    RR = R[0]+R[1]+R[2]+R[3]+R[4]
        
    # debug pass
    #for i in range(5):
    #    if R[i] == '.':
    #        print('Hint failed with:',Word,guess,'->',RR)
    #        continue

    return R[0]+R[1]+R[2]+R[3]+R[4]


#==========================================================
#                Suggest a guess
#==========================================================
def Suggest(WordList,FullList):
    Suggs=[]
    if len(WordList)<3:
        for W in WordList:
            H = WhatIf(W,WordList)
            Suggs.append([H,W])
    else:
        for W in FullList:
            H = WhatIf(W,WordList)
            Suggs.append([H,W])
    Suggs.sort()
    return Suggs

#==========================================================
#                   Entropy functions
#==========================================================
def Entropy(subtotal,total=-1):
    if 0==subtotal:
        return 0
    if -1==total:
        return math.log(subtotal,2)
    else:
        return (subtotal/total)*math.log(subtotal,2)


def WhatIf(guess,WordList):
    HintDict={}
    for W in WordList:
        hint = MakeHint(W,guess)
        if hint in HintDict:
            HintDict[hint] +=1
        else:
            HintDict[hint] =1
    H = 0
    for hint in HintDict:
        count = HintDict[hint]
        H +=Entropy(count,len(WordList))
    return H



FullList = LoadWordList()
WordList = FullList.copy()
HintList=[]

"""
# check compatibility of MakeHint and Filter
for word in WordList:
    for guess in WordList:
        hint = MakeHint(word,guess)
        if Filter(word,hint,guess):
            continue
        print(word,hint,guess)
quit()
"""

"""
# run a big slow simulation to check solution accuracy
# and iteration counts
for solution in FullList:
    WordList = FullList.copy()

    count=1
    guess = 'TARES'
    hint = MakeHint(solution,guess)
    if 'GGGGG'==hint:
        print('OK',solution,count)
        break
    WL=[]
    for Word in WordList:
        if hint == MakeHint(Word,guess):
            WL.append(Word)
    WordList = WL

    while True:
        if 0==len(WordList) or count>10:
            print('XX',solution,count,'syserr 0 length')
            break

        guess = Suggest(WordList,FullList)[0][1]
        count+=1
        hint = MakeHint(solution,guess)
        if 'GGGGG'==hint:
            print('OK',solution,count)
            break
        WL=[]
        for Word in WordList:
            if hint == MakeHint(Word,guess):
                WL.append(Word)
        WordList = WL
quit()
"""


print('Wordle solver v1.0 ({:,d} words in list).'.format(len(WordList)))
print('Type help for help.')

while True:
    cmd=input('>').upper()
    if ''==cmd:
        continue
    if 'QUIT'==cmd:
        quit()

    #===========================================
    # HELP
    if cmd.startswith('HELP'):
        print('Note: anything you type is converted to upper case.')
        print('Commands are:')
        print('guess <word>')
        print('      Means you just put <word> into wordle, and got a hint')
        print("      back. You are prompted for that hint, eg G##Y# where")
        print('      G means green, Y means yellow, # means gray.')
        print('      You get a chance to correct mistyped hints.')
        print('      (Type cancel to get out of the hint loop).')
        print('')
        print('whatif <word>')
        print('      Returns the expected new entropy if you guess <word>.')
        print('')
        print('list')
        print('      Lists each currently possible word.')
        print('')
        print('table')
        print('      Shows the current wordle table.')
        print('')
        print('suggest <number>')
        print('      Returns <number> best guess suggestions.')
        print('      if you leave out <number> you get 10.')
        print('')
        print('pattern <include> <omit>')
        print('      Finds words which match a pattern.')
        print('      <include> is mandatory 5 letters or dots, then a comma,')
        print('                 then optional letters to include anywhere.')
        print('      <omit> is optional. If used, it starts with a minus sign,')
        print('             followed by letters to omit.')
        print('      e.g: a...e,si -qr means select words with:')
        print('           a and e in positions 1 and 5,')
        print('           with s and i anywhere, and with p and q nowhere.')
        print('')
        print('quit')
        print('      Stops the program.')
        print('')
        continue

    #===========================================
    # WHATIF
    if cmd.startswith('WHATIF '):
        word = cmd[7:].strip()
        if not Is5LUCW(word):
            print(word,' is not a 5-letter word')
            continue
        H0 = Entropy(len(WordList))
        Ht = WhatIf(word,WordList)
        fmt = word+' Entropy: {:5.2f}->{:5.2f}, {:6.2f}\n'
        print(fmt.format(H0,Ht,Ht-H0))
        continue

    #===========================================
    # GUESS
    if cmd.startswith('GUESS '):
        guess = cmd[6:].strip().upper()
        if not Is5LUCW(guess):
            print(guess,' is not a 5-letter word')
            continue
        OldN = len(WordList)
        OldH = Entropy(OldN)
        Cancelled = False
        while not Cancelled:
            Hint=[]
            response=input('>hint? ').upper()
            if response=='CANCEL':
                Cancelled=True
                break

            if 5!=len(response) or not GoodCharacters(response,'GY#'):
                print('hints are 5 letters long, using GY# only, not:',response)
                continue

            Hint=[response,guess]
            for i in range(5):
                Show(response[i],guess[i])
            print('')
            yesno = input('Is that correct? (Y/N): ').upper()
            if yesno.startswith('Y'):
                HintList.append(Hint)
                break
        if Cancelled:
            continue

        WL=[]
        for Word in WordList:
            #if Filter(Word,response,guess):
            if response == MakeHint(Word,guess):
                WL.append(Word)
        WordList = WL

        NewN = len(WordList)
        NewH = Entropy(NewN)
        print('Old Entropy: {:5.2f} {:,d} words'.format(OldH,OldN))
        print('New Entropy: {:5.2f} {:,d} words'.format(NewH,NewN))
        print('')
        continue

    #===========================================
    # LIST
    if cmd.startswith('LIST'):
        for W in WordList:
            print(W)
        print('{:d} words'.format(len(WordList)))
        print('')
        continue

    #===========================================
    # PATTERN
    if cmd.startswith('PATTERN'):
        Z = cmd.split()
        if len(Z)<2:
            print('select needs a pattern!')
            continue
        MI = Z[1].split(',')

        if len(MI)<1 or len(MI[0])!=5:
            print('missing/invalid select <include> pattern.')
            continue
        Mask=MI[0]
        if not GoodCharacters(Mask,'.'+CAPS):
            print('invalid characters in',Mask,'<include> pattern.')
            continue

        Incl=''
        if len(MI)>1:
            Incl=MI[1]
        if not GoodCharacters(Incl,CAPS):
            print('invalid characters in',Incl,'<include> pattern.')
            continue

        Omit=''
        if len(Z)>2:
            Omit=Z[2]
            if '-' != Omit[0]:
                print('select <omit> string should start with a - sign.')
                continue
            Omit=Omit[1:]
        if not GoodCharacters(Omit,CAPS):
            print('invalid characters in',Omit,'<omit> pattern.')
            continue

        count=0
        for Word in WordList:
            if Select(Word,Mask,Incl,Omit):
                print(Word)
                count +=1
        print('Found',count,'words')
        print('')
        continue

    #===========================================
    # TABLE
    if cmd.startswith('TABLE'):
        for Hint in HintList:
            response,guess = Hint
            for i in range(5):
                    Show(response[i],guess[i])
            print('')
        print('')
        continue

    #===========================================
    # SUGGEST
    if cmd.startswith('SUGGEST'):
        Z = cmd.split()
        limit=10
        if len(Z)>1:
            try:
                limit=int(Z[1])
            except ValueError:
                print(Z[1],' is not a number!')
                continue
        Suggs=Suggest(WordList,FullList)
        Suggs=Suggs[:limit]
        H0 = Entropy(len(WordList))
        for S in Suggs:
            fmt = S[1]+' Entropy: {:5.2f}->{:5.2f}, {:6.2f}'
            print(fmt.format(H0,S[0],S[0]-H0))
        print('')
        continue

    print('Unknown command, type help for help.')
