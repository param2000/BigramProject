-------------------------------------------------------------
-BigramGeneration - Python Program for Bigram Token Analysis-
-Author: Paramjit Raloowall                                 -
-------------------------------------------------------------

This program reads input text or a text file, generates bigram tokens with their frequency counts, and optionally displays a histogram to visualize the frequency of each bigram. By default, histogram generation is enabled.
Longer filenames are treated as simple strings to avoid any file character limit issues.

--------------------------
Assumptions
--------------------------
- Numerical values are part of the bigram generation, e.g., "1235 street" is a valid token.
- Word splitting is based on Python’s default string split behavior.
- Special characters are removed before bigram generation.
- All text is converted to lowercase (as shown in the examples).
- Unicode characters are supported (e.g., Café).
-must supply word-size to parse everything as size is restriction to make sure timely output and reasonable histogram display happens


-------------------------
How to Use (Command Line)
-------------------------
Note: The program uses argparse for a robust CLI. If Python is installed as 'python3' instead of 'python', adjust the usage accordingly.

Basic usage:
   python bigram_generator.py [input_text_or_filename] [--word-size WORD_SIZE] [--histogram {true,false}] [--debug]

Arguments:
----------
1. input_text_or_filename (positional, optional):
   - Path to a .txt file OR a raw string of text.
   - If the argument corresponds to an existing file, its contents will be read.
   - Otherwise, it is treated as raw input text.
   - If not provided, a default sample text is used.

2. --word-size (optional):
   - Maximum number of words to consider for bigram generation.
   - Defaults to 50.
   - Example: --word-size 100

3. --histogram (optional):
   - Enable or disable the histogram plot.
   - Accepts "true", "false", "1", "0", "yes", or "no".
   - Defaults to "true".
   - Example: --histogram false

4. --debug (optional):
   - Enable debug output for additional internal process details.
   - Simply include the flag if debugging is desired.
   - Example: --debug

Example Usages:
---------------
1. Run with default text (no arguments):
   python BigramGeneration.py

2. Run with a file:(Here, the file "training.en" is used as input.)
   python BigramGeneration.py training.en --word-size 100 --histogram true


3. Run with raw input text and disable histogram:
   python BigramGeneration.py "The rain in Spain stays mainly in the plain" --word-size 20 --histogram false

4. Run with debug mode enabled:
   python BigramGeneration.py "Your sample text here" --debug

5. Run all of argument together
   python BigramGeneration.py training.en --word-size 1000 --histogram yes --debug
-----------------------
Features & Functionality
-----------------------

✓ Generates bigrams as space-separated strings (e.g., "quick brown").
✓ Outputs a dictionary of bigram counts.
✓ Limits analysis to the first N words (default: 50).
✓ Cleans text by removing punctuation, handling hyphens, and normalizing case.
✓ Optionally plots a horizontal histogram using matplotlib.
✓ Processes both raw string input and text file contents gracefully.
✓ Debug mode prints internal structures for transparency.

---------------
Program Structure
---------------

Class: BigramGeneration
- clean_text(text): Cleans the input text (removes extra punctuation, splits hyphenated words, converts to lowercase).
- generate_bigrams_tokens(text): Returns a list of bigram strings.
- bigram_get_token_with_counts(text): Returns a dictionary mapping each bigram to its frequency count.
- parse_bigrams_from_text(text_input): Determines whether the input is a file or raw text, then performs analysis.
- plot_histogram(): Displays a histogram of the bigram frequencies using matplotlib.

----------
Dependencies
----------
- Python 3.12 or higher
- matplotlib

To install matplotlib, run:
   pip install matplotlib

------------
Output Example
------------
For a sample input, the program outputs bigrams and their counts, e.g.:

   the quick: 2
   quick brown: 1
   brown fox: 1
   ...

Additionally, if histogram generation is enabled, a bar chart of the bigram frequencies is displayed.

----------------
Unit Testing
----------------
To run unit tests (with histogram suppressed), use the following command:
   python TestBigramGeneration.py -v
