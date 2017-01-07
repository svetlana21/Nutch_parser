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
        
    def test_sent_norm(self):
        self.test_nutch_parser.tokens = ['  www.fd.az word 22.11.1999  ', ' http://abiturient.az/600anket/ 23 45,  \nword 12-11-2014, 15:00',
                                         '\n date 23.11.2014 tel +99412 344 00 00 12 yanvar 2016', '45 345 345 66', 'word © word',
                                         'date 1999-11-11 e-mail derslik@tqdk.gov.az']
        true_result = ['LINK word D', 'LINK N N word D TIME', 'date D tel TEL D', 'date D e mail EMAIL']
        self.test_nutch_parser.sent_norm()
        fact_result = self.test_nutch_parser.tokens
        print(fact_result)
        self.assertEqual(true_result, fact_result)
        
    def test_counts(self):
        self.test_nutch_parser.tokens = ['Mən Jo Prezelın sözləri ilə razıyam beynəlxalq ticarət embarqo başlanması haqda.',
                       'Bu embarqo konflikti deyildi, dəmir yolların və kommunikasiyanın bağlanması idi.']
        true_result = (2, 21)
        fact_result = self.test_nutch_parser.counts()
        self.assertEqual(true_result, fact_result)

    def test_symbols_s(self):
        self.test_nutch_parser.tokens = ['Mən Jo Prezelın sözləri ilə razıyam beynəlxalq ticarət embarqo başlanması haqda.',
                       'Bu embarqo konflikti deyildi, dəmir yolların və kommunikasiyanın bağlanması idi.']
        true_result = ['<s> Mən Jo Prezelın sözləri ilə razıyam beynəlxalq ticarət embarqo başlanması haqda </s>',
                       '<s> Bu embarqo konflikti deyildi, dəmir yolların və kommunikasiyanın bağlanması idi </s>']
        fact_result = self.test_nutch_parser.symbols_s()
        self.assertEqual(true_result, fact_result)
        
if __name__ == '__main__':
    unittest.main()
