# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    for i in secret_word:
        if i in letters_guessed:
            continue
        else:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    word = str()
    for i in secret_word:
        if i in letters_guessed:
            word = word + i
        else:
            word = word + "_ "
    return word




def get_available_letters(letters_guessed):
    available_letters = list(string.ascii_lowercase)
    for i in letters_guessed:
        if i in available_letters:
            available_letters.remove(i)
    return "".join(available_letters)
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    gues = 6
    warn = 3
    letters_guessed = []
    print("Вітаю у грі 'Шибениця' ")
    print("Слово має довжину", len(secret_word), "літер")
    while gues > 0 and not is_word_guessed(secret_word, letters_guessed):
      print("У вас є", gues, "спроб")
      print("Доступні літери:", get_available_letters(letters_guessed))
      guess = input("Будь ласка запропонуйте літеру - ")
      if len(guess) == 1 and str.isalpha(guess):
        guess = str.lower(guess)
        if guess in letters_guessed:
          if warn != 0:
            warn = warn - 1
            print("Ви вже обрали цю літеру, тому у вас залишилось", warn, "попередження:", get_guessed_word(secret_word, letters_guessed))
          else:
            gues = gues - 1
            print("У вас не залишилось попереджень тому ви втрачаєте спробу:", get_guessed_word(secret_word, letters_guessed))
        else:
          letters_guessed.append(guess)
          if guess in secret_word:
            print("Гарна спроба:", get_guessed_word(secret_word, letters_guessed))
          else:
            if guess in ['a', 'e', 'i', 'o', 'u']:
              gues = gues - 2
            else:
              gues = gues - 1
            print("Ця літера відсутня у слові:", get_guessed_word(secret_word, letters_guessed))
      else:
        if warn != 0:
          warn = warn - 1
          print("Ця літера не належить слову, у вас залишилось", warn, "попередження:", get_guessed_word(secret_word, letters_guessed))
        else:
          gues = gues - 1
          print("Ця літера не належить слову. У вас не залишилось попереджень, тому ви втрачаєте спробу:", get_guessed_word(secret_word, letters_guessed))
      print("-----------------------------------")
    if is_word_guessed(secret_word, letters_guessed):
      print("Мої вітання ви перемогли! Ваш загальний рахунок: ", gues * len(set(secret_word)))
    else:
      print("У вас закінчились спроби, на жаль ви програли")



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    s = []
    my_word = my_word.replace(" ", " ")
    other_word = other_word.replace(" ", "")
    if len(my_word) == len(other_word):
      for i in range(0,len(my_word)):
        if my_word[i] == "_":
          if other_word[i] in my_word:
            return False
    for i in range(len(other_word)):
      s = []
      for j in range(len(other_word)):
        if(other_word[i] == other_word[j]):
          s.append(my_word[j])
        k = 1
        if(s[0] == '_'): 
          k = 0
        for a in s:
          if((a == '_' and k == 1) or (a != '_' and k == 0)): 
            return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    match = []
    for i in wordlist:
      if match_with_gaps(my_word, i):
        match.append(i)
    if len(match) == 0:
      print("Співпадінь не знайдено")
    else:
      for j in match:
        print(j, end=" ")
    print("")



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    gues = 6
    warn = 3
    letters_guessed = []
    print("Вітаю у грі 'Шибениця' ")
    print("Слово має довжину", len(secret_word), "літер")
    print("-----------------------------------")
    while gues > 0 and not is_word_guessed(secret_word, letters_guessed):
      print("У вас є", gues, "спроб")
      print("Доступні літери:", get_available_letters(letters_guessed))
      guess = input("Будь ласка запропонуйте літеру - ")
      if len(guess) == 1 and str.isalpha(guess):
        guess = str.lower(guess)
        if guess in letters_guessed:
          if warn != 0:
            warn = warn - 1
            print("Ви вже обрали цю літеру, тому у вас залишилось", warn, "попередження:", get_guessed_word(secret_word, letters_guessed))
          else:
            gues = gues - 1
            print("У вас не залишилось попереджень тому ви втрачаєте спробу:", get_guessed_word(secret_word, letters_guessed))
        else:
          letters_guessed.append(guess)
          if guess in secret_word:
            print("Гарна спроба:", get_guessed_word(secret_word, letters_guessed))
          else:
            if guess in ['a', 'e', 'i', 'o', 'u']:
              gues = gues - 2
            else:
              gues = gues - 1
            print("Ця літера відсутня у слові:", get_guessed_word(secret_word, letters_guessed))
      else:
        if warn != 0:
          warn = warn -  1
          print("Ця літера не належить слову, у вас залишилось", warn, "попередження:", get_guessed_word(secret_word, letters_guessed))
        else:
          gues = gues - 1
          print("Ця літера не належить слову. У вас не залишилось попереджень, тому ви втрачаєте спробу:", get_guessed_word(secret_word, letters_guessed))
      print("-----------------------------------")
    if is_word_guessed(secret_word, letters_guessed):
      print("Мої вітання ви перемогли! Ваш загальний рахунок: ", gues * len(set(secret_word)))
    else:
      print("У вас закінчились спроби, на жаль ви програли")




# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)