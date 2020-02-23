# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!
    

word = choose_word(wordlist)

print 'Welcome to the game, Hangman!\n'
print 'I am thinking a work that is',  str(len(word)), 'letters long.\n'


def check_guess(c):
    if c in available_char:
        available_char.remove(c)
        return True
    else:
        return False


def show_word():
    str = ''
    for c in word:
        if c in guess_dict:
            str += c
        else:
            str += '_'
    return str

def check_game():
    for c in word:
        if not c in guess_dict:
            return False
    return True

def loop():
    global guessLeft
    guessLeft = 8
    global available_char
    available_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    global available_str
    available_str = ''
    global guess_dict
    guess_dict = {}
    while guessLeft > 0:
        print '------------------------------------------'
        print 'You have', guessLeft ,'guesses left'
        print 'Available letters:', available_str.join(available_char)
        c = raw_input('Please guess a letter: ')
        c = c.lower()
        if not check_guess(c):
            print 'invalid input, please try again'
            continue
        if c in word:
            guess_dict[c] = 1
            print 'Good guess:', show_word(), '\n'
        else:
            print 'Oops! That letter not in my word', show_word()
        guessLeft -= 1
        if check_game():
            print 'Congratulations! You won.\n'
            exit

loop()
print 'Sorry. You failed\n'
