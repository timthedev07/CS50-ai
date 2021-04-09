import nltk
import sys
from string import punctuation, digits, whitespace


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""



NONTERMINALS = """
S -> N V | NP VP | S Conj NP VP | S Conj VP |
CN -> N N | N CN
NP -> N | AP NP | Det N P N | Det Adj N | Det N | Det N Adv
NP -> Det AP Adj N P NP P NP| 


VP -> V | V N | V NP | V PP | V PP NP | V NP | Adv V NP | V Adv
VP -> V NP PP | P NP


PP -> P NP | P
AP -> Adj | Adj AP
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # split, turn into lowercase, and remove unnecessary word
    words = ''.join([c.lower() for c in sentence if c not in punctuation + digits])

    return nltk.word_tokenize(words)
    


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # get all subtrees of the tree applying the filter `validChunk`(see below)
    res_chunks = [i for i in tree.subtrees(validChunk)]

    return res_chunks
    
def validChunk(tree:nltk.tree.Tree):
    """
    Checks whether a chunk is a valid chunk(itself must be a NP and not have any other NP subtrees)
    """
    # if the tree itself is not a noun phrase
    if tree.label() != "NP":
        return False

    # iterate over the subtrees of the given tree
    for subtree in tree.subtrees(lambda x:x!=tree):

        # if any subtree is a noun phrase
        if subtree.label() == "NP":
            return False

        # if ant subtree of the current subtree is a NP
        for deep_subtree in subtree.subtrees(lambda x:x!=subtree):
            if deep_subtree.label() == "NP":
                return False
    
    # if all checks are passed
    return True
    
if __name__ == "__main__":
    main()
