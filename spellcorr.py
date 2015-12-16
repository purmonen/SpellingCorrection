import re, collections
import sys
from nltk.tokenize import word_tokenize
from nltk.metrics import edit_distance

class NGram:

    def __init__(self, n, tokens):
        self.n = n
        self.ngrams = {}
        for i in range(n-1, len(tokens)):
            key = tuple(tokens[i-n+1:i+1])
            if not key in self.ngrams:
                self.ngrams[key] = 0
            self.ngrams[key] += 1

    def __getitem__(self, key):
        return self.ngrams.get(key, 0)

class SpellCorr:

    def __init__(self, tokens):
        self.tokens = set(tokens)
        self.wordFrequencies = NGram(1, tokens)
        self.ngrams = NGram(2, tokens)

    def correctionsForWord(self, word, distance):
        return [token for token in self.tokens if edit_distance(token, word) <= distance]

    def bigramCorrectionsForWords(self, words, index, distance):
        if len(words) == 0: return []
        wordToBeCorrected = words[index]
        corrections = dict([(word, 0) for word in self.correctionsForWord(wordToBeCorrected, distance)])
        n = self.ngrams.n
        for i in range(n):
            context = words[index+i-n+1:index+i+1]
            for correction in corrections:
                context[n-i-1] = correction
                corrections[correction] += self.ngrams[tuple(context)]
        corrections = list(corrections.items())
        corrections.sort(key=lambda word: -word[1])
        return list(filter(lambda x: x[1] > 0, corrections))

    def wordFrequencyCorrectionsForWord(self, word, distance):
        corrections = [(word, self.wordFrequencies[(word,)]) for word in self.correctionsForWord(word, distance)]
        corrections.sort(key=lambda x: -x[1])
        return corrections

    def correctionsForWords(self, words, index):
        bigramCorrections = self.bigramCorrectionsForWords(words, index, 3)
        if len(bigramCorrections) > 0:
            return bigramCorrections
        else:
            corrections = [(word, self.wordFrequencies[(word,)]) for word in self.correctionsForWord(words[index], 3)]
            corrections.sort(key=lambda x: -x[1])
            return corrections

    def isWordCorrect(self, word):
        return word in self.tokens


if __name__ == '__main__':
    spellCorr = SpellCorr(word_tokenize(open('text.txt').read().lower()))
    #sample1 = "Det är första gngen i Statoils histoyia oljebolaget vidtar en sådan åtgärd."

    sample1 = """En tjugoprig tjej stpr vir kassan ocj ska betal när expediten ber om legimitation.
    Nähä men det kanske går bra ändp?
    Ja, men skrv ut det under det nu dp sp vämför vi sen.
    Tjejen och expediten tittar undrande op kollegan som lugnt fortsätter att vika kläder.
    Ja om du skriver under kvrror sp jab vu jämföra ed din anamnteckning på kortet."""

    word_tokenize(sample1)

    tokens = word_tokenize(sample1.lower())
    for i in range(len(tokens)):
        print(tokens[i], end=" ")
        if not spellCorr.isWordCorrect(tokens[i]):
            print('ngrams: ', end=": ")
            print(spellCorr.bigramCorrectionsForWords(tokens, i, 3)[:8], end=", ")

            print('word frequency: ', end=": ")
            print(spellCorr.wordFrequencyCorrectionsForWord(tokens[i], 1)[:8])
        else:
            print()
