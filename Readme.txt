The bigram generation can be run by bigram.py "your text file or input"
The bigram tests can be run by the bigramTests.py

**Histogram**
The program also generates a visual representation of histogram and dependency must be installed
I am using pip installer to install libraries
    -- pip install matplotlib

if you don't want to install the visual matplotlib library please comment line 59 in bigram.py (plot_histogram(counts))

**Note**
    --Special care has been taken to leverage built-in libraries rather than reinventing functionality.
    --word split is based on the space character ' '
**ASSUMPTION**
    --By default, the program can process up to 50 words.
    --This limit is defined by a constant (WORD_SIZE_LIMIT:int =5000),
    --which you can modify if you need to handle a larger input;
    --however, the program is designed to work within this default cap.
    --Longer filenames are treated as simple strings

##Pre-requisites
- **Python Version**
    - [Version 3.12 or higher]
- **Dependencies**
    -[matplotlib] https://matplotlib.org
    - install by using pip install matplotlib
