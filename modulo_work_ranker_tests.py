# Author: storm

from modulo_word_ranker import ModuloWordRanker

def run_tests():
    tester = ModuloWorkRankerTester()
    tester.run()


class ModuloWorkRankerTester(object):
    """For testing ModuloWorkRanker"""
    def __init__(self):
        super(ModuloWorkRankerTester, self).__init__()
        self.words = "bookkeeper question".split()
        self.wr = ModuloWordRanker()

    def test(self, word):
        print("%s:\n %d"%(word, self.wr.calc_rank(word)))


    def run(self):
        big_word = ""
        for word in self.words:
            big_word += word
            self.test(word)

        self.test(big_word)
        big_word *= 10
        self.test(big_word)


run_tests()
