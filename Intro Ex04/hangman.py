####################################################
# FILE: hangman.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex4 2015-2016
# DESCRIPTION: a game of hangman
####################################################


import hangman_helper
__INIT_ALPHA_ORDER__ = 97


def update_word_pattern(word, pattern, letter):
    '''
    replaces underscores '_' in the pattern with the 'letter', if exists,
    according to the word.
    :param word: assumes string. word to guess in game.
    :param pattern: assumes string. current display of state,
                        with letters and underscores.
    :param letter: assumes char. letter guessed by player.
    :return: the updated pattern, as a string.
    '''

    for (i, char) in enumerate(word):
        if char == letter:
            pattern = pattern[:i] + letter + pattern[i+1:]

    return pattern

def check_end_game(pattern, guesses):
    '''
    decides if game over: if the word has been revealed
    or the guesses reached the maximum allowed.
    :param pattern: assumes string. contains underscores and letters guessed.
    :param guesses: number of guesses made.
    :return: a number according to win/loss/neither.
    '''

    WIN = 1
    CONTINUE = 2
    LOSS = 0

    if not '_' in pattern:
        return WIN
    elif guesses >= hangman_helper.MAX_ERRORS:
        return LOSS
    else:
        return CONTINUE

def compare_word_pattern(word, pattern):
    '''
    Compares two strings, and decides if the letters in the pattern are in
    the same indexes as in the word.
    Will also return False if lengths of strings don't equal.
    :param word: assumes string.
    :param pattern: assumes string. includes '_' as well as letters.
    :return: True or False.
    '''

    check = True

    if len(word) != len(pattern):
        return False

    for (index,letter) in enumerate(pattern):
        if letter == '_':
            continue
        else:
            if letter == word[index]:
                check = True
            else:
                check = False

    return check

def filter_words_list (words, pattern, wrong_guess_lst):
    '''
    Filters the words list by keeping only the words which:
    -have the same length of the pattern - using compare_word_pattern
    -include the identical letters in the positions of the pattern -
                                            using compare_word_pattern
    -do not have any letters that appear in the wrong guess list
    :param words: list of strings.
    :param pattern: current pattern in game, includes underscores and letters.
    :param wrong_guess_lst: list of wrong letters guessed by player.
    :return: the filtered list of words.
    '''

    fix_words = []
    new_words = []

    #new list of words with same length as pattern
    for word in words:
        if len(word) == len(pattern):
            fix_words.append(word)

    valid = True
    for word in fix_words:
        for letter in word:
            #eliminates words with letters in wrong guess list
            if letter in wrong_guess_lst:
                valid = False
                break
            if compare_word_pattern(word, pattern):
                #identical letters in same position as in pattern
                valid = True
                for (i,let) in enumerate(word):
                #checks all letters that appear in word and pattern appear
                #in same instances in pattern as in word
                    if let in pattern:
                        if let != pattern[i]:
                            valid = False
            else:
                valid = False

        if valid == True:
            new_words.append(word)

    return new_words

def letter_to_index(letter):
    '''
    Returns the index of the given letter in an alphabet list.
    '''
    return ord(letter.lower()) - __INIT_ALPHA_ORDER__

def index_to_letter(index):
    '''
    Returns the letter of a given index in an alphabet index list
    '''
    return chr(index + __INIT_ALPHA_ORDER__)

def choose_letter (words, pattern):
    '''
    :param words: list of strings.
    :param pattern: current pattern in game.
    :return: char: letter which appears most times in words list.
                    letter cannot appear in pattern.
    '''


    letters_count = [0]*26
    counting_list = [] #list of lists. inner list of letter and instances,
                                #  by order of appearance in words.

    #removes words without the letters in pattern
    for word in words:
        for letter in pattern:
            if letter != '_':
                if letter not in word:
                        words.remove(word)

    #creates a list letters_count with number of times each letter appears
    for word in words:
        for let in word:
            index = letter_to_index(let)
            letters_count[index] += 1
            counting_list.append([let,0])

    #extends counting_list (of letters appeared)
    #in order for indexes to match in next loop
    length = len(counting_list)
    while length <= 26:
        counting_list.append(['empty',0])
        length += 1

    #updates counting_list with count of times letters shown
    for (index, count) in enumerate(letters_count):
        counting_list[index][1] = count

    #chooses letter
    max_val_index = letters_count.index(max(letters_count))
    max_val = index_to_letter(max_val_index)

    #checks that chosen letter is not in pattern
    while max_val in pattern:
        letters_count[max_val_index] = 0
        max_val = index_to_letter(letters_count.index(max(letters_count)))

    return max_val


def run_single_game(words_list):
    '''
    randomly picks a word from words_list, and plays a game of hangman.
    asks player each turn for a letter.
    if guessed correct letter, adds to pattern displayed.
    if guessed incorrect letter, add to list of wrong guess and draws
    another body part on hangman.
    :param words_list: a list of words (strings).
    :return: None.
    '''

    word_to_guess = hangman_helper.get_random_word(words_list)
    num_of_guesses = 0
    letters_guessed = []
    pattern = '_' * len(word_to_guess)
    DEFAULT_MSG = hangman_helper.DEFAULT_MSG
    curr_msg = DEFAULT_MSG

    while check_end_game(pattern, num_of_guesses) == 2: #game not over

        #displays game state and gets input from player
        hangman_helper.display_state(pattern, num_of_guesses, letters_guessed,
                                     curr_msg, ask_play=False)
        current_letter_guess = hangman_helper.get_input()

        #player asks for hint
        if current_letter_guess[0] == hangman_helper.HINT:
            hint_list = filter_words_list(words_list,pattern,letters_guessed)
            hint_let = choose_letter(hint_list, pattern)
            curr_msg = hangman_helper.HINT_MSG + hint_let
            continue

        #player enters letter
        else:
            current_letter_guess = str(current_letter_guess[1])

        #guess is invalid
        if (str.islower(current_letter_guess) == False) or \
                (len(current_letter_guess) > 1):
            curr_msg = hangman_helper.NON_VALID_MSG


        #letter entered already guessed
        elif current_letter_guess in letters_guessed or \
                                        current_letter_guess in pattern:
            curr_msg = hangman_helper.ALREADY_CHOSEN_MSG +current_letter_guess


        #letter guessed correctly, updates pattern and checks if game ended
        elif current_letter_guess in word_to_guess:
            pattern = update_word_pattern(word_to_guess, pattern,
                                          current_letter_guess)
            if check_end_game(pattern, num_of_guesses) != 2:
                break
            curr_msg = DEFAULT_MSG

        #letter guessed not in word,
        #updates wrong guesses and checks if game ended
        else:
            letters_guessed.append(current_letter_guess)
            num_of_guesses += 1
            if check_end_game(pattern, num_of_guesses) != 2:
                break
            curr_msg = DEFAULT_MSG

    #WIN, asks to play again
    if check_end_game(pattern, num_of_guesses) == 1:
        hangman_helper.display_state(pattern, num_of_guesses, letters_guessed,
                                     hangman_helper.WIN_MSG, ask_play=True)
    #LOSS, asks to play again
    elif check_end_game(pattern, num_of_guesses) == 0:
        hangman_helper.display_state(pattern, num_of_guesses, letters_guessed,
                                     hangman_helper.LOSS_MSG + word_to_guess,
                                     ask_play=True)


def main():
    '''
    Executes main function.
    Iterates over the game as long as player asks to play again.
    '''

    WORDS_LIST = hangman_helper.load_words('words.txt')
    play_again = True
    while play_again:
        run_single_game(WORDS_LIST)
        play_again = hangman_helper.get_input()[1]

main()