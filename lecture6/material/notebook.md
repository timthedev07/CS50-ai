# Language

some common tasks using Natural Language Processing:
- automatic summarization
- information extraction
- language identification
- machine translation
- named entity recognition
- speech recognition
- text classification
- word sense disambiguation , where the AI needs to choose the right meaning of a word that has multiple meanings (e.g. bank means both a financial institution and the ground on the sides of a river).

## **Syntax and Semantics**
**Syntax** is the structure of a sentence, where different parts of the sentence somehow together construct a grammatically well formed sentence.

**Semantics** is the meaning of words in a sentence. While the sentence “Just before nine o’clock Sherlock Holmes stepped briskly into the room” is syntactically different from “Sherlock Holmes stepped briskly into the room just before nine o’clock,” their content is effectively identical, so their overall meaning is the same but the structures are different. 
Some phrases might be entirely syntactically correct, but are completely nonsensical. For instance, the sentence: `Colorless green ideas sleep furiously`.

## **Context-Free Grammar**

### ***Formal grammar***
A system of rules for generating sentences in a language

Consider this simple, valid, and well formed sentence:

```py
she        saw        the        city
```
The words shown above are **terminal symbols**, those are what we ultimately care about generating. But each of the words is going to be associated with a **non-terminal symbol**(we use non-terminal symbols to get terminal symbols), for example, the simple sentence above might be translated to:

```py
N(oun)    V(erb)   D(eterminer)    N(oun)
she        saw        the           city
```

### ***Rewriting rules***
```py
P == Preposition
NP = noun phrase
VP = verb phrase
S = sentence

N -> she | Ken | car | city | ... 
D -> the | a | an | those | ... 
V -> saw | ate | procrastinate | talk | ... 
P -> to | over | below | on | ... 
ADJ -> relevant | dumb | charming | old | ... 

# advanced ones
NP -> N | DN
VP -> V | V NP
S -> NP VP
AP -> A | A AP
PP -> P | NP
```

An example of noun phrase:
```python
        NP
        ʌ
       / \
      D   N
      |   |
     the city
```

An example of verb phrase:
```python
        NP
      /    \
     /      \
    V       NP
    |       /\
   saw     /  \
         the  city
```

In our case, she saw the city would be:

<img src="assets/syntactictree.png" width="400">

A more complex example containing adjective and prepositional phrases:

```bash
         S                      
  _______|___                    
 |           VP                 
 |    _______|____               
 |   |            NP            
 |   |    ________|___           
 |   |   |            NP        
 |   |   |         ___|_____     
 |   |   |        AP        |   
 |   |   |    ____|___      |    
 NP  |   |   |        AP    NP  
 |   |   |   |        |     |    
 N   V   D   A        A     N   
 |   |   |   |        |     |    
she saw the blue     wide street
```

## **n-grams**
a contiguous sequence of *n* items from a sample of text

### ***character n-gram***
a contiguous sequence of *n* characters from a sample of text

### ***word n-gram***
a contiguous sequence of *n* words from a sample of text

### ***Unigram***
A contiguous sequence of 1 item from a sample text

### ***Bigram***
A contiguous sequence of 2 item from a sample text

### ***Trigram***
A contiguous sequence of 3 item from a sample text

In this sentence:

“How often have I said to you that when you have eliminated the impossible whatever remains, however improbable, must be the truth?

The first three trigrams are ***How often have***, ***often have I***, and ***have I said***.

## **Tokenization**
The task of splitting a sequence of characters into pieces(tokens)

# **Markov Models**

As discussed in previous lectures, Markov models consist of nodes, the value of each of which has a probability distribution based on a finite number of previous nodes. Markov models can be used to generate text. To do so, we train the model on a text, and then establish probabilities for every n-th token in an n-gram based on the n words preceding it. For example, using trigrams, after the Markov model has two words, it can choose a third one from a probability distribution based on the first two. Then, it can choose a fourth word from a probability distribution based on the second and third words. To see an implementation of such a model using `nltk`, refer to generator.py in the source code, where our model learns to generate Shakespeare-sounding sentences. Eventually, using Markov models, we are able to generate text that is often grammatical and sounding superficially similar to human language output. However, these sentences lack actual meaning and purpose.

## **Text categorization & Bag-of-Words Model**
- Bag-of-words is a model that represents text as an unordered collection of words.
- This model ignores syntax and considers only the meanings of the words in the sentence.
- This approach is helpful in some classification tasks, such as sentiment analysis (another classification task would be distinguishing regular email from spam email). 
- Sentiment analysis can be used, for instance, in product reviews, categorizing reviews as positive or negative.

Consider the following reviews on some product:

- “My grandson loved it! So much fun!”
- “Product broke after a few days.”
- “One of the best games I’ve played in a long time.”
- “Kind of cheap and flimsy, not worth it.”

As a human, we know that two of the sentences are positive and the others are negative because of the words that show up in the text(fun, loved, best & broke cheap, flimsy).

## **Naive Bayes**
Naive Bayes is a very popular technique often used in sentiment analysis of Bag-of-Words models. It is based on the Bayes rule of probability:

<img src="assets/bayesrule.png" width="500">

In the case of analyzing the reviews, we would like to calculate the probability of negative and probability of positive.

For example, say, we are trying to figure out the probability that the first review shown above is positive(represented using the emoji)
```
P(😀 | "")
```