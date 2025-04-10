from matplotlib import pyplot as plt


def plot_histogram(bigram_counts):
    labels, values = zip(*bigram_counts.items())
    plt.figure(figsize=(10, 7))
    plt.barh(labels, values)
    plt.xlabel("Frequency")
    plt.ylabel("Bigrams(n=2)")
    plt.title("Bigram Frequency Histogram")
    plt.tight_layout()
    plt.show()
