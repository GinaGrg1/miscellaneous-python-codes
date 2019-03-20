import unittest
import os

from analyze import analyze_text


class TextAnalysisTests(unittest.TestCase):
    """ Tests for the ``analyze_text()`` function."""

    def setUp(self):
        """ Fixture that creates a file for the text methods to use."""
        self.filename = 'text_analysis_test_file.txt'
        with open(self.filename, 'w') as f:
            f.write('Now we are engaged in a great civil war.\n'
                    'testing whether that nation,\n'
                    'or any nation so conceived and so dedicated,\n'
                    'can long endure.')

    def tearDown(self):
        """ Fixture that deletes the files used by the test methods."""
        try:
            os.remove(self.filename)
        except:
            pass

    def test_function_runs(self):
        """ Basic smoke test."""
        analyze_text(self.filename)

    def test_line_count(self):
        """ Check that the line count is correct."""
        self.assertEqual(analyze_text(self.filename)[0], 4, 'Test Failed: Line count does not match.')

    def test_character_count(self):
        """ Check that the character count is correct."""
        self.assertEqual(analyze_text(self.filename)[1], 131, 'Test Failed: Character count does not match.')

    def test_no_such_file(self):
        """ Check the proper exception is thrown for a missing file."""
        with self.assertRaises(IOError):
            analyze_text('foobar')

    def test_no_deletion(self):
        """ Check that the function doesn't delete the input file."""
        analyze_text(self.filename)
        self.assertTrue(os.path.exists(self.filename))


if __name__ == '__main__':
    unittest.main()