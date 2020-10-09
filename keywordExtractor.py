import re

# move these to a file
stopwords = ('is', 'not', 'that', 'there', 'are', 'can', 'you', 'with', 'of', 'those', 'after', 'all', 'one')
delimiters = (',', '.')

def parse_keywords(phrase):
    assert isinstance(phrase, str), f'{type(phrase)} is not a string'
    words = [word.strip().lower() for word in re.split(r'\W+', phrase) if len(word) > 0]
    content_words = []
    for word in words:
        if (not (word in stopwords) and not any(word in i for i in content_words)):
            content_words.append((word, words.count(word)))
    regular_exp = '|'.join(map(re.escape, stopwords + delimiters))
    candidate_keyphrases = [p.strip().lower() for p in re.split(regular_exp, phrase) if len(p) > 2]
    
    m = CoOccurrenceMatrix(content_words, candidate_keyphrases)
    word_scores = m.get_all_word_scores()
    expression_scores = m.get_all_expression_scores()
    #the number of top candidates to choose
    T = len(content_words) // 3
    #combines the word and expression scores sorts them
    scores_sorted = sorted((word_scores + expression_scores), reverse=True)
    #returns the words/expressions with the top T scores
    return scores_sorted[:T]


class CoOccurrenceMatrix:

    content_words = []
    phrases = []
    matrix = [[]]

    def __init__(self, input, phrases):
        # make sure to check for types of contents of tuples
        # assert isinstance(input, list) and (e for e in input is (type(tuple))), f'Provide a valid list of words and occurence'
        # assert isinstance(phrases, list) and (p for p in phrases is type(str)), f'Provide the keyphrases as a list of strings'
        self.matrix = [[0] * len(input)] * len(input)
        for i,tup1 in enumerate(input):
            for j,tup2 in enumerate(input):
                self.matrix[i][j] = CoOccurrenceMatrix.count_co_occurence(tup1[0], tup2[0], phrases)
        self.content_words = input
        self.phrases = phrases
        # print(phrases)
        # print(self.matrix)

    #gets the index of the tuple in content_words containing the specified words
    def get_index(self, word):
        assert isinstance(word, str), f'The word must be a string'
        for i,e in enumerate(self.content_words):
            if e[0] == word:
                return i
        # print('not found')

    #returns the sum of a row of the specified word in the matrix divided by the frequency of the word
    def get_word_score(self, word):
        assert isinstance(word, str), f'The word must be a string'
        try:
            return sum(self.matrix[self.get_index(word)]) / self.content_words[self.get_index(word)][1]
        except TypeError:
            return 0

    #returns an array of tuples of the words and their degree scores (other way around)
    def get_all_word_scores(self):
        return [(self.get_word_score(tup[0]), tup[0]) for tup in self.content_words]

    #returns an array of tuples of the phrases and their degree scores (other way around)
    def get_all_expression_scores(self):
        out = []
        for e in self.phrases:
            score = 0
            words = e.split(' ')
            for word in words:
                # print(word)
                score += self.get_word_score(word.strip())
            out.append((score, e))
        return out


    #counts the number of times that both str1 and str2 appear in the candidate phrases.
    @staticmethod
    def count_co_occurence(str1, str2, phrases):
        # assert isinstance((str1, str2), (str, str)), f'The words must be strings'
        # assert isinstance(phrases, list) and (s for s in phrases is type(str)), f'Phrases must be a list of strings'
        count = 0
        for p in phrases:
            if (str1 in p) and (str2 in p):
                count += 1
        return count

from rake_nltk import Rake
def parse_keywords_rake_nltk(phrase):
    r = Rake()
    r.extract_keywords_from_text(j)
    return r.get_ranked_phrases()
