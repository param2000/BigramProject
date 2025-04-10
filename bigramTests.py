import unittest
from collections import Counter
from bigram import clean_text, generate_bigrams, bigram_with_counts, analyze_text_source
import tempfile
import os

class TestBigramHistogram(unittest.TestCase):

    def test_clean_text(self):
        self.assertEqual(clean_text("Hello, World!"), "hello world")
        self.assertEqual(clean_text("123 Testing!"), " testing")
        self.assertEqual(clean_text("No@Special#Chars$"), "nospecialchars")

    def test_get_bigrams_normal(self):
        text = "The quick brown fox"
        expected = ["the quick", "quick brown", "brown fox"]
        self.assertEqual(generate_bigrams(text), expected)

    def test_clean_text_lowercases(self):
        """Test that clean_text converts text to lowercase."""
        text = "ABC Def"
        cleaned = clean_text(text)
        self.assertEqual(cleaned, "abc def")

    def test_generate_bigrams_with_extra_spaces(self):
        """Test that extra spaces are correctly handled in generate_bigrams."""
        text = "   Hello    world   "
        # After cleaning: "hello world " -> split into ['hello', 'world']
        expected = ["hello world"]
        self.assertEqual(generate_bigrams(text), expected)

    def test_get_bigrams_insufficient_words(self):
        self.assertEqual(generate_bigrams("Word"), [])
        self.assertEqual(generate_bigrams(""), [])

    def test_bigram_singles(self):
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
