-------------------------------------------------------------
-BigramGeneration - Python Program for Bigram Token Analysis-
-Author: Paramjit Raloowall                                 -
-------------------------------------------------------------

This program reads input text or a text file, generates bigram tokens, with their frequency counts.
Optionally, it displays a histogram to visualize the frequency of each bigram. Default is enabled
Longer filenames are treated as simple strings to avoid any file character limit failures

--------------------------
Assumptions
--------------------------
Numerical value are part of the Bigram generation, "1235 street" is valid token
word's split is based on default split behavior of the python

-------------------------
How to Use (Command Line)
-------------------------
Note, python is installed as 'python' argument if python is installed as python3 modify the usage accordingly

python bigram_generator.py [input_text_or_filename] [word_limit] [enable_histogram]

Arguments:
----------
1. input_text_or_filename (optional):
   - Path to a .txt file OR a raw string of text.
   - If the argument matches a valid file, the file contents are read.
   - Otherwise, it is treated as raw input text.
   - If not provided, default sample text will be used.

2. word_limit (optional):
   - Maximum number of words to consider for bigram generation.
   - Defaults to 50.

3. enable_histogram (optional):
   - Whether to show a histogram plot.
   - Accepts "true", "false", "1", "0", "yes", "no".
   - Defaults to "true".

Example Usages:
---------------
1. Run with default text:
   python bigram_generator.py

2. Run with a file:
   python bigram_generator.py training.en 100 true
   training.en file is included

3. Run with raw input and disable histogram:
   python bigram_generator.py "The rain in Spain stays mainly in the plain" 20 false


-----------------------
Features & Functionality
-----------------------

✓ Generates bigrams as space-separated strings (e.g., "quick brown").
✓ Outputs a dictionary of bigram counts.
✓ Limits analysis to the first N words (default: 50).
✓ Cleans text to remove punctuation and normalize case.
✓ Optionally plots a horizontal histogram using matplotlib.
✓ Handles both raw string input and text files gracefully.
✓ Debug mode prints internal structures for transparency.

---------------
Program Structure
---------------

Class: BigramGeneration
- clean_text(text): Cleans input text by return only characters and numbers and lowering case.
- generate_bigrams_tokens(text): Returns a list of bigram strings.
- bigram_get_token_with_counts(text): Returns a dictionary of bigram → count.
- parse_bigrams_from_text(text_input): Handles file or text input and triggers the analysis and outputs.
- plot_histogram(): Displays histogram of bigram frequency.

----------
Dependencies
----------
- Python 3.12 or higher
- matplotlib

Install matplotlib default is needed:
> pip install matplotlib

------------
Output Example
------------
the quick: 2
quick brown: 1
brown fox: 1
...

Also displays a bar chart (if histogram is enabled).

