import nltk
import random

from typing import List, Tuple, Dict, NewType
from nltk.metrics import ConfusionMatrix


# VAR ==================================================================================================================

Trigrams = NewType('Trigrams', List[ Tuple[str, str] ])
Bigrams = NewType('Bigrams', List[ Tuple[str, str] ])
Unigrams = NewType('Unigrams', List[str])

stopwords = nltk.corpus.stopwords.words('english')
stopwords += list('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~') + ['first', 'second', 'third', 'fourth', 'fifth']

Labeled_String = NewType('Labeled_String', Tuple[str, bool])
Features = NewType('Features', Dict[str, bool])
Feature_Set = NewType('Feature_Set', Tuple[Features, bool])


# PREP =================================================================================================================

def seed_train_test(text_list: List[Labeled_String]) -> Tuple[ List[Labeled_String], List[Labeled_String] ]:

    random.seed(500)
    random.shuffle(text_list)

    train_idx = round(len(text_list) * 0.8)
    train = text_list[:train_idx]
    test = text_list[train_idx:]

    return train, test


def get_most_common(word_list: List[str]) -> Tuple[Trigrams, Bigrams, Unigrams]:

    # stems = [
    #     [nltk.stem.porter.PorterStemmer().stem(word)
    #      for word in nltk.word_tokenize(line.lower()) if word not in stopwords] for line in word_list]

    stems = [
        [nltk.stem.WordNetLemmatizer().lemmatize(word)
        for word in nltk.word_tokenize(line.lower()) if word not in stopwords] for line in word_list]

    trigrams = nltk.FreqDist(b for line in stems for b in nltk.trigrams(line))
    trigrams = Trigrams([grams for grams, count in trigrams.items() if count >= 5])

    bigrams = nltk.FreqDist(b for line in stems for b in nltk.bigrams(line))
    bigrams = Bigrams([grams for grams, count in bigrams.items() if count >= 5])

    unigrams = nltk.FreqDist(stem for line in stems for stem in line)
    unigrams = Unigrams([tuple([grams]) for grams, count in unigrams.items() if count >= 10])

    return trigrams, bigrams, unigrams


def extract_ngram_features(text: str, most_common: Tuple[Trigrams, Bigrams, Unigrams]) -> Features:

    # stems = [
    #     nltk.stem.porter.PorterStemmer().stem(word)
    #     for word in nltk.word_tokenize(text.lower()) if word not in stopwords]

    stems = [
        nltk.stem.WordNetLemmatizer().lemmatize(word)
        for word in nltk.word_tokenize(text.lower()) if word not in stopwords]

    text_grams = [ngram for n in (3, 2, 1) for ngram in nltk.ngrams(stems, n)]
    # trigrams, bigrams, unigrams = most_common

    features = Features({i: i in text_grams for gram_list in most_common for i in gram_list})
    # features.update({
    #     'section_definitions': True if 'mean' in [i[0] for i in nltk.FreqDist(stems).most_common(5)] else False})

    return features


# TRAIN ----------------------------------------------------------------------------------------------------------------


def evaluate_test(
        naive_bayes: nltk.classify.naivebayes.NaiveBayesClassifier, test: List[Labeled_String],
        most_common: Tuple[Trigrams, Bigrams, Unigrams]):

    test_features = [(extract_ngram_features(t, most_common), label) for (t, label) in test]

    test_results = [naive_bayes.classify(extract_ngram_features(t, most_common)) for (t, label) in test]
    test_gold = [label for t, label in test_features]
    confusion = ConfusionMatrix(test_gold, test_results)

    print(f"Accuracy: {nltk.classify.util.accuracy(naive_bayes, test_features):.4f};\n{confusion}")
    print(f"Delta: {', '.join([str(n) for n, result in enumerate(test_results) if result != test_gold[n]])}\n")
    naive_bayes.show_most_informative_features()


def train_naive_bayes(labeled_strings: List[Labeled_String]):
    # prepare training/test data
    train, test = seed_train_test(labeled_strings)

    # get n-grams
    most_common_ngrams = get_most_common([text for (text, label) in train if label == True])

    # train title model
    train_features = [(extract_ngram_features(text, most_common_ngrams), label) for (text, label) in train]
    naive_bayes = nltk.classify.naivebayes.NaiveBayesClassifier.train(train_features)

    evaluate_test(naive_bayes, test, most_common_ngrams)
    return most_common_ngrams, naive_bayes
