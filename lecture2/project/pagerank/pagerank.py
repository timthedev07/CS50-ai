import os
import random
import re
import sys
from random import choices
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
    num_p = len(corpus)
    # set up a dictionary that is going to be returned
    res = dict()
    for iPage in corpus:

        # Divide 1 - d among all pages
        pageRank = (1 - damping_factor) / num_p

        # If no connections, add eq probability
        if len(corpus[page]):
            if iPage in corpus[page]:
                pageRank += damping_factor / len(corpus[page])
        else:
            pageRank += damping_factor / num_p
        res[iPage] = pageRank

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
    # gets all of the pages in a corpus
    pages = list(corpus.keys())
    # setting the first example to a random page
    prev_sample = random.choice(pages)
    # setting up a list for all samples
    data = []
    # append the first generated sample to the list
    data.append(prev_sample)

    # set up the distribution dictionary to be returned, all values are initially 0
    distribution = {}.fromkeys(pages, 0)

    # iterate over the range 1 to n since we have already generated the first sample
    for i in range(1, n):
        # get the transition model based on the previous sample
        model = transition_model(corpus, prev_sample, damping_factor)
        # generate the next sample based on the transition model
        next_sample = choices(list(reversed(sorted(model.keys()))), weights=tuple(model.values()))[0]
        
        # append that sample to the list previously setted up.
        data.append(next_sample)

        # set the prev sample to the current sample for the next iteration
        prev_sample = next_sample
    
    # setting up a dictionary 
    count = {}
    # count the occurrences
    for i in data:
        if i not in count:
            count[i] = 1
        else:
            count[i] += 1
    distribution = {key:count[key]/n for key in count}
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
    # defining threshold
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
