import nltk
import sys
import os
import math
from string import punctuation, ascii_lowercase 


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
    for fname in [os.path.join(directory, i) for i in os.listdir(directory)]:
        with open(fname, "r") as txtFile:
            entries[fname[len(directory) + 1:]] = txtFile.read()
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
        if c.lower() in ascii_lowercase + ' ':
            words += c.lower()
    # tokenize
    words = nltk.word_tokenize(words)
    res = []
    for word in words:
        if word not in nltk.corpus.stopwords.words("english"):
            res.append(word)
    print(res)
    return words
   
def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    res = dict()
    seen = set()
    TOTAL_DOCUMENTS = len(documents)
    for document, text in documents.items():
        for word in text:
            if word not in seen:
                numDocumentsContainingWord = 0
                for x, y in documents.items():
                    if x != document and word in y:
                        numDocumentsContainingWord += 1
                res[word] = math.log(TOTAL_DOCUMENTS / numDocumentsContainingWord)
                seen.add(word)
    
    return res

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
