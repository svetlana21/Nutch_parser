# -*- coding: utf-8 -*-
import pprint as pp
import re
import langid
from nltk.tokenize import sent_tokenize

class NutchParser():
    '''
    Класс для обработки данных Nutch.
    '''
    def __init__(self):
        self.tokens = []
    
    def delete_signs(self, filename):
        '''
        Удаление помет, расставляемых натчем
        '''
        with open(filename, encoding='utf-8') as file:       # чтение файла
            text = file.read()
        recno = re.compile('\nRecno::.+')       # регулярные выражения, соответствующие пометам
        url = re.compile('\nURL::.+')
        parse = re.compile('\n\nParseText::\n')
        text = re.sub(recno, '', text)      # удаление помет
        text = re.sub(url, '', text)
        text = re.sub(parse, '', text)
        return text
    
    def langid(self, text):
        '''
        Разбиение на предложения и удаление английских и русских предложений
        '''
        self.tokens = sent_tokenize(text)        # разбиение на предложения
        non_az_tokens = []
        for token in self.tokens:
            lang = langid.classify(token)       # определение языка токена
            if lang[0] == 'en' or lang[0] == 'ru':
                non_az_tokens.append([token, lang[0]])      # запись русских и английских токенов в отдельный список
        for token in non_az_tokens:     # удаление русских и английских токенов из списка всех токенов
            self.tokens.remove(token[0])

    def counts(self):
        '''
        Подсчёт числа слов и предложений.
        '''
        num_sent = len(self.tokens)
        new_text = ' '.join(self.tokens)
        num_words = new_text.count(' ') + 1
        print('Number of sentences: ', num_sent)
        print('Number of words: ', num_words)
        return num_sent, num_words

    def symbols_s(self):
        '''
        Расстановка символов начала и конца предложения <s> и </s> и запись в файл.
        '''
        tokens_with_s=[]
        for token in self.tokens:       # расстановка символов <s> и </s>
            token = token.strip('\n')      # удаление лишних символов
            token = token.strip('\r')
            tokens_with_s.append('<s> ' + token[:-1] + ' </s>')
        new = open('tokens.txt', 'w', encoding='utf-8')     # запись в файл
        for token in tokens_with_s:
            new.write("%s\n" % token)
        new.close()
        return tokens_with_s
        
if __name__ == '__main__':
    
    my_parser = NutchParser()
    
    text = my_parser.delete_signs('texts.txt')
    my_parser.langid(text)
    my_parser.counts()
    my_parser.symbols_s()