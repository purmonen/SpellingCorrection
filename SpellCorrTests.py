import unittest
from nltk.tokenize import word_tokenize
from SpellCorr import SpellCorr, NGram

class SpellCorrTests(unittest.TestCase):

    tokens1 = word_tokenize("a monkey once stole a monkey")

    def test_unigram(self):
        unigram = NGram(1, SpellCorrTests.tokens1)
        self.assertEqual(unigram[('a',)], 2)
        self.assertEqual(unigram[('monkey',)], 2)
        self.assertEqual(unigram[('monkez',)], 0)

    def test_bigram(self):
        bigram = NGram(2, SpellCorrTests.tokens1)
        self.assertEqual(bigram[('a', 'monkey')], 2)
        self.assertEqual(bigram[('monkey', 'once')], 1)
        self.assertEqual(bigram[('monkez', 'oncz')], 0)

    def test_spellcorr(self):

        spellCorr = SpellCorr(word_tokenize("money mega monster, a monkey once stole a monkey, money once"))
        self.assertEqual(spellCorr.correctionsForWord('monkez', 1), ['monkey'])
        self.assertEqual(set(spellCorr.correctionsForWord('monkez', 2)), set(['monkey', 'money']))

        bigramCorrections = spellCorr.bigramCorrectionsForWords(word_tokenize('once upon a time a monxey once'), 5, 1)
        self.assertEqual(len(bigramCorrections), 2)
        self.assertEqual(bigramCorrections[0][0], 'monkey')
        self.assertEqual(bigramCorrections[0][1], 3)

        self.assertEqual(bigramCorrections[1][0], 'money')
        self.assertEqual(bigramCorrections[1][1], 1)


if __name__ == '__main__':
    unittest.main()
