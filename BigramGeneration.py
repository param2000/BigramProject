import re
import sys
from collections import Counter
from matplotlib import pyplot as plt

class BigramGeneration:
    def __init__(self, debug:bool = False, word_size:int =50):
        self.input_text = ''
        self.bigram_counts:dict[str:int]={}
        self.FILENAME_LIMIT = 255
        self.debug = debug
        self.WORD_SIZE_LIMIT:int = word_size

    def __str__(self):
        for bigram, count in self.bigram_counts.items():
            print(f"{bigram}: {count}")


    def clean_text(self,text:str) -> str:
        """ return string after cleanup [sub string]"""
        # Lowercase and remove non-alphabetic characters except spaces
        temp = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        #if self.debug: print (temp)
        return temp

    def generate_bigrams_tokens(self, text:str) -> list[str]:
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


    def bigram_token_with_counts(self, text:str) -> dict[str:int]:
        """ return type: dictionary with bigram and count value {"one  two":1} """
        bigrams = self.generate_bigrams_tokens(text)

        #generate the dictionary pairs with counts
        #bigram_counts = Counter(bigrams)
        self.bigram_counts = {}

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

    def parse_bigrams_from_text(self, text_input: str) -> dict[str, int]:
        """
            Analyzes the input source to generate bigram counts.
            If `text_input` is a string with a length less than or equal to `self.FILENAME_LIMIT`, the method
            will attempt to open it as a file. If the file cannot be found, or if the input exceeds the limit,
            it will treat `text_input` as raw text. The text is then processed to generate a dictionary of bigram counts.
            :param text_input: A file path or a plain text string.
            :return: A dictionary with bigrams as keys and their occurrence counts as values.
            :raises ValueError: If the provided input is not a string.
        """
        if not isinstance(text_input, str):
            raise ValueError("Input must be a string path or plain text")

        # Attempt to treat text_input as a file if within the filename length limit.
        if len(text_input) <= self.FILENAME_LIMIT:
            try:
                with open(text_input, 'r', encoding='utf-8') as f:
                    self.input_text = f.read()
            except FileNotFoundError:
                self.input_text = text_input  # Fallback: treat as raw text if file not found.
        else:
            self.input_text = text_input

        return self.bigram_token_with_counts(self.input_text)

    def plot_histogram(self):
        tokens = self.bigram_counts.keys()
        values = self.bigram_counts.values()

        plt.figure(figsize=(10, 7))
        plt.barh(tokens, values)
        plt.xlabel("Frequency")
        plt.ylabel("Bigrams(n=2)")
        plt.title("Bigram Token Frequency Histogram")
        plt.tight_layout()
        plt.show()


# Testing/usage
if __name__ == "__main__":
    "Please note that words limit is in place"
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = """The quick brown fox and the quick blue hare. I would like your advice about Rule 143 concerning inadmissibility.
                    My question relates to something that will come up on Thursday and which I will then raise again.
                    The Cunha report on multiannual guidance programmes comes before Parliament on Thursday and contains a 
                    proposal in paragraph 6 that a form of quota penalties should be introduced for countries which fail to meet their fleet reduction targets annually.
                    It says that this should be done despite the principle of relative stability."""
        #input_text = "training.en"

    bigram_generator = BigramGeneration(debug=True,word_size= 50)

    counts = bigram_generator.parse_bigrams_from_text(input_text)
    for bigram, count in counts.items():
        print(f"{bigram}: {count}")

    bigram_generator.plot_histogram()
