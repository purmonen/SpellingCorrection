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
        self.trigrams = NGram(3, tokens)
        self.ngrams = NGram(2, tokens)
        print("Inited SpellCorr with " + str(self.tokens) + " tokens")

    def correctionsForWord(self, word, distance):
        return [token for token in self.tokens if edit_distance(token, word) <= distance]

    def ngramCorrectionsForWords(self, ngrams, words, index, distance):
        if len(words) == 0: return []
        wordToBeCorrected = words[index]
        corrections = dict([(word, 0) for word in self.correctionsForWord(wordToBeCorrected, distance)])
        n = ngrams.n
        for i in range(n):
            context = words[index+i-n+1:index+i+1]
            if len(context) == 0: continue
            for correction in corrections:
                context[n-i-1] = correction
                corrections[correction] += ngrams[tuple(context)]
        corrections = list(corrections.items())
        corrections.sort(key=lambda word: -word[1])
        return list(filter(lambda x: x[1] > 0, corrections))

    def trigramCorrectionsForWords(self, words, index, distance):
        return self.ngramCorrectionsForWords(self.trigrams, words, index, distance)

    def bigramCorrectionsForWords(self, words, index, distance):
        return self.ngramCorrectionsForWords(self.ngrams, words, index, distance)

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

    sample1 = """
    Ja, men skrv ut det under det nu dp sp vämför vi sen.
    Tjejen och expediten tittar undrande op kollegan som lugnt fortsätter att vika kläder.
    Ja om du skriver under kvrror sp jab vu jämföra ed din anamnteckning på kortet."""

    sample = """Tyvär stog dem brevid oss tillsvidare men det värkade iallafalll vara det ända sett vi behövde inteagera med varandra."""

    tokens = word_tokenize(sample.lower())
    wfTokens = tokens.copy()
    bigramTokens = tokens.copy()
    trigramTokens = tokens.copy()
    superTokens = tokens.copy()

    for i in range(len(tokens)):
        print(tokens[i])
        if not spellCorr.isWordCorrect(tokens[i]):

            trigramCorrectionsWithDistance1 = spellCorr.trigramCorrectionsForWords(tokens, i, 1)
            print('    tg1: ', end="")
            print(trigramCorrectionsWithDistance1[:8])

            trigramCorrectionsWithDistance2 = spellCorr.trigramCorrectionsForWords(tokens, i, 2)
            print('    tg2: ', end="")
            print(trigramCorrectionsWithDistance2[:8])

            bigramCorrectionsWithDistance1 = spellCorr.bigramCorrectionsForWords(tokens, i, 1)
            print('    ng1: ', end="")
            print(bigramCorrectionsWithDistance1[:8])

            bigramCorrectionsWithDistance2 = spellCorr.bigramCorrectionsForWords(tokens, i, 2)
            print('    ng2: ', end="")
            print(bigramCorrectionsWithDistance2[:8])


            wfCorrectionsWithDistance1 = spellCorr.wordFrequencyCorrectionsForWord(tokens[i], 1)
            print('    wf1: ', end="")
            print(wfCorrectionsWithDistance1[:5])

            wfCorrectionsWithDistance2 = spellCorr.wordFrequencyCorrectionsForWord(tokens[i], 2)
            print('    wf2: ', end="")
            print(wfCorrectionsWithDistance2[:5])

            bigramCorrections = (bigramCorrectionsWithDistance1 + bigramCorrectionsWithDistance2)
            if len(bigramCorrections) > 0:
                bigramTokens[i] = '[' + bigramCorrections[0][0] + ', ' + tokens[i] + ']'


            trigramCorrections = (trigramCorrectionsWithDistance1 + trigramCorrectionsWithDistance2)
            if len(trigramCorrections) > 0:
                trigramTokens[i] = '[' + trigramCorrections[0][0] + ', ' + tokens[i] + ']'

            wfCorrections = (wfCorrectionsWithDistance1 + wfCorrectionsWithDistance2)
            if len(wfCorrections) > 0:
                wfTokens[i] = '[' + wfCorrections[0][0] + ', ' + tokens[i] + ']'

            superCorrections = trigramCorrections + bigramCorrections + wfCorrections
            if len(superCorrections) > 0:
                superTokens[i] = '[' + superCorrections[0][0] + ', ' + tokens[i] + ']'
                tokens[i] = superCorrections[0][0]

    print('ngram corrections')
    print(' '.join(bigramTokens))

    print()
    print('WF corrections')
    print(' '.join(wfTokens))

    print()
    print('Super corrections')
    print(' '.join(superTokens))
