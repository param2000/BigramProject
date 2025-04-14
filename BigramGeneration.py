import re
import sys

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
        self.bigram_token_frequency: dict[str:int]={}
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
        temp = inputtext.lower().replace('-', ' ')
        temp=re.sub(r'[^\w\s]', '', temp, flags=re.UNICODE)

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

    # Get input text from command line if provided; otherwise, use the default text.
    input_text = sys.argv[1] if len(sys.argv) > 1 else default_text

    # Get word size limit from command line or default to 50.
    try:
        word_size = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    except ValueError:
        print("Invalid word size limit; using default value of 50.")
        word_size = 50

    # Get histogram flag from command line or default to True.
    enable_histogram: bool = True
    if len(sys.argv) > 3:
        argv3 = sys.argv[3].strip().lower()
        if argv3 in ("true", "1", "yes"): enable_histogram = True
        if argv3 in ("false", "0", "no"): enable_histogram = False

    # Create an instance of BigramGeneration.
    bigram_generator = BigramGeneration(debug=False, word_size=word_size, histogram_generation = enable_histogram)

    # Parse bigrams from the input text.
    counts = bigram_generator.parse_bigrams_from_text(input_text)

    # Print the bigrams and their counts.
    print(bigram_generator)

