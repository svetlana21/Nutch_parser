# -*- coding: utf-8 -*-
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
        Разбиение на предложения и удаление вкраплений иностранных языков.
        Турецкий язык не учитывается, т.к. langid часто путает его с азербайджанским.
        '''
        self.tokens = sent_tokenize(text)        # разбиение на предложения
        non_az_tokens = []
        for token in self.tokens:
            lang = langid.classify(token)       # определение языка токена
            if lang[0] != 'az' and lang[0] != 'tr':
                non_az_tokens.append([token, lang[0]])      # запись неазербайджанских токенов в отдельный список 
        for token in non_az_tokens:     # удаление неазербайджанских токенов из списка всех токенов
            self.tokens.remove(token[0])
            
    def sent_norm(self):
        '''
        Нормализация предложений.
        1. Замена некоторых данных на спецсимволы:
            1) даты -> DATE;
            2) время -> TIME;
            3) ссылки -> LINK;
            4) телефоны -> TEL;
            5) адреса эл. почты -> EMAIL;
            6) числа, записанные арабскими или римскими цифры -> N.
        2. Удаление информации следующей за знаком копирайта.
        3. Удаление лишних небуквенных символов.
        4. Удаление дефисов на месте тире с сохранением дефисных написаний слов.
        5. Удаление лишних пробельных символов.
        6. Удаление токенов, содержащих > 3 обозначений чисел N подряд (т.к. скорее всего это нумерация страниц) и токенов из одного слова.
        7. Удаление символа комбинируемой надстрочной точки (в unicode – U+0307).
        '''
        for i in range(0, len(self.tokens)):
            token = self.tokens.pop(i)      # извлекаем по одному токену из списка
            token = re.sub('\d{4}-\d{2}-\d{2}|\d{2}[-.]\d{2}[-.]\d{4}|\d{2}\.\d{2}\.\d{2}', 'DATE', token)   # даты -> DATE
            token = re.sub('\d{2} (yanvar|fevral|mart|aprel|may|iyun|iyul|avqust|sentyabr|oktyabr|noyabr|dekabr) \d{4}', 'DATE', token)
            token = re.sub('\d{2}:\d{2}', 'TIME', token)        # время -> TIME
            token = re.sub('www\.\S+|http:\S+', 'LINK', token)  # ссылки -> LINK
            token = re.sub('\(?\+99\d? ?\(?\d{2,3}\)? ?\d{2,3}[ -]?\d{2,3}[ -]?\d{2,3}', 'TEL', token)     # телефоны -> TEL
            token = re.sub('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 'EMAIL', token)       # адреса эл. почты -> EMAIL
            token = re.sub('\d+', 'N', token)   # числа -> N
            copy = token.find('©')              # Удаление информации следующей за знаком копирайта
            if copy != -1:
                token = token.replace(token[copy:], '')
            token = re.sub('[^AaBbCcÇçDdEeƏəFfGgĞğHhXxIıİiJjKkQqLlMmNnOoÖöPpRrSsŞşTtUuÜüVvYyZz\- ]', '', token)   # Удаление небуквенных символов         
            hyphen1 = token.find(' -')      # удаление дефисов на месте тире с сохранением дефисных написаний слов
            hyphen2 = token.find('- ')
            if hyphen1 != -1:
                token = token.replace(' -', ' ')
            if hyphen2 != -1:
                token = token.replace('- ', ' ')    
            split_token = token.split()     
            for ind in range(0, len(split_token)):
                word = split_token.pop(ind)
                word = re.sub('^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$', 'N', word)     # числа, записанные римскими цифрами -> N
                split_token.insert(ind, word)            
            token = ' '.join(split_token).strip()     # Удаление лишних пробельных символов
            self.tokens.insert(i, token)        # помещаем токен в список на прежнее место
        aux_list = []
        for token in self.tokens:
            spaces = token.count(' ')           # подсчёт пробелов в токене
            if 'N N N N' in token or spaces==0:
                aux_list.append(token)          # если токен содержит посл-ть N N N N или ни одного пробела, добавляем во вспомогательный список
        for tok in aux_list:
            self.tokens.remove(tok)             # удаляем из основного списка всё, что оказалось во вспомогательном
        clear_tokens = []
        for token in self.tokens:  # удаление символа U+0307, часто встречающегося в словах
            if '̇' in token:
                token = token.replace('̇', '')
            clear_tokens.append(token)
        self.tokens = clear_tokens.copy()

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
    # tokens = my_parser.tokens
    tokens = my_parser.symbols_s()
    my_parser.write(tokens)
