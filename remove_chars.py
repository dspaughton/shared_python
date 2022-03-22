"""
Example solutions for a coding challenge.
    Problem is to remove various character pairs from a string.
    Illustrates the use of various loop constructs, and the 'walrus' operator.
"""

def process_string1_commented(text, pairs):
    lentext = len(text)
    while True: #emulate do-while
        for pair in pairs:
            done = ''   # already searched
            rem  = text # still have to search
            #
            # cumbersome loop:
            #while True: # set then test index
            #    index = rem.find(pair)
            #    if -1 == index: # handles empty rem
            #       break
            #
            # bad 'walrus' loop, without brackets 'index' becomes True or False :-0
            #while  index:=rem.find(pair) != -1:
            #
            # correct 'walrus' loop, with required brackets around the walrus assignment
            while (index:=rem.find(pair)) != -1: # set then test index with 'walrus' operator
                done += rem[:index]
                rem   = rem[index+len(pair):]
                text = done + rem
        if lentext == len(text):
            return text # get out if no progress
        lentext = len(text)



def process_string1(text, pairs):
    lentext = len(text)
    while True: #emulate do-while
        for pair in pairs:
            done = ''   # already searched
            rem  = text # still have to search
            # set then test index with 'walrus' operator (since python 3.8)
            while (index:=rem.find(pair)) != -1:
                done += rem[:index]
                rem   = rem[index+len(pair):]
                text = done + rem
        if lentext == len(text):
            return text # get out if no progress
        lentext = len(text)



def process_string2(text, pairs):
    lentext = len(text)
    while True: #emulate do-while
        for pair in pairs:
            text = text.replace(pair,'')
        if lentext == len(text):
            return text # get out if no progress
        lentext = len(text)


def process_string3(text, pairs):
    lentext = -1 # impossible value means we loop at least once
    while lentext != len(text): # stop if no progress
        lentext = len(text)
        for pair in pairs:
            text = text.replace(pair,'')
    return text


my_string = 'other stuff abba bye-bayerW' 
my_pairs = ['ab','ba','er']

print( my_string, '-> #'+process_string1(my_string,my_pairs)+'#' )
print( my_string, '-> #'+process_string2(my_string,my_pairs)+'#' )
print( my_string, '-> #'+process_string3(my_string,my_pairs)+'#' )

