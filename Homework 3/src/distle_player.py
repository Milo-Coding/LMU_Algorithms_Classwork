from edit_dist_utils import *


class DistlePlayer:
    '''
    AI Distle Player! Contains all of the logic to automagically play
    the game of Distle with frightening accuracy (hopefully)
    '''

    # attributes needed to play
    my_words: set[str]
    guesses: int
    max_guesses: int

    def start_new_game(self, dictionary: set[str], max_guesses: int) -> None:
        '''
        Called at the start of every new game of Distle, and parameterized by
        the dictionary composing all possible words that can be used as guesses,
        only ONE of which is the correct Secret word that your agent must
        deduce through repeated guesses and feedback.

        [!] Should initialize any attributes that are needed to play the
        game, e.g., by saving a copy of the dictionary, etc.

        Parameters:
            dictionary (set[str]):
                The dictionary of words from which the correct answer AND any
                possible guesses must be drawn
            max_guesses (int):
                The maximum number of guesses that are available to the agent
                in this game of Distle
        '''
        # save our vars
        self.my_words = dictionary.copy()
        self.max_guesses = max_guesses
        self.guesses = max_guesses + 1  # add one so we can count down in make_guess
        return

    def make_guess(self) -> str:
        '''
        Requests a new guess to be made by the agent in the current game of Distle.
        Uses only the DistlePlayer's attributes that had been originally initialized
        in the start_new_game method.

        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.

        Returns:
            str:
                The next guessed word from this DistlePlayer
        '''
        # what is our current guess
        self.guesses -= 1

        if (len(self.my_words) == 0):
            return "loaded"  # guess something word if we miscalculated in case we could get lucky
        # the shortest word gives the most info about our secret word
        guess: str = max(self.my_words, key=len)
        return guess

    def get_feedback(self, guess: str, edit_distance: int, transforms: list[str]) -> None:
        '''
        Called by the DistleGame after the DistlePlayer has made an incorrect guess.
        The feedback furnished is described in the parameters below. Your agent will
        use this feedback in an attempt to rule out as many remaining possible guess
        words as it can, through which it can then make better guesses in make_guess.

        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.

        Parameters:
            guess (str):
                The last, incorrect guess made by this DistlePlayer
            edit_distance (int):
                The numerical edit distance between the guess your agent made and the
                secret word
            transforms (list[str]):
                The list of top-down transforms needed to turn the guess word into the
                secret word, i.e., the transforms that would be returned by your
                get_transformation_list(guess, secret_word)
        '''
        # temp set for comparisons
        temp_dict: set[str]

        # count transpositions and the letters we have for later
        transpose: int = 0
        my_letters: dict = self.str_to_dict(guess)

        # figure out how long our word acutally is
        word_length: int = len(guess) + 1

        for mov in transforms:
            if mov == "D":
                word_length -= 1
            elif mov == "I":
                word_length += 1
            elif mov == "T":
                transpose += 1

        temp_dict = self.my_words.copy()
        for word in temp_dict:
            # check length the first time the loop is called to speed up the trimming
            if self.guesses == self.max_guesses and len(word) == word_length:
                self.my_words.remove(word)

            # if all the transitions are transpositions, we have all the letters we need
            elif (transpose == edit_distance):
                if (self.str_to_dict(word) != my_letters):
                    self.my_words.remove(word)

            # any guess word with a different edit distance can't be the secret word
            # we do this check 2nd (and therefore less often) because it is the most intensive
            elif (get_transformation_list(guess, word) != transforms):
                self.my_words.remove(word)

        return

    def str_to_dict(self, word: str) -> dict:
        """
        create a dictionary of characters with corrosponding ints to the frequency of each character in the word
        """
        word_as_dict: dict = {}
        for char in list(word):
            if char not in word_as_dict:
                word_as_dict[char] = 1
            else:
                word_as_dict[char] += 1
        return word_as_dict
    