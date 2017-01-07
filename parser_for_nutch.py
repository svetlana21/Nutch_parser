# -*- coding: utf-8 -*-
import pprint as pp
import re
import langid
import string
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
            
    def sent_norm(self):
        '''
        Нормализация предложений.
        1. Замена некоторых данных на спецсимволы:
            1) даты -> D;
            2) время -> TIME;
            3) числа -> N;
            4) ссылки -> LINK;
            5) телефоны -> TEL;
            6) адреса эл. почты -> EMAIL.
        2. Удаление информации следующей за знаком копирайта.
        3. Удаление лишних пробельных символов и пунктуации.
        4. Удаление токенов, содержащих > 3 обозначений чисел N подряд (т.к. скорее всего это нумерация страниц) и токенов из одного слова.
        '''
        for i in range(0, len(self.tokens)):
            token = self.tokens.pop(i)      # извлекаем по одному токену из списка
            token = re.sub('\d{4}-\d{2}-\d{2}|\d{2}[-.]\d{2}[-.]\d{4}|\d{2}\.\d{2}\.\d{2}', 'D', token)   # даты -> D
            token = re.sub('\d{2} (yanvar|fevral|mart|aprel|may|iyun|iyul|avqust|sentyabr|oktyabr|noyabr|dekabr) \d{4}', 'D', token)
            token = re.sub('\d{2}:\d{2}', 'TIME', token)        # время -> TIME
            token = re.sub('www\.\S+|http:\S+', 'LINK', token)  # ссылки -> LINK
            token = re.sub('\(?\+99\d? ?\(?\d{2,3}\)? ?\d{2,3}[ -]?\d{2,3}[ -]?\d{2,3}[ -]?', 'TEL', token)     # телефоны -> TEL
            token = re.sub('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 'EMAIL', token)       # адреса эл. почты -> EMAIL
            token = re.sub('\d+', 'N', token)   # числа -> N
            copy = token.find('©')              # Удаление информации следующей за знаком копирайта
            if copy != -1:
                token = token.replace(token[copy:], '')
            token = token.encode('utf-8')       # Удаление лишних пробельных символов и пунктуации
            punct_replacer = bytes.maketrans(string.punctuation.encode('utf-8'), ' '.encode('utf-8')*len(string.punctuation)) 
            token = token.translate(punct_replacer).decode('utf-8')
            token = ' '.join(token.split()).strip()
            self.tokens.insert(i, token)        # помещаем токен в список на прежнее место
        aux_list = []
        for token in self.tokens:
            spaces = token.count(' ')           # подсчёт пробелов в токене
            if 'N N N N' in token or spaces==0:
                aux_list.append(token)          # если токен содержит посл-ть N N N N или ни одного пробела, добавляем во вспомогательный список
        for tok in aux_list:
            self.tokens.remove(tok)             # удаляем из основного списка всё, что оказалось во вспомогательном

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
            tokens_with_s.append('<s> ' + token[:-1] + ' </s>')
        return tokens_with_s
    
    def write(self, all_tokens):
        new = open('tokens.txt', 'w', encoding='utf-8')     # запись в файл
        for token in all_tokens:
            new.write("%s\n" % token)
        new.close()
        
if __name__ == '__main__':
    
    my_parser = NutchParser()
    
    text = my_parser.delete_signs('texts.txt')
    my_parser.langid(text)
    my_parser.sent_norm()
    my_parser.counts()
    my_parser.symbols_s()
