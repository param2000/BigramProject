import re
import sys
from collections import Counter
from matplotlib import pyplot as plt



class BigramGeneration:
    def __init__(self, debug:bool = False, word_size:int =10):
        self.bigram_counts:dict[str:int]={}

        self.debug = debug
        self.WORD_SIZE_LIMIT:int = word_size

    def __str__(self):
        for bigram, count in self.bigram_counts.items():
            print(f"{bigram}: {count}")


    def clean_text(self,text:str) -> str:
        """ return string after cleanup [sub string]"""
        # Lowercase and remove non-alphabetic characters except spaces
        temp = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        #if self.debug: print (temp)
        return temp

    def generate_bigrams(self, text:str)->list[str]:
        """Bigram Generation, return list of string {'one two'}"""

        words = self.clean_text(text).split()
        restricted_length = words[:self.WORD_SIZE_LIMIT]
        length_of_word_list: int = len(words)
        bigrams = []

        if length_of_word_list >= self.WORD_SIZE_LIMIT:
            print(f"This program will only handle first {self.WORD_SIZE_LIMIT} words for Bigram generation ")

        #genrate the bigrams
        for i in range(len(restricted_length) - 1):
            bigrams.append(restricted_length[i] + ' ' + restricted_length[i + 1])

        return bigrams


    def bigram_with_counts(self, text:str)->dict[str:int]:
        """ return type: dictionary with bigram and count value {"one  two":1} """
        bigrams = self.generate_bigrams(text)

        #generate the dictionary pairs with counts
        #bigram_counts = Counter(bigrams)

        for bigram in bigrams:
            if bigram in self.bigram_counts:
                self.bigram_counts[bigram]+=1
            else:
                self.bigram_counts[bigram]=1

        #debugging info
        if self.debug:
            #print(bigrams)
            print(self.bigram_counts)
        return self.bigram_counts


    def analyze_text_source(self, source:str) -> dict[str:int]:
        if isinstance(source, str):
            try:
                with open(source, 'r') as f:
                    text = f.read()
            except FileNotFoundError:
                text = source  # Treat input as plain text
        else:
            raise ValueError("Input must be a string path or plain text")

        #get bigrams
        bigram_dic_with_counts  = self.bigram_with_counts(text)

        #if self.debug: print(bigram_dic_with_counts)

        return bigram_dic_with_counts

    def plot_histogram(self):
        labels, values = zip(*self.bigram_counts.items())
        plt.figure(figsize=(10, 7))
        plt.barh(labels, values)
        plt.xlabel("Frequency")
        plt.ylabel("Bigrams(n=2)")
        plt.title("Bigram Frequency Histogram")
        plt.tight_layout()
        plt.show()


# Testing/usage
if __name__ == "__main__":
    "Please note that words limit is in place"
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        #input_text = "The quick brown fox and the quick blue hare."
        input_text = "training.en"

    bigram_generator = BigramGeneration(debug=True,word_size= 50)

    counts = bigram_generator.analyze_text_source(input_text)
    for bigram, count in counts.items():
        print(f"{bigram}: {count}")

    bigram_generator.plot_histogram()
