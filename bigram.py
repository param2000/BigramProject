import re
import sys
from collections import Counter
from bigram_plot import plot_histogram

debug = False

def clean_text(text):
    # Lowercase and remove non-alphabetic characters except spaces
    temp = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    if debug: print (temp)
    return temp

def generate_bigrams(text):
    words = clean_text(text).split()
    bigrams = []
    #genrate the bigrams
    for i in range(len(words) - 1):
        bigrams.append(words[i] + ' ' + words[i + 1])
    return bigrams


def bigram_with_counts(text):
    """
    :rtype: dictionary with bigram and count value
    """
    bigrams = generate_bigrams(text)

    if debug: print(bigrams)
    #generate the dictionary pairs with counts
    bigram_counts = Counter(bigrams)
    return bigram_counts


def analyze_text_source(source):
    if isinstance(source, str):
        try:
            with open(source, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            text = source  # Treat input as plain text
    else:
        raise ValueError("Input must be a string path or plain text")

    bigram_dic_with_counts  = bigram_with_counts(text)
    if debug: print(bigram_dic_with_counts)
    return bigram_dic_with_counts

# Testing
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = "The quick brown fox and the quick blue hare."

    counts = analyze_text_source(input_text)
    for bigram, count in counts.items():
        print(f"{bigram}: {count}")

    plot_histogram(counts)
