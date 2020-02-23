from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...
    max_score = 0
    max_index = 0
    n = sum([v for v in hand.values()])
    all_available = []
    for i in range(1, n+1):
        all_available.extend(get_perms(hand, i))
    valid = []
    for word in all_available:
        if is_valid_word(word, hand, word_list):
            valid.append(word)
    if len(valid) == 0:
        return None
    i = 0
    for word in valid:
        score = get_word_score(word, n)
        if score > max_score:
            max_score = score
            max_index = i
        i += 1
    return valid[max_index]
        

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...
    score = 0
    handlen = calculate_handlen(hand)
    while True:
        print 'Current Hand:'
        display_hand(hand)
        word = comp_choose_word(hand, word_list)
        print 'computer choose word:', word
        if word == None:
            break
        if is_valid_word(word, hand, word_list):
            hand = update_hand(hand, word)
            earn = get_word_score(word, handlen)
            score += earn
            print word, 'earn', earn, 'points, Total points:', score, '\n'
        else:
            print 'invalid word,', word, ' please try again'
            continue
    
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
    again = False
    last_hand = {}
    while True:
        opt = ''
        opt = raw_input('select a letter to go an action:\n n: new game\n r: replay the last game\n e: exit the game\n')
        if opt == 'n':
            hand = deal_hand(HAND_SIZE)
            last_hand = hand.copy()
            while True:
                player = raw_input('choose the play, u for user and c for computer\n')
                if player == 'u':
                    play_hand(hand.copy(), word_list)
                elif player == 'c':
                    comp_play_hand(hand.copy(), word_list)
                else:
                    continue
                break
            again = True
        elif opt == 'r':
            if not again:
                continue
            else:
                while True:
                    player = raw_input('choose the player, u for user and c for computer\n')
                    if player == 'u':
                        play_hand(hand.copy(), word_list)
                    elif player == 'c':
                        comp_play_hand(hand.copy(), word_list)
                    else:
                        continue
                    break
                again = True
        elif opt == 'e':
            break
        else:
            continue

        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
