import re, collections
import sys
from nltk.tokenize import word_tokenize
from nltk.metrics import edit_distance
from nltk.util import ngrams

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

    def correctionsForWord(self, word):
        if word in self.tokens: return []
        return [token for token in self.tokens if edit_distance(token, word) < 3]

    def correctionsForWords(self, words, index):
        if len(words) == 0: return []
        wordToBeCorrected = words[index]
        corrections = dict([(word, 0) for word in self.correctionsForWord(wordToBeCorrected)])

        n = self.ngrams.n

        for i in range(n):
            context = words[index+i-n+1:index+i+1]
            for correction in corrections:
                context[n-i-1] = correction
                corrections[correction] += self.ngrams[tuple(context)]

        corrections = list(corrections.items())

        print("SUMMA COMING ", end= " ")
        print(sum([x[1] for x in corrections]))
        if sum([x[1] for x in corrections]) == 0:
            corrections = [(word, self.wordFrequencies[(word,)]) for word in self.correctionsForWord(wordToBeCorrected)]

        corrections.sort(key=lambda word: -word[1])
        return corrections[:8]

spellCorr = SpellCorr(word_tokenize(open('korpus.txt').read().lower()))


#sample1 = "Det är första gngen i Statoils histoyia oljebolaget vidtar en sådan åtgärd."

sample1 = """En tjugoprig tjej stpr vir kassan ocj ska betal när expediten ber om legimitation.
Nähä men det kanske går bra ändp?
Ja, men skrv ut det under det nu dp sp vämför vi sen.
Tjejen och expediten tittar undrande op kollegan som lugnt fortsätter att vika kläder.
Ja om du skriver under kvrror sp jab vu jämföra ed din anamnteckning på kortet."""


word_tokenize(sample1)

#print(spellCorr.correctionsForWords(["vad", "tr"]))
#print(spellCorr.findErrors(word_tokenize(sample1.lower())))

tokens = word_tokenize(sample1.lower())
for i in range(len(tokens)):
    print(tokens[i], end=" ")
    print(spellCorr.correctionsForWords(tokens, i))
