import unittest
from nltk.tokenize import word_tokenize
from SpellCorr import SpellCorr, NGram

class SpellCorrTests(unittest.TestCase):

    tokens1 = word_tokenize("a monkey once stole a monkey")

    def test_unigram(self):
        unigram = NGram(1, SpellCorrTests.tokens1)
        self.assertEqual(unigram[('a',)], 1)
        self.assertEqual(unigram[('monkey',)], 2)
        self.assertEqual(unigram[('monkez',)], 0)

    def test_unigram(self):
        bigram = NGram(2, SpellCorrTests.tokens1)
        self.assertEqual(bigram[('a', 'monkey')], 2)
        self.assertEqual(bigram[('monkey', 'once')], 1)
        self.assertEqual(bigram[('monkez', 'oncz')], 0)

    def test_spellcorr(self):
        spellCorr = SpellCorr(word_tokenize("monkey money mega monster"))
        self.assertEqual(spellCorr.correctionsForWord('monkez', 1), ['monkey'])
        self.assertEqual(set(spellCorr.correctionsForWord('monkez', 2)), set(['monkey', 'money']))


if __name__ == '__main__':
    unittest.main()
