import unittest

from translator import TranslatorWrap

class TestTranslator(unittest.TestCase):
    def en2zh(self):
        translator = TranslatorWrap()
        result = translator.en2zh("Are John B and Sarah Endgame  Its a Ship Show - Outer Banks  Netflix")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()