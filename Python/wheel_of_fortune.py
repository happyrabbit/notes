# Wheel of Fortune
# Some functions and methods that are used in the game
# time.sleep(s): delays execution of the next line of code for s seconds
# random.choice(list): returns a random element from the list
# random.shuffle(list): shuffles the list
# random.randint(a, b): returns a random integer between a and b (inclusive)

import time
import random
import json

# Commenting out the following lines
# for x in range(2, 6):
#     print('Sleep {} seconds..'.format(x))
#     time.sleep(x)
# print('Done!')

rand_number = random.randint(1, 10)
print('Random number between 1 and 10:', rand_number)

letters = [letter for letter in 'abcdefghijklmnopqrstuvwxyz']
print('Original list:', letters)
rand_letter = random.choice(letters)
print('Random letter:', rand_letter)

# Some string functions
# .uppper() and .lower() methods
# .count(s) method: returns the number of occurrences of s in the string

VOWEL_COST = 250
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS = 'AEIOU'

# We’re going to define a few useful functions for you:
# getNumberBetween(prompt, min, max) repeatedly asks the user for a number between min and max with the prompt
def getNumberBetween(prompt, min, max):
    '''repeatedly asks the user for a number between min and max with the prompt '''
    userinp = input(prompt)
    while True:
        try:
            n = int(userinp)
            if n < min:
                errmessage = 'Must be at least {}'.format(min)
            elif n > max:
                errmessage = 'Must be at most {}'.format(max)
            else:
                return n
        except ValueError:
            errmessage = '{} is not a number.'.format(userinp)
        # If we haven't gotten a number yet, add the error message and ask again
        userinp = input('{}\n{}'.format(errmessage, prompt))

# spinWheel() simulates spinning the wheel and returns a dictionary with a random prize
def spinWheel():
    '''simulates spinning the wheel and returns a dictionary with a random prize
       Examples:
       { "type": "cash", "text": "$950", "value": 950, "prize": "A trip to Ann Arbor!" },
       { "type": "bankrupt", "text": "Bankrupt", "prize": false },
       { "type": "loseturn", "text": "Lose a turn", "prize": false }
    '''
    with open("/Users/hui/Downloads/wheel.json", "r") as f:
        wheel = json.loads(f.read())
    return random.choice(wheel)

def getRandomCategoryAndPhrase():
    '''Returns a category & phrase (as a tuple) to guess
    Example:
    ("Artist & Song", "Whitney Houston's I Will Always Love You")
    '''
    with open("/Users/hui/Downloads/phrases.json", "r") as f:
        phrases = json.loads(f.read())
    category = random.choice(list(phrases.keys()))
    phrase = random.choice(phrases[category])
    return (category, phrase.upper())

def obscurePhrase(phrase, guessed):
    '''Given a phrase and a list of guessed letters, returns an obscured version
    Example:
        guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
        phrase:  "GLACIER NATIONAL PARK"
        returns: "_L___ER N____N_L P_RK"
    '''
    rv = ''
    for s in phrase:
        if (s in guessed) or (s not in LETTERS):
            rv += s
        else:
            rv += '_'
    return rv

def showBoard(category, obscuredPhrase, guessed):
    '''Returns a string representing the current state of the game'''
    current_board = '''
Category: {}
Phrase:   {}
Guessed:  {}
    '''.format(category, obscuredPhrase, ', '.join(sorted(guessed)))
    return current_board

# Part A: WOFPlayer
# YOUR TASKS BEGIN HERE
# Start by defining a class to represent a Wheel of Fortune player, called WOFPlayer. Every instance of WOFPlayer has three instance variables:

# .name: The name of the player (should be passed into the constructor)
# .prizeMoney: The amount of prize money for this player (an integer, initially 0)
# .prizes: The prizes this player has won so far (a list, initially empty)
# Of these instance variables, only name should be passed into the constructor.

# The class should also have the following methods (note: we will exclude self in our descriptions):

# .addMoney(amt): increases self.prizeMoney by `amtt
# .goBankrupt(): sets self.prizeMoney to 0
# .addPrize(prize): appends prize to self.prizes
# .__str__(): returns the player’s name and prize money in the following format:
# Steve ($1800) (for a player with instance variables .name == 'Steve' and .prizeMoney == 1800)

class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []

    def addMoney(self, amt):
        self.prizeMoney += amt

    def goBankrupt(self):
        self.prizeMoney = 0

    def addPrize(self, prize):
        self.prizes.append(prize)

    def __str__(self):
        return '{} (${})'.format(self.name, self.prizeMoney)
    
# Part B: WOFHumanPlayer
# Next, you'll define a class named WOFHumanPlayer, which should inherit from WOFPlayer (part A). Each intance of this class will represent a human player. In addition to having all of the instance variables and methods that WOFPlayer has, WOFHumanPlayer should have an additional method:

# .getMove(category, obscuredPhrase, guessed): asks the user to enter a move (using input()) and returns whatever string they entered.
# .getMove()’s prompt should be:

#   {name} has ${prizeMoney}
  
#   Category: {category}
#   Phrase:   {obscured_phrase}
#   Guessed:  {guessed}
  
#   Guess a letter, phrase, or type 'exit' or 'pass':

class WOFHumanPlayer(WOFPlayer):
    def getMove(self, category, obscuredPhrase, guessed):
        prompt = '''
        {} has ${}

        Category: {}
        Phrase: {}
        Guessed: {}

        Guess a letter, phrase, or type 'exit' or 'pass':
        '''.format(self.name, self.prizeMoney, category, obscuredPhrase, ', '.join(sorted(guessed)))
        return input(prompt)

# Part C: WOFComputerPlayer
# Finally, you'll define a class named WOFComputerPlayer, which should inherit from WOFPlayer (part A). An instance of this class will represent a computer player.
# Class variable
# .SORTED_FREQUENCIES: Should be set to 'ZQXJKVBPYGFWMUCLDRHSNIOATE', which is a list of English characters sorted from least frequent ('Z') to most frequent ('E'). We’ll use this when trying to make a “good” move.

class WOFComputerPlayer(WOFPlayer):
    SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'
    
    def __init__(self, name, level):
        WOFPlayer.__init__(self, name)
        self.level = level
    
    def smartCoinFlip(self):
        return random.randint(1, 10) <= self.level
    
    def getPossibleLetters(self, guessed):
        if self.prizeMoney < VOWEL_COST:
            return [letter for letter in letters if (letter not in guessed) and (letter not in VOWELS)]
        else:
            return [letter for letter in letters if letter not in guessed]
    
    def getMove(self, category, obscuredPhrase, guessed):
        possible_letters = self.getPossibleLetters(guessed)
        if not possible_letters:
            return 'pass'
        elif self.smartCoinFlip():
            for letter in reversed(self.SORTED_FREQUENCIES):
                if letter in possible_letters:
                    return letter
        else:
            return random.choice(possible_letters)