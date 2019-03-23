from nltk import word_tokenize
from nltk import tokenize
import string, re
import time
import pyarabic.araby as ar

class Normalizer(object):

    transPunctuation = str.maketrans('', '', string.punctuation)
    reURL = re.compile(r'\b([--:\w?@%&+~#=]*\.[a-z]{2,4}\/{0,2})((?:[?&](?:\w+)=(?:\w+))+|[--:\w?@%&+~#=]+)?\b')
    reDecimals = re.compile(r'\b([1-9]\d*(\.|\,)\d*|0?(\.|\,)\d*[1-9]\d*|[1-9]\d*)\b')
    dictCodes = {"CODE_URL": "<unk>", "CODE_DECIMAL": "<unk>"}

    def __init__(self):
        self._tokens = []
        self._vocab = []

    @property
    def vocab(self):
        self._vocab = sorted(set(self._tokens))
        self._vocab.remove('<unk>')
        self._vocab.insert(0, '<unk>')
        self._vocab.insert(1, '<s>')
        self._vocab.insert(2, '</s>')

        print(len(self._tokens))
        print(len(self._vocab))

        return self._vocab

    def removePunctuation(self, text):
        return text.translate(self.transPunctuation)

    def normalizeURLs(self, line):
        return self.reURL.sub('CODE_URL', line)

    def removeRepeatition(self, line):
        return re.sub(r'(.)\1+', r'\1', line)

    def normalizeDecimals(self, line):
        return line
        #return self.reDecimals.sub('CODE_DECIMAL', line)

    def translateCodesForTokens(self, tokens):
        newTokens = []
        for tok in tokens:

            #if len(tok) > 25:
            #    break

            newTok = re.sub('({})'.format('|'.join(map(re.escape, self.dictCodes.keys()))), lambda m: self.dictCodes[m.group()], tok)
            newTokens.append(newTok)

        return newTokens

    def translateCodesForLine(self, line):
        return re.sub('({})'.format('|'.join(map(re.escape, self.dictCodes.keys()))), lambda m: self.dictCodes[m.group()], line)

    def normalizeLine(self, line):
        return line

    def tokenize(self, line):
        return word_tokenize(line)

    def NormalizeLine(self, line):
        line = self.normalizeLine(line)
        tokens = self.tokenize(line)
        tokens = self.translateCodesForTokens(tokens)
        self._tokens.extend(tokens)
        return self.translateCodesForLine(line)

    def ProcessFile(self, fileName):

        start = time.time()

        with open(fileName, 'rt', encoding = "utf-8") as f:
            for i, line in enumerate(f):

                if i > 1000:
                    break

                self.NormalizeLine(line)

        end = time.time()
        print("Total execution time is : {} seconds".format(end - start))

        return self.vocab

    def SaveVocab(self, fileName):
        with open(fileName, 'wt', encoding = "utf-8") as f:
            for _, word in enumerate(self.vocab):
                f.write("%s\n" % word)

class NormalizerEN(Normalizer):
    
    def normalizeLine(self, line):
        line = self.normalizeURLs(line)
        line = self.normalizeDecimals(line)
        line = self.removeRepeatition(line)
        return line

    def tokenize(self, line):
        return tokenize.wordpunct_tokenize(line)


class NormalizerAR(Normalizer):

    def normalizeAlef(self, line):
        line = re.sub('[إأآا]', 'ا', line)
        return line

    def tokenize(self, line):
        return tokenize.wordpunct_tokenize(line)
    
    def normalizeLine(self, line):
        line = self.normalizeURLs(line)
        line = self.normalizeDecimals(line)
        line = self.removeRepeatition(line)
        line = self.normalizeAlef(line)
        line = ar.strip_harakat(line)
        line = ar.strip_tatweel(line)
        line = ar.normalize_ligature(line)
        return line

"""
normalizer = NormalizerEN()
vocab = normalizer.ProcessFile("Data/TED2013/TED2013.ar-en.en")
normalizer.SaveVocab("Data/TED2013/TED2013.vocab.en")
"""

"""
normalizer = NormalizerAR()
vocab = normalizer.ProcessFile("Data/TED2013/TED2013.ar-en.ar")
normalizer.SaveVocab("Data/TED2013/TED2013.vocab.ar")
"""