from nltk import word_tokenize, pos_tag, load
from collections import defaultdict
import string

########################################################################################################################

corpus_r1 = 'When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow. ' \
             'The rainbow is a division of white light into many beautiful colors. These take the shape of a long ' \
             'round arch, with its path high above, and its two ends apparently beyond the horizon. There is, ' \
             'according to legend, a boiling pot of gold at one end. People look, but no one ever finds it. When ' \
             'a man looks for something beyond his reach, his friends say he is looking for the pot of gold at the ' \
             'end of the rainbow. '

corpus_r2 = 'Throughout the centuries people have explained the rainbow in various ways. Some have accepted ' \
            'it as a miracle without physical explanation. To the Hebrews it was a token that there would be ' \
            'no more universal floods. The Greeks used to imagine that it was a sign from the gods to foretell ' \
            'war or heavy rain. The Norsemen considered the rainbow as a bridge over which the gods passed from ' \
            'earth to their home in the sky. Others have tried to explain the phenomenon physically. Aristotle ' \
            'thought that the rainbow was caused by reflection of the sun\'s rays by the rain. '

corpus_r3 = 'Since then physicists have found that it is not reflection, but refraction by the raindrops ' \
            'which causes the rainbows. Many complicated ideas about the rainbow have been formed. The ' \
            'difference in the rainbow depends considerably upon the size of the drops, and the width of ' \
            'the colored band increases as the size of the drops increases. The actual primary rainbow ' \
            'observed is said to be the effect of super-imposition of a number of bows. If the red of the ' \
            'second bow falls upon the green of the first, the result is to give a bow with an abnormally ' \
            'wide yellow band, since red and green light when mixed form yellow. This is a very common ' \
            'type of bow, one showing mainly red and yellow, with little or no green or blue. '

corpus_g1 = 'You wished to know all about my grandfather. Well, he is nearly ninety-three years old; ' \
            'he dresses himself in an ancient black frock coat, usually minus several buttons; yet he ' \
            'still thinks as swiftly as ever. A long, flowing beard clings to his chin, giving those ' \
            'who observe him a pronounced feeling of the utmost respect. When he speaks, his voice is ' \
            'just a bit cracked and quivers a trifle. Twice each day he plays skilfully and with zest ' \
            'upon our small organ. Except in the winter when the ooze or snow or ice prevents, he slowly ' \
            'takes a short walk in the open air each day. We have often urged him to walk more and smoke ' \
            'less, but he always answers, \"Banana oil!\" Grandfather likes to be modern in his language. '

########################################################################################################################


def form_bigrams_subsequent(corpus: str) -> dict:
    """
    Calculate P(next word | current word) for given corpus
    Corpus must be blank space separated strings
    :param corpus: corpus string
    :return: a dictionary containing conditional probabilities of the word following each word in the corpus
    """

    # Prepare the corpus for tokenizing - normalisation
    # Remove all punctuation and make all lower case
    for s in string.punctuation:
        if s == '-':
            pass
        else:
            corpus = corpus.replace(s, '').lower()

    # print(corpus)

    # Create a default dictionary with an empty list as the default key value to hold words/probabilities
    # Tokenize the corpus string.
    # Create a temp empty string to store previous word

    bigrams_subsequent = defaultdict(list)  # Non-existent keys throw a KeyError if defaultdict not used
    corpus_tokens = word_tokenize(corpus, 'english')
    temp = ''

    # Create dictionary of next word possibilities
    # Iterate through the corpus:
    # If the temp word is not empty (as it will be initially), add the temp word as key and the word as value,
    # which essentially forms a previous word / current word pairing.
    # Assign the word to the temp word and continue until through corpus

    for word in corpus_tokens:
        if temp != '':
            bigrams_subsequent[temp].append(word)
        temp = word

    return bigrams_subsequent


def form_bigrams_previous(corpus: str) -> dict:
    """
    Calculate P(next word | current word) for given corpus
    Corpus must be blank space separated strings
    :param corpus: corpus string
    :return: a dictionary containing conditional probabilities of the word following each word in the corpus
    """

    # Prepare the corpus for tokenizing - normalisation
    # Remove all punctuation and make all lower case
    for s in string.punctuation:
        if s == '-':
            pass
        else:
            corpus = corpus.replace(s, '').lower()

    # print(corpus)

    # Create a default dictionary with an empty list as the default key value to hold words/probabilities
    # Tokenize the corpus string.
    # Create a temp empty string to store previous word

    bigrams_previous = defaultdict(list)  # Non-existent keys throw a KeyError if defaultdict not used
    corpus_tokens = word_tokenize(corpus, 'english')
    temp = ''

    # Create dictionary of next word possibilities
    # Iterate through the corpus:
    # If the temp word is not empty (as it will be initially), add the temp word as key and the word as value,
    # which essentially forms a previous word / current word pairing.
    # Assign the word to the temp word and continue until through corpus

    for word in corpus_tokens:
        if temp != '':
            bigrams_previous[word].append(temp)
        temp = word

    return bigrams_previous


def calculate_probabilities(bigrams):

    # Iterate through the word_pairings dictionary keys:
    # Create a set of all the unique words for the given key
    # Create a dictionary for the key : probabilities  to be stored
    # Iterate through the unique words:
    # Add each word as key and calculate probability as a float
    # Add the probabilities dictionary as the value to the original word

    for k in bigrams.keys():
        possibilities = set(bigrams[k])  # Remove the duplicates
        probabilities = {}
        for word in possibilities:
            probabilities[word] = float(bigrams[k].count(word)) / len(bigrams[k])
        bigrams[k] = probabilities

    return bigrams


def probability_of_subsequent_word(subsequent_probabilities: dict, word: str, candidate: str):
    """
    Show the probability of next_word given current_word
    :param subsequent_probabilities: the conditional probabilities for the given corpus
    :param word: the word to use to find the subsequent word
    :param candidate: the word to calculate probability for
    :return: the probability of next_word being the subsequent word to current_word. 0.0 if not in corpus.
    """

    # Looks for current_word in the corpus_probabilities dictionary:
    # If it exists, looks for next_word in the values for current_word:
    # If it exists, returns the value, else returns 0.0

    current_next = 0.0

    if word in subsequent_probabilities:
        if candidate in subsequent_probabilities[word]:
            current_next = subsequent_probabilities[word][candidate]

    return current_next


def probability_of_previous_word(previous_probabilities: dict, word: str, candidate: str):
    """
    Show the probability of next_word given current_word
    :param previous_probabilities: the conditional probabilities for the given corpus
    :param word: the word to use to find the subsequent word
    :param candidate: the word to calculate probability for
    :return: the probability of next_word being the subsequent word to current_word. 0.0 if not in corpus.
    """

    # Looks for current_word in the corpus_probabilities dictionary:
    # If it exists, looks for next_word in the values for current_word:
    # If it exists, returns the value, else returns 0.0

    current_prev = 0.0

    if word in previous_probabilities:
        if candidate in previous_probabilities[word]:
            current_prev = previous_probabilities[word][candidate]

    return current_prev


def subsequent_word(subsequent_probabilities, word):
    """
    Return the subsequent word with the highest probability
    :param subsequent_probabilities: per word probabilities
    :param word: the initial word
    :return: the candidate with the highest probability of being the next word
    """

    candidate = ''

    if word in subsequent_probabilities:
        candidate = max(subsequent_probabilities[word])

    if candidate is '':
        return 'No word found.'
    else:
        return candidate


def previous_word(previous_probabilities, word):
    """
    Return the subsequent word with the highest probability
    :param previous_probabilities: per word probabilities
    :param word: the initial word
    :return: the candidate with the highest probability of being the next word
    """

    candidate = ''

    if word in previous_probabilities:
        candidate = max(previous_probabilities[word])

    if candidate is '':
        return 'No word found.'
    else:
        return candidate


def subsequent_word_candidates(subsequent_probabilities, word):
    """
    Return the list of candidates
    :param subsequent_probabilities:
    :param word:
    :return:
    """
    return subsequent_probabilities[word]


def previous_word_candidates(previous_probabilities, word):
    """
    Return the list of candidates
    :param previous_probabilities:
    :param word:
    :return:
    """

    return previous_probabilities[word]


def best_candidate(previous_probabilities, subsequent_probabilities, prev_word, sub_word):
    """

    :param previous_probabilities:
    :param subsequent_probabilities:
    :param prev_word:
    :param sub_word:
    :return:
    """

    # Get list of word class tags
    tagdict = load('help/tagsets/upenn_tagset.pickle')
    tags = []
    for tag in tagdict.keys():
        if tag != '$' and tag != '.' and tag != ',' and tag != '(' and tag != ')' and tag != ':' \
                and tag != '--' and tag != "''":
            tags.append(tag)
    print(tags)

    # Determine permitted tag list
    permitted_tags_sub = defaultdict(list)
    for tag in tags:
        if tag[0] == 'N' or tag == 'DT':
            permitted_tags_sub['DT'].append(tag)
    print(permitted_tags_sub)

    permitted_tags_prev = defaultdict(list)
    for tag in tags:
        if tag != 'PRP':
            permitted_tags_prev['VBZ'].append(tag)
    print(permitted_tags_prev)

    # Determine word classes of prev_word and sub_word
    prev_word = pos_tag(prev_word.split(' '))
    sub_word = pos_tag(sub_word.split(' '))
    print(prev_word, sub_word)

    # Determine the list of probable candidates derived from prev_word with their probability and their word class
    prev_candidates = subsequent_probabilities[prev_word[0][0]]
    prev_candidates = sorted(prev_candidates.items(), key=lambda x: x[1])
    prev1 = {}
    for tup in prev_candidates:
        prev1[tup[0]] = []
        prev1[tup[0]].append(tup[1])

    word_class = []
    for k in prev1.keys():
        word_class.append(pos_tag(k.split(' ')))

    for w_class in word_class:
        prev1[w_class[0][0]].append(w_class[0][1])
    print('Prev: ', prev1)

    # Determine the list of probable candidates derived from sub_word with their probability and their word class
    sub_candidates = previous_probabilities[sub_word[0][0]]
    sub_candidates = sorted(sub_candidates.items(), key=lambda x: x[1])
    sub1 = {}
    for tup in sub_candidates:
        sub1[tup[0]] = []
        sub1[tup[0]].append(tup[1])

    word_class = []
    for k in sub1.keys():
        word_class.append(pos_tag(k.split(' ')))

    for w_class in word_class:
        sub1[w_class[0][0]].append(w_class[0][1])
    print('Sub: ', sub1)

    # Check for permitted word classes depending upon prev_word and sub_word
    tags_allowed_prev = permitted_tags_sub[prev_word[0][1]]

    permitted_candidates_prev = {}
    for key, value in prev1.items():
        if prev1[key][1] in tags_allowed_prev:
            permitted_candidates_prev[key] = value
        else:
            pass
    permitted_candidates_prev = sorted(permitted_candidates_prev.items(), key=lambda x: x[1])
    print('PER_PREV: ', permitted_candidates_prev)

    tags_allowed_sub = permitted_tags_prev[sub_word[0][1]]

    permitted_candidates_sub = {}
    for key, value in sub1.items():
        if sub1[key][1] in tags_allowed_sub:
            permitted_candidates_sub[key] = value
        else:
            pass
    permitted_candidates_sub = sorted(permitted_candidates_sub.items(), key=lambda x: x[1])
    print('PER_SUB: ', permitted_candidates_sub)

    # Check for any cross over between the two candidate lists
    crossovers = {}
    for word in permitted_candidates_prev:
        for word1 in permitted_candidates_sub:
            if word[0] == word1[0]:
                crossovers[word[0]] = word[1][0]
    print(crossovers)

    best_match = ''
    for k, v, in crossovers.items():
        if v == max(crossovers.values()):
            best_match = k
    print(best_match)

    return best_match
