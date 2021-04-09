import nltk
import sys
import os
import math
from string import punctuation, ascii_lowercase, digits



FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    entries = dict()
    for fname in [i for i in os.listdir(directory)]:
        with open(os.path.join(directory, fname), "r") as txtFile:
            entries[fname] = txtFile.read()
    return entries



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = ''

    # remove non-alphabetical values
    for c in document:
        if c.lower() in ascii_lowercase + ' ' + digits:
            words += c.lower()
    # tokenize
    words = nltk.word_tokenize(words)
    res = []

    # filter out the punctuations and stopwords
    for word in words:
        if word not in nltk.corpus.stopwords.words("english") and word not in punctuation:
            res.append(word)

    return res
   

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # set a the dictionary that is going to be returned
    res = dict()

    # store words already seen
    seen = set()

    # get the total number of documents
    TOTAL_DOCUMENTS = len(documents)

    # iterate over the text in documents
    for text in documents.values():

        # iterate over every single word in the document
        for word in text:

            # if word not yet seen
            if word not in seen:

                    # compute the idf value
                # getting NumDocumentsContaining(word)
                numDocumentsContainingWord = 0
                for y in documents.values():
                    if word in y:
                        numDocumentsContainingWord += 1
                # apply formula
                res[word] = math.log(TOTAL_DOCUMENTS / numDocumentsContainingWord)

                # add to seen
                seen.add(word)
    
    return res

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # declare a dictionary where the keys are file names, and each of the 
    # values is list of words in the query that also appear in the file
    intersections = dict()
    
    # iterate over the documents
    for document, words in files.items():

        # declare empty list
        buffer = []

        # for each word in query
        for qword in query:

            # if word is also in the current document
            if qword in words:

                # append that to the buffer
                buffer.append(qword)
        # push to the dictionary
        intersections[document] = buffer
    
    # a dictionary with filenames corresponding to their tf-idf values
    score = dict()

    # again iterate over the files
    for document, words in files.items():
        # setting current score to 0
        curr_score = 0 


        # iterate over the intersecting words
        for word in intersections[document]:
            tf = term_frequency(words, word)
            
            # compute tfidf value and add it to total score for current document
            curr_score += tf * idfs[word]
        # print(f"Score for document <{document}>: <{curr_score}>")
        score[document] = curr_score
    
    # sort the scores
    rank = dict(sorted(score.items(), key=lambda pair: pair[1], reverse=True))
    k = 0

    res = []

    for i in rank:
        if k >= n:
            break
        # yield i
        res.append(i)
        k += 1
    return res

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # declare a dictionary where the keys are sentence, and each of the 
    # values is list of words in the query that also appear in the sentence
    intersections = dict()
    
    # iterate over the sentences
    for sentence, word_list in sentences.items():

        # declare empty list
        buffer = []

        # for each word in query
        for qword in query:

            # if word is also in the current sentence
            if qword in word_list:

                # append that to the buffer
                buffer.append(qword)
        
        # push to the dictionary
        intersections[sentence] = buffer

    # a dictionary with sentences corresponding to their tf-idf values
    score = dict()

    # again iterate over the sentences
    for sentence, word_list in sentences.items():
        # setting current score to 0
        curr_score = 0 

        # iterate over the intersecting words
        for word in intersections[sentence]:

            # compute tfidf value and add it to total score for current document
            curr_score += idfs[word]
        score[sentence] = curr_score

    # sort the scores
    rank = dict(sorted(score.items(), key=lambda pair: pair[1], reverse=True))

    # get max score
    max_score = list(rank.values())[0]

    # if there is a tie
    if max_score == list(rank.values())[1]:
        new_partial_rank = dict()
        # compute query term density for every sentence that has the max score(in the tie)
        tie_items = 0
        for key, value in rank.items():
            if value == max_score:
                new_score = len([j for j in sentences[key] if j in query]) / len(sentences[key])
                new_partial_rank[key] = new_score
                tie_items += 1
        # sort to get new partial rank
        new_partial_rank = dict(sorted(new_partial_rank.items(), key=lambda pair: pair[1], reverse=True))
        # replace
        b = new_partial_rank.__len__()
        old_rank = rank.copy()
        rank = dict()
        new_keys = list(new_partial_rank.keys())
        new_values = list(new_partial_rank.values())
        old_keys = list(old_rank.keys())
        old_values = list(old_rank.values())

        for key, value in old_rank.items():
            if value > 0:
                print(f"{key[:25]} : {value}")

        for i in range(b):
            rank[new_keys[i]] = new_values[i]
            print(f"ok: {rank[new_keys[i]]} | {new_values[i]}")
        for i in range(len(old_rank) - b):
            rank[old_keys[i]] = old_values[i]
    print("="*100)
    print("="*100)
    print("="*100)

    for key, value in rank.items():
        if value > 0:
            print(f"{key[:25]} : {value}")

    k = 0

    res = []

    for i in rank:
        if k >= n:
            break
        # yield i
        res.append(i)
        k += 1
    return res

def term_frequency(text, word):
    """
    Compute the term frequency of `word` in the document `text`
    text: `list` or `tuple` or `set`
    word: `str`
    """
    f = 0
    for i in text:
        if word == i:
            f += 1
    return f


if __name__ == "__main__":
    main()
