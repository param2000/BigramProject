import unittest
from collections import Counter
from BigramGeneration import BigramGeneration  # Adjust module name if necessary
import tempfile
import os


class TestBigram(unittest.TestCase):

    def setUp(self):
        # Create an analyzer instance with a high word limit (e.g. 5000) so that tests are not limited.
        self.analyzer = BigramGeneration(debug=False, word_size=20)

    def test_clean_text(self):
        """Test cleanup cases."""
        self.assertEqual(self.analyzer.clean_text("Hello, World!"), "hello world")
        self.assertEqual(self.analyzer.clean_text("123 Testing!"), " testing")
        self.assertEqual(self.analyzer.clean_text("No@Special#Chars$"), "nospecialchars")
        self.assertEqual(self.analyzer.clean_text("one\ntwo"), "one\ntwo")
        self.assertEqual(self.analyzer.clean_text("ABC Def"), "abc def")

    def test_get_bigrams_normal(self):
        text = "The quick brown fox"
        expected = ["the quick", "quick brown", "brown fox"]
        self.assertEqual(self.analyzer.generate_bigrams(text), expected)

    def test_get_bigrams_to_handle_numbers(self):
        """Test the presence of numbers in the text."""
        text = "The address is 12345 nowhere street omaha nebraska"
        expected = ['the address', 'address is', 'is nowhere', 'nowhere street', 'street omaha', 'omaha nebraska']
        self.assertEqual(self.analyzer.generate_bigrams(text), expected)

    def test_to_handle_empty_strings(self):
        """Test with an empty string."""
        text = "                                        "
        expected = []
        self.assertEqual(self.analyzer.generate_bigrams(text), expected)

    def test_to_handle_empty_strings_and_single_word(self):
        """Test empty strings and single word cases."""
        text = "                                        nebraska"
        expected = []
        self.assertEqual(self.analyzer.generate_bigrams(text), expected)

    def test_clean_text_lowercases(self):
        """Test that clean_text converts text to lowercase."""
        text = "ABC Def"
        cleaned = self.analyzer.clean_text(text)
        self.assertEqual(cleaned, "abc def")

    def test_newline_delimiter_generation(self):
        """Test that newline characters are preserved by clean_text and processed correctly by generate_bigrams."""
        expected = ["one two"]
        self.assertEqual(self.analyzer.generate_bigrams("one\ntwo"), expected)
        self.assertEqual(self.analyzer.generate_bigrams("one\n two"), expected)
        self.assertEqual(self.analyzer.generate_bigrams("one \ntwo"), expected)

    def test_get_bigrams_insufficient_words(self):
        """One word should not generate any bigrams."""
        self.assertEqual(self.analyzer.generate_bigrams("Word"), [])
        self.assertEqual(self.analyzer.generate_bigrams(""), [])

    def test_bigram_singles(self):
        """Test with a sequence of single characters."""
        text = "a a a b b a"
        expected_counts = Counter({
            "a a": 2,
            "a b": 1,
            "b b": 1,
            "b a": 1
        })
        # Reset bigram_counts to get a fresh count.
        self.analyzer.bigram_counts = {}
        self.assertEqual(self.analyzer.bigram_with_counts(text), expected_counts)

    def test_analyze_text_source_with_file(self):
        """Test that reading from a temporary file produces the correct bigram counts."""
        content = "foo bar baz foo bar"
        expected = Counter({
            "foo bar": 2,
            "bar baz": 1,
            "baz foo": 1
        })

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp:
            temp.write(content)
            temp_path = temp.name
            #print(temp_path)
            #print(temp.name)
        try:
            self.analyzer.bigram_counts = {}
            result = self.analyzer.analyze_input_source(temp_path)
            self.assertEqual(result, expected)
        finally:
            os.remove(temp_path)

    def test_analyze_text_source_with_raw_text(self):
        """Test frequencies with raw text input."""
        text = "one two three one two"
        expected = Counter({
            "one two": 2,
            "two three": 1,
            "three one": 1
        })
        # Reset bigram_counts before processing.
        self.analyzer.bigram_counts = {}
        result = self.analyzer.analyze_input_source(text)
        self.assertEqual(result, expected)

    def test_analyze_text_source_invalid_input(self):
        """Test that analyze_text_source raises ValueError when input is not a string."""
        with self.assertRaises(ValueError):
            self.analyzer.analyze_input_source(123)

    def test_long_filename_handling(self):
        """Test that longer filename are treated as simple strings"""
        filename = "a" * 255 +'txt'
        expected = {}
        result = self.analyzer.analyze_input_source(filename)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
