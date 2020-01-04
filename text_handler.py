from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

# Funções para identyfycação da pergunta (super symples!)

start_question = "porque,por que,pq,por quê"
end_question = "?"
main_words = "y,ypsylon,ipslon,ipsilon,ypslon"


def word_is_contained(word, sentence, single_word=True):
    tokens = word_tokenize(sentence, 'portuguese')
    if single_word:
        for token in tokens:
            if word in token:
                return True
        return False
    else:
        return word in sentence


def evaluate_question(text):
    text = text.lower()
    sentences = sent_tokenize(text, 'portuguese')
    contains = False
    for sentence in sentences:
        if any(word_is_contained(s, sentence, False) for s in start_question.split(',')) and \
                any(word_is_contained(s, sentence, True) for s in main_words.split(',')):
            return True
    return False
