# -*- coding: utf-8 -*-
import unittest

from parser_for_nutch import NutchParser

class TestNutchParser(unittest.TestCase):

    def setUp(self):
        self.test_nutch_parser = NutchParser()

    def test_delete_signs(self):
        test_data = 'test.txt'
        true_result = 'Karabakh - Earth and people...\nHeyd?r ?liyev Gulhan?y? niy?'
        fact_result = self.test_nutch_parser.delete_signs(test_data)
        #print(fact_result)
        self.assertEqual(true_result, fact_result)
        
    def test_langid(self):
        '''
        2 предложения на английском, 2 на русском и 2 на азербайджанском.
        '''
        test_data = 'Sentence one. Sentence two. Mən Jo Prezelın sözləri ilə razıyam beynəlxalq ticarət embarqo başlanması haqda. Bu embarqo konflikti deyildi, dəmir yolların və kommunikasiyanın bağlanması idi. Это первое предложение на русском. А это второе.'
        true_result = ['Mən Jo Prezelın sözləri ilə razıyam beynəlxalq ticarət embarqo başlanması haqda.',
                       'Bu embarqo konflikti deyildi, dəmir yolların və kommunikasiyanın bağlanması idi.']
        self.test_nutch_parser.langid(test_data)
        fact_result = self.test_nutch_parser.tokens
        self.assertEqual(true_result, fact_result)
        
    def test_counts(self):
        self.test_nutch_parser.tokens = ['Mən Jo Prezelın sözləri ilə razıyam beynəlxalq ticarət embarqo başlanması haqda.',
                       'Bu embarqo konflikti deyildi, dəmir yolların və kommunikasiyanın bağlanması idi.']
        true_result = (2, 21)
        fact_result = self.test_nutch_parser.counts()
        self.assertEqual(true_result, fact_result)

    def test_symbols_s(self):
        self.test_nutch_parser.tokens = ['\nMən Jo Prezelın sözləri ilə razıyam beynəlxalq ticarət embarqo başlanması haqda.',
                       'Bu embarqo konflikti deyildi, dəmir yolların və kommunikasiyanın bağlanması idi.']
        true_result = ['<s> Mən Jo Prezelın sözləri ilə razıyam beynəlxalq ticarət embarqo başlanması haqda </s>',
                       '<s> Bu embarqo konflikti deyildi, dəmir yolların və kommunikasiyanın bağlanması idi </s>']
        fact_result = self.test_nutch_parser.symbols_s()
        self.assertEqual(true_result, fact_result)
        
if __name__ == '__main__':
    unittest.main()