import re
import sys
from collections import Counter
import matplotlib.pyplot as plt

debug = True

def clean_text(text):
    # Lowercase and remove non-alphabetic characters except spaces
    temp = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    print(temp)
    return re.sub(r'[^a-zA-Z\s]', '', text.lower())

def generate_bigrams(text):
    words = clean_text(text).split()
    bigrams = []
    #genrate the bigrams
    for i in range(len(words) - 1):
        bigrams.append(words[i] + ' ' + words[i + 1])
    return bigrams


def bigram_histogram(text):
    bigrams = generate_bigrams(text)

    if debug: print(bigrams)

    bigram_counts = Counter(bigrams)
    return bigram_counts


def plot_histogram(bigram_counts):
    labels, values = zip(*bigram_counts.items())
    plt.figure(figsize=(10, 7))
    plt.barh(labels, values)
    plt.xlabel("Frequency")
    plt.ylabel("Bigrams(n=2)")
    plt.title("Bigram Frequency Histogram")
    plt.tight_layout()
    plt.show()


def analyze_text_source(source):
    if isinstance(source, str):
        try:
            with open(source, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            text = source  # Treat input as plain text
    else:
        raise ValueError("Input must be a string path or plain text")

    counts = bigram_histogram(text)
    plot_histogram(counts)
    return counts


# Testing
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = "The quick brown fox and the quick blue hare."

    counts = analyze_text_source(input_text)
    for bigram, count in counts.items():
        print(f"{bigram}: {count}")
