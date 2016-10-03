# Author: storm

from modulo_calculator import ModuloCalculator


class ModuloWordRanker(object):
    """ 
    Calculates the modulo 'rank' of words (strings), using the
    given modulus. 
    The 'rank' of a word its placement in lexicographical order 
    (aka, lexicographic|lexical|dictionary|alphabetical order).
    See https://en.wikipedia.org/wiki/Lexicographical_order.
    """

    # Used as the default modulus. 
    MODULUS = int(1e9+7) #this prime is often used in coding challenges
    
    
    @classmethod
    def rank(cls, word_str):
        """ Not super useful.. """
        return cls.ranks(word_str)[word_str]


    @classmethod
    def ranks(cls, *word_strs: dict(type=list, help='a list of strings')
              ) -> "{word_1:rank_1, ..., word_n:rank_n}":
        """
        Calculates the ranks of words in a list.
        Returns a dictionary of the form:
          {word_1:rank_1, ..., word_n:rank_n}
        """
        d = {}
        wr = cls()
        for word in word_strs:
            d[word] = wr.calc_rank(word)
        del wr
        return d
    
    
    # WARNING:
    #   Undefined behaviour when modulus is not a prime.
    def __init__(self,
            modulus: dict(type=int, help='a prime') = MODULUS,
            word_str: dict(type=str, help='a word to rank') = ""):
        super(ModuloWordRanker, self).__init__()
        self.mc = ModuloCalculator(modulus)
        self.calc_rank(word_str) # <-- calls _set_word(word_str)


    def __del__(self):
    #     print(" ** %s is dying **"%str(self))
        del self.mc
    #     print("length of last word:", len(self.word))
        del self.word
    #     print("rank of last word:  ", self.rank)
        del self.rank
        del self.char_counts
        del self.unique_chars
    #     print(" ** %s is dead **\n"%str(self))

    
    def _set_word(self, word_str):
        """ Resets everything except for our ModuloCalculator. """

        # Collect unique characters
        char_counts_tmp = {}
        for c in word_str:
            char_counts_tmp[c] = 1 + char_counts_tmp.setdefault(c, 0)
        self.char_counts = char_counts_tmp

        # Sort the unique characters, and store in an immutable
        #   collection for a compiler boost
        unique_chars_tmp = list(char_counts_tmp.keys())
        unique_chars_tmp.sort()
        self.unique_chars = tuple(unique_chars_tmp)

        self.rank = 1
        self.word = word_str


    def _fact(self, n):
        """ 'Modulo factorial' """
        return self.mc.mod_fact(n) # defer to the ModuloCalculator


    def _inv_fact(self, n):
        """ 'Modulo inverse factorial' """
        return self.mc.mod_inverse_fact(n) # defer to the ModuloCalculator


    def _calc_permutations(self, l_idx):
        """
        Calculates the number of distinct permutations of word[l_idx:],
        modded by the modulus.
        """
        m = self.mc.mod
        num_perms = self._fact(len(self.word[l_idx:]))
        for c in self.unique_chars:
            if self.char_counts[c] > 1: # since 1! == 0! == 1

                # This commented-out line is a lot slower than the equivalent
                #   one immediately after it:
                # num_perms = self.mc.multiply(num_perms, self._inv_fact(self.char_counts[c]))
                num_perms = (num_perms * self._inv_fact(self.char_counts[c]))%m

        return num_perms


    def _increment_char_counts_to_idx(self, r_idx):
        """ Increments each character's count through word[:r_idx]. """
        for c in self.word[:r_idx]:
            self.char_counts[c] += 1


    def _decrement_char_counts_to_idx(self, r_idx):
        """ Decrements each character's count through word[:r_idx]. """
        for c in self.word[:r_idx]:
            self.char_counts[c] -= 1


    def _update_rank(self, c, l_idx):
        """ Updates the rank of the word. """
        self.char_counts[c] -= 1
        # self.rank = self.mc.add(self.rank, self._calc_permutations(l_idx))
        self.rank = (self.rank + self._calc_permutations(l_idx))%self.mc.mod
        self.char_counts[c] += 1


    def calc_rank(self, word_str):
        """ Updates the rank of the word. """
        self._set_word(word_str)
        if len(word_str) <= 1: return 1

        for i in range(0, len(word_str)):
            self._decrement_char_counts_to_idx(i)

            for c in self.unique_chars:
                if c == self.word[i]: break
                if self.char_counts[c]:  #> 0:
                    self._update_rank(c, i+1)

            self._increment_char_counts_to_idx(i)

        return self.rank
