import unittest
from collections import Counter
from BigramGeneration import clean_text, generate_bigrams, bigram_with_counts, analyze_text_source
import tempfile
import os

class TestBigram(unittest.TestCase):

    def test_clean_text(self):
        """test cleanup cases"""
        self.assertEqual(clean_text("Hello, World!"), "hello world")
        self.assertEqual(clean_text("123 Testing!"), " testing")
        self.assertEqual(clean_text("No@Special#Chars$"), "nospecialchars")
        self.assertEqual(clean_text("one\ntwo"), "one\ntwo")
        self.assertEqual(clean_text("ABC Def"), "abc def")

    def test_get_bigrams_normal(self):
        text = "The quick brown fox"
        expected = ["the quick", "quick brown", "brown fox"]
        self.assertEqual(generate_bigrams(text), expected)

    def test_get_bigrams_to_handle_numbers(self):
        """Test the presence of numbers in the text"""
        text = "The address is 12345 nowhere street omaha nebraska"
        expected = ['the address','address is', 'is nowhere', 'nowhere street', 'street omaha', 'omaha nebraska']
        self.assertEqual(generate_bigrams(text), expected)

    def test_to_handle_empty_strings(self):
        """Test empty string"""
        text = "                                        "
        expected = []
        self.assertEqual(generate_bigrams(text), expected)

    def test_to_handle_empty_strings_and_single_word(self):
        """Test empty strings and single word"""
        text = "                                        nebraska"
        expected = []
        self.assertEqual(generate_bigrams(text), expected)

    def test_clean_text_lowercases(self):
        """Test that clean_text converts text to lowercase."""
        text = "ABC Def"
        cleaned = clean_text(text)
        self.assertEqual(cleaned, "abc def")

    def test_newline_delimiter_generation(self):
        """Test that clean_text keep newline"""
        expected = ["one two"]
        self.assertEqual(generate_bigrams("one\ntwo"), expected)
        self.assertEqual(generate_bigrams("one\n two"), expected)
        self.assertEqual(generate_bigrams("one \ntwo"), expected)

    def test_get_bigrams_insufficient_words(self):
        """one word should not generate a bigram"""
        self.assertEqual(generate_bigrams("Word"), [])
        self.assertEqual(generate_bigrams(""), [])

    def test_bigram_singles(self):
        """ Test with single characters"""
        text = "a a a b b a"
        expected_counts = Counter({
            "a a": 2,
            "a b": 1,
            "b b": 1,
            "b a": 1
        })
        self.assertEqual(bigram_with_counts(text), expected_counts)

    def test_analyze_text_source_with_file(self):
        """temp file read and should have correct output and counts"""
        content = "foo bar baz foo bar"
        expected = Counter({
            "foo bar": 2,
            "bar baz": 1,
            "baz foo": 1
        })

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp:
            temp.write(content)
            temp_path = temp.name
        try:
            result = analyze_text_source(temp_path)
            self.assertEqual(result, expected)
        finally:
            os.remove(temp_path)

    def test_analyze_text_source_with_raw_text(self):
        """ test frequencies with raw text"""
        text = "one two three one two"
        expected = Counter({
            "one two": 2,
            "two three": 1,
            "three one": 1
        })
        result = analyze_text_source(text)
        self.assertEqual(result, expected)

    def test_analyze_text_source_invalid_input(self):
        """Test that analyze_text_source raises a ValueError when the input is not a string."""
        with self.assertRaises(ValueError):
            analyze_text_source(123)

if __name__ == '__main__':
    unittest.main()
