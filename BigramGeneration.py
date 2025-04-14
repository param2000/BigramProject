import argparse
import re
import sys
import os

from matplotlib import pyplot as plt

class BigramGeneration:
    bigram_token_frequency: dict[str, int]
    debug: bool
    WORD_SIZE_LIMIT: int
    enable_histogram_generation: bool
    FILENAME_LIMIT: int
    input_text :str

    def __init__(self, debug:bool = False, word_size:int =50, histogram_generation=True):
        self.input_text:str = ''
        self.bigram_token_frequency: dict[str, int]={}
        self.FILENAME_LIMIT = 255
        self.debug = debug
        self.WORD_SIZE_LIMIT = word_size
        self.enable_histogram_generation = histogram_generation

    def __str__(self):
        output_lines = [f"{bigram}: {count}" for bigram, count in self.bigram_token_frequency.items()]
        return "\n".join(output_lines)


    def clean_text(self, inputtext:str) -> str:
        """ return string after cleanup [sub string]"""
        # Lowercase and remove non-alphabetic characters except spaces
        #temp = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        #temp = inputtext.lower().replace('-', ' ')
        #temp=re.sub(r'[^\w\s]', '', temp, flags=re.UNICODE)

        #Replace hyphens that occur between word characters only.
        temp = re.sub(r'(?<=\w)-(?=\w)', ' ', inputtext.lower())
        temp = re.sub(r'[^\w\s]', '', temp, flags=re.UNICODE)

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


    def bigram_get_token_with_counts(self, text:str) -> dict[str:int]:
        """ return type: dictionary with bigram and count value {"one  two":1} """
        bigrams = self.generate_bigrams_tokens(text)

        #generate the dictionary pairs with counts
        #bigram_counts = Counter(bigrams)
        self.bigram_token_frequency = {}

        for bigram in bigrams:
            if bigram in self.bigram_token_frequency:
                self.bigram_token_frequency[bigram]+=1
            else:
                self.bigram_token_frequency[bigram]=1

        #debugging info
        if self.debug:
            #print(bigrams)
            print(self.bigram_token_frequency)


        if self.enable_histogram_generation:
            self.plot_histogram()


        return self.bigram_token_frequency

    def parse_bigrams_from_text(self, text_input: str) -> dict[str, int]:
        """Analyze the input text to generate bigram tokens
            if the input_text is a path present for am existing file then the file will be read for input_text
            Otherwise input_text is assumed to be a simple raw text input.
        """

        if not isinstance(text_input, str):
            raise ValueError("Input must be a string path or plain text")

        if os.path.exists(text_input):
            with open(text_input, 'r', encoding='utf-8') as f:
                self.input_text = f.read()
        else:
            self.input_text = text_input


        return self.bigram_get_token_with_counts(self.input_text)

    def plot_histogram(self):
        #tokens = self.bigram_token_frequency.keys()
        #values = self.bigram_token_frequency.values()

        # Sort items by frequency (highest first)
        sorted_items = sorted(self.bigram_token_frequency.items(), key=lambda item: item[1], reverse=True)
        tokens, values = zip(*sorted_items)

        # Dynamically adjust the figure height based on the number of tokens
        #todo figure the large data set display
        # Adjust the multiplier (e.g., 0.15) as needed for readability.
        #fig_height = 1 + len(tokens) * 0.15

        plt.figure(figsize=(16, 12))
        plt.barh(range(len(tokens)), values, tick_label=tokens)
        plt.xlabel("Frequency")
        plt.ylabel("Bigrams (n=2)")
        plt.title("Bigram Token Frequency Histogram")
        # Invert y-axis so the highest frequency is at the top.
        #plt.gca().invert_yaxis()
        # Adjust the font size of y-tick labels for better readability.
        plt.yticks(fontsize=5)
        plt.tight_layout()
        plt.show()


# Testing/usage
if __name__ == "__main__":
    # Default text if no input provided via command line.
    default_text = (
        "The quick brown fox and the quick blue hare. I would like your advice about Rule 143 concerning inadmissibility. "
        "My question relates to something that will come up on Thursday and which I will then raise again. "
        "The Cunha report on multiannual guidance programmes comes before Parliament on Thursday and contains a proposal in paragraph 6 "
        "that a form of quota penalties should be introduced for countries which fail to meet their fleet reduction targets annually. "
        "It says that this should be done despite the principle of relative stability."
    )
    parser = argparse.ArgumentParser(description="Bigram Generation Program")
    parser.add_argument("input_text", nargs="?", default=default_text,
                        help="Input text or file path to parse for bigrams.")
    parser.add_argument("--word-size", type=int, default=50,
                        help="Word size limit for bigram generation (default: 50).")
    parser.add_argument("--histogram", type=str, default="true",
                        help="Enable histogram generation (true/false, 1/0, yes/no; default: true).")
    parser.add_argument("--debug", action="store_true", default=False,
                        help="Enable debug output.")
    args = parser.parse_args()

    # Convert the histogram flag to a boolean.
    enable_histogram = args.histogram.lower() in ("true", "1", "yes")

    # Create an instance of BigramGeneration.
    bigram_generator = BigramGeneration(debug=args.debug,
                                        word_size=args.word_size,
                                        histogram_generation=enable_histogram)

    # Parse and generate bigram counts from the given input.
    counts = bigram_generator.parse_bigrams_from_text(args.input_text)

    # Print the generated bigrams and their counts.
    print(bigram_generator)


