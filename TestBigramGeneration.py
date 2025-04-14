import unittest
from BigramGeneration import BigramGeneration  # Adjust module name if necessary
import tempfile
import os


class TestBigram(unittest.TestCase):

    def setUp(self):
        # Create an analyzer instance with a high word limit (e.g. 5000) so that tests are not limited.
        self.analyzer = BigramGeneration(debug=False, word_size=20,histogram_generation=False)

    def test_clean_operation(self):
        """Test cleanup cases. extract alpha numerica values"""
        self.assertEqual(self.analyzer.clean_text("Hello, World!"), "hello world")
        self.assertEqual(self.analyzer.clean_text("123 Testing!"), "123 testing")
        self.assertEqual(self.analyzer.clean_text("No@Special#Chars$"), "nospecialchars")
        self.assertEqual(self.analyzer.clean_text("one\ntwo"), "one\ntwo")
        self.assertEqual(self.analyzer.clean_text("ABC Def"), "abc def")
        self.assertEqual(self.analyzer.clean_text("year-old"), "year old")

    def test_get_bigrams_normal(self):
        text = "The quick brown fox and the quick blue hare"
        expected = ["the quick", "quick brown", "brown fox","fox and", "and the","the quick","quick blue","blue hare"]
        self.assertEqual(self.analyzer.generate_bigrams_tokens(text), expected)

    def test_get_bigrams_to_handle_numbers(self):
        """Test the presence of numbers in the text."""
        text = "The address is 12345 nowhere street omaha nebraska"
        expected = ['the address', 'address is','is 12345', '12345 nowhere', 'nowhere street', 'street omaha', 'omaha nebraska']
        expected_freq ={'the address':1, 'address is':1,'is 12345':1, '12345 nowhere':1, 'nowhere street':1, 'street omaha':1, 'omaha nebraska':1}
        self.assertEqual(self.analyzer.generate_bigrams_tokens(text), expected)
        self.assertEqual(self.analyzer.parse_bigrams_from_text(text), expected_freq)

    def test_to_handle_empty_strings(self):
        """Test with an empty string."""
        text = "                                        "
        expected = []
        self.assertEqual(self.analyzer.generate_bigrams_tokens(text), expected)
        self.assertEqual(self.analyzer.parse_bigrams_from_text(text), {})

    def test_to_handle_empty_strings_and_single_word(self):
        """Test empty strings and single word cases."""
        text = "                                        nebraska"
        expected = []
        self.assertEqual(self.analyzer.generate_bigrams_tokens(text), expected)
        self.assertEqual(self.analyzer.parse_bigrams_from_text(text), {})

    def test_clean_text_lowercases(self):
        """Test that clean_text converts text to lowercase."""
        text = "ABC Def"
        cleaned = self.analyzer.clean_text(text)
        self.assertEqual(cleaned, "abc def")

    def test_newline_delimiter_generation(self):
        """Test that newline characters are preserved by clean_text and processed correctly by generate_bigrams."""
        expected = ["one two"]
        self.assertEqual(self.analyzer.generate_bigrams_tokens("one\ntwo"), expected)
        self.assertEqual(self.analyzer.parse_bigrams_from_text("one\ntwo"), {"one two":1})
        self.assertEqual(self.analyzer.generate_bigrams_tokens("one\n two"), expected)
        self.assertEqual(self.analyzer.parse_bigrams_from_text("one\ntwo"), {"one two":1})
        self.assertEqual(self.analyzer.generate_bigrams_tokens("one \ntwo"), expected)
        self.assertEqual(self.analyzer.parse_bigrams_from_text("one\ntwo"), {"one two":1})

    def test_get_bigrams_insufficient_words(self):
        """One word should not generate any bigrams."""
        self.assertEqual(self.analyzer.generate_bigrams_tokens("Word"), [])
        self.assertEqual(self.analyzer.generate_bigrams_tokens(""), [])
        self.assertEqual(self.analyzer.parse_bigrams_from_text(""), {})
        self.assertEqual(self.analyzer.parse_bigrams_from_text("Word"), {})

    def test_bigram_singles(self):
        """Test with a sequence of single characters."""
        text = "a a a b b a"
        expected_counts = { "a a": 2, "a b": 1, "b b": 1, "b a": 1}
        # Reset bigram_counts to get a fresh count.
        self.analyzer.bigram_token_frequency = {}
        self.assertEqual(self.analyzer.bigram_get_token_with_counts(text), expected_counts)

    def test_analyze_text_source_with_file(self):
        """Test that reading from a temporary file produces the correct bigram counts."""
        content = "foo bar baz foo bar"
        expected = { "foo bar": 2, "bar baz": 1, "baz foo": 1}

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp:
            temp.write(content)
            temp_path = temp.name
            #print(temp_path)
            #print(temp.name)
        try:
            self.analyzer.bigram_token_frequency = {}
            result = self.analyzer.parse_bigrams_from_text(temp_path)
            self.assertEqual(result, expected)
        finally:
            os.remove(temp_path)

    def test_correct_frequency_output(self):
        """Test frequencies with raw text input."""
        text = "one two three one two"
        expected = {"one two": 2, "two three": 1, "three one": 1}

        # Reset bigram_counts before processing.
        self.analyzer.bigram_token_frequency = {}
        result = self.analyzer.parse_bigrams_from_text(text)
        self.assertEqual(result, expected)

    def test_analyze_text_source_invalid_input(self):
        """Test that analyze_text_source raises ValueError when input is not a string."""
        with self.assertRaises(ValueError):
            self.analyzer.parse_bigrams_from_text(123)

    def test_long_filename_handling(self):
        """Test that longer filename are treated as simple strings"""
        filename = "a" * 255 +'txt'
        expected = {}
        result = self.analyzer.parse_bigrams_from_text(filename)
        self.assertEqual(result, expected)

    def test_mixed_case_case_sensitive(self):
        """Test repeating tokens"""
        input_string = "The the The"
        expected_output = {"the the": 2}
        self.assertEqual(self.analyzer.parse_bigrams_from_text(input_string), expected_output )

    def test_only_punctuation_marks(self):
        """Test just punctuation marks"""
        input_string = "!!! ???"
        expected_output = {}
        self.assertEqual(self.analyzer.parse_bigrams_from_text(input_string), expected_output )

    def test_single_space(self):
        """Test single space characters"""
        input_string = " "
        expected_output = {}
        self.assertEqual(self.analyzer.parse_bigrams_from_text(input_string), expected_output )

    def test_just_numbers(self):
        """Test just number tokens"""
        input_string = "123 456 123"
        expected_output = {"123 456": 1,"456 123":1}
        self.assertEqual(self.analyzer.parse_bigrams_from_text(input_string), expected_output )

    def test_accented_letters(self):
        """Test accented letters"""
        input_string = "Café au lait"
        expected_output = {"café au": 1,"au lait":1}
        self.assertEqual(self.analyzer.parse_bigrams_from_text(input_string), expected_output )

    def test_minus_sign(self):
        """Test minus sign between words like year-old"""
        input_string = "year-old"
        expected_output = {"year old": 1}
        self.assertEqual(self.analyzer.parse_bigrams_from_text(input_string), expected_output )

if __name__ == '__main__':
    unittest.main()
