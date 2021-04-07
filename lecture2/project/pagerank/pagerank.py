import os
import random
import re
import sys
from random import choices, choice
from copy import deepcopy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus:dict, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # get the number of pages in corpus
    N = len(corpus)

    # if no out going links
    if len(corpus[page]) < 1:
        return dict().fromkeys(corpus.keys(), 1 / N)
    # set up a dictionary that is going to be returned, 
    # where initially, each page has a probability of (1 - damping_factor) / N
    res = dict().fromkeys(corpus.keys(), (1 - damping_factor) / N)
    
    # iterating over all of the possible links to go next
    for nextPossibleDestination in corpus[page]:
        res[nextPossibleDestination] += damping_factor / len(corpus[page])
    # check if the values of the probability distribution sum to 1(or really close)
    assert abs(sum(res.values()) - 1) < 0.0001
    return res


def sample_pagerank(corpus:dict, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # get all of the pages in a corpus
    pages = list(corpus.keys())

    # setting up a dictionary for counting the occurrences
    count = {}.fromkeys(pages, 0)

    # setting the first example to a random page
    sample = random.choice(pages)
    count[sample] += 1

    # set up the distribution dictionary to be returned, all values are initially 0
    distribution = {}.fromkeys(pages, 0)

    
    
    # iterate over the range 1 to n since we have already generated the first sample
    for i in range(1, n):

        # get the transition model based on the previous sample
        model = transition_model(corpus, sample, damping_factor)

        # generate the next sample based on the transition model
        sample = choices(
            population=list(model.keys()),
            weights=list(model.values()),
        )[0]
        
        if i % 600 == 0:
            print()
            print("Model")
            for key, value in model.items():
                print(f"{key} | {value}")
            print(f"Random choices parameters:\nCandidates: {list(model.keys())}\nWeights: {list(model.values())}")
        count[sample] += 1


    print(count)
    distribution = {key:value/n for key, value in count.items()}
    assert abs(sum(count.values()) - n) < 0.0001
    return distribution

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Getting total number of pages
    N = len(corpus)

    # Setting up a rank where initially each page has the same probability
    rank = {}.fromkeys(list(corpus.keys()), 1/N)

    # defining the threshold
    threshold = 0.00001

    # defining a constant expression
    HELPER_EXPRESSION = (1-damping_factor)/N

    # setting done to false so the while loop starts
    done = False

    while not done:
        done = False
        prev_rank = deepcopy(rank)
        for page in corpus:
            Sum = 0
            for p in corpus:
                if page in corpus[p]:
                    Sum += rank[p] / len(corpus[p])
            rank[page] = HELPER_EXPRESSION + damping_factor * Sum
            done = abs(prev_rank[page] - rank[page]) < threshold

    return rank


    


if __name__ == "__main__":
    main()
