# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals

from .base import Num2Word_Base
from .utils import get_digits, splitbyx
import regex as re


def get_ord_map(mydict):
    result = {}
    for val in mydict.values():
        result[val[0]] = val[1]
    return result

ZERO = ('ноль', 'нуля', 'нулю', 'ноль', 'нулем', 'нуле')

ONES_FEMININE = {
    1: ('одна', 'одной', 'одной', 'одну', 'одной', 'одной'),
    2: ('две', 'двух', 'двум', 'две', 'двумя', 'двух'),
    3: ('три', 'трех', 'трем', 'три', 'тремя', 'трех'),
    4: ('четыре', 'четырех', 'четырем', 'четыре', 'четырьмя', 'четырех'),
    5: ('пять', 'пяти', 'пяти', 'пять', 'пятью', 'пяти'),
    6: ('шесть', 'шести', 'шести', 'шесть', 'шестью', 'шести'),
    7: ('семь', 'семи', 'семи', 'семь', 'семью', 'семи'),
    8: ('восемь', 'восьми', 'восьми', 'восемь', 'восемью', 'восьми'),
    9: ('девять', 'девяти', 'девяти', 'девять', 'девятью', 'девяти'),
}

ONES = {
    1: ('один', 'одного', 'одному', 'один', 'одним', 'одном'),
    2: ('два', 'двух', 'двум', 'два', 'двумя', 'двух'),
    3: ('три', 'трёх', 'трём', 'три', 'тремя', 'трёх'),
    4: ('четыре', 'четырёх', 'четырём', 'четыре', 'четырьмя', 'четырёх'),
    5: ('пять', 'пяти', 'пяти', 'пять', 'пятью', 'пяти'),
    6: ('шесть', 'шести', 'шести', 'шесть', 'шестью', 'шести'),
    7: ('семь', 'семи', 'семи', 'семь', 'семью', 'семи'),
    8: ('восемь', 'восьми', 'восьми', 'восемь', 'восемью', 'восьми'),
    9: ('девять', 'девяти', 'девяти', 'девять', 'девятью', 'девяти'),
}

TENS = {
    0: ('десять', 'десяти', 'десяти', 'десять', 'десятью', 'десяти'),
    1: ('одиннадцать', 'одиннадцати', 'одиннадцати', 'одиннадцать', 'одиннадцатью', 'одиннадцати'),
    2: ('двенадцать', 'двенадцати', 'двенадцати', 'двенадцать', 'двенадцатью', 'двенадцати'),
    3: ('тринадцать', 'тринадцати', 'тринадцати', 'тринадцать', 'тринадцатью', 'тринадцати'),
    4: ('четырнадцать', 'четырнадцати', 'четырнадцати', 'четырнадцать', 'четырнадцатью', 'четырнадцати'),
    5: ('пятнадцать', 'пятнадцати', 'пятнадцати', 'пятнадцать', 'пятнадцатью', 'пятнадцати'),
    6: ('шестнадцать', 'шестнадцати', 'шестнадцати', 'шестнадцать', 'шестнадцатью', 'шестнадцати'),
    7: ('семнадцать', 'семнадцати', 'семнадцати', 'семнадцать', 'семнадцатью', 'семнадцати'),
    8: ('восемнадцать', 'восемнадцати', 'восемнадцати', 'восемнадцать', 'восемнадцатью', 'восемнадцати'),
    9: ('девятнадцать', 'девятнадцати', 'девятнадцати', 'девятнадцать', 'девятнадцатью', 'девятнадцати'),
}

ORD_MAP = get_ord_map(TENS)

TWENTIES = {
    2: ('двадцать', 'двадцати', 'двадцати', 'двадцать', 'двадцатью', 'двадцати'),
    3: ('тридцать', 'тридцати', 'тридцати', 'тридцать', 'тридцатью', 'тридцати'),
    4: ('сорок', 'сорока', 'сорока', 'сорок', 'сорока', 'сорока'),
    5: ('пятьдесят', 'пятидесяти', 'пятидесяти', 'пятьдесят', 'пятидесятью', 'пятидесяти'),
    6: ('шестьдесят', 'шестидесяти', 'шестидесяти', 'шестьдесят', 'шестидесятью', 'шестидесяти'),
    7: ('семьдесят', 'семидесяти', 'семидесяти', 'семьдесят', 'семидесятью', 'семидесяти'),
    8: ('восемьдесят', 'восьмидесяти', 'восьмидесяти', 'восемьдесят', 'восьмидесятью', 'восьмидесяти'),
    9: ('девяносто', 'девяноста', 'девяноста', 'девяносто', 'девяноста', 'девяноста'),
}

ORD_MAP.update(get_ord_map(TWENTIES))

HUNDREDS = {
    1: ('сто', 'ста', 'стам', 'сто', 'ста', 'ста'),
    2: ('двести', 'двухсот', 'двумстам', 'двести', 'двумяста', 'двухстах'),
    3: ('триста', 'трёхсот', 'трёмстам', 'триста', 'тремястами', 'трёхстах'),
    4: ('четыреста', 'четырёхсот', 'четырёмстам', 'четыреста', 'четырьмястами', 'четырёхстах'),
    5: ('пятьсот', 'пятисот', 'пятистам', 'пятьсот', 'пятьюстами', 'пятистах'),
    6: ('шестьсот', 'шестисот', 'шестистам', 'шестьсот', 'шестьюстами', 'шестистах'),
    7: ('семьсот', 'семисот', 'семистам', 'семьсот', 'семьюстами', 'семистах'),
    8: ('восемьсот', 'восьмисот', 'восьмистам', 'восемьсот', 'восемьюстами', 'восьмистах'),
    9: ('девятьсот', 'девятисот', 'девятистам', 'девятьсот', 'девятьюстами', 'девятистах'),
}
ORD_MAP.update(get_ord_map(HUNDREDS))

THOUSANDS_BASE = {
1: 'тысяч',
2: 'миллион',
3: 'миллиард',
4: 'триллион',
5: 'квадриллион',
6: 'квинтиллион',
7: 'секстиллион',
8: 'септиллион',
9: 'октиллион',
10: 'нониллион'
}

THOUSANDS = {
    1: (('а', 'и', 'ам', 'у', 'ью', 'е'),
        ('и', '', 'ам', 'и', 'ами', 'ах'),
        ('', '', 'ам', '', 'ами', 'ах')),  # 10^3
    2: (('', 'а', 'у', '', 'ом', 'е'),
        ('а', 'ов', 'ам', 'а', 'ами', 'ах'),
        ('ов', 'ов', 'ам', 'ов', 'ами', 'ах'))
}



class Num2Word_RU(Num2Word_Base):
    CURRENCY_FORMS = {
        'RUB': (
            ('рубль', 'рубля', 'рублей'), ('копейка', 'копейки', 'копеек')
        ),
        'EUR': (
            ('евро', 'евро', 'евро'), ('цент', 'цента', 'центов')
        ),
        'USD': (
            ('доллар', 'доллара', 'долларов'), ('цент', 'цента', 'центов')
        ),
        'UAH': (
            ('гривна', 'гривны', 'гривен'), ('копейка', 'копейки', 'копеек')
        ),
        'KZT': (
            ('тенге', 'тенге', 'тенге'), ('тиын', 'тиына', 'тиынов')
        ),
    }
    def pluralize(self, n, forms):
        if n == 0:
            return forms[2]
        if n % 10 == 1:
            return forms[0]
        elif n % 10 <= 4:
            return forms[1]
        return forms[2]

    def setup(self):

        self.cards_suff_map = {'ти': 1,
                               'и': 1
                               }

        self.negword = "минус"
        self.pointword = "запятая"

        self.ord_suffixes = {0: ('ый', 'ого', 'ому', 'ый', 'ым', 'ом'),
                             1: ('ое', 'ого', 'ому', 'ое', 'ым', 'ом'),
                             2: ('ая', 'ой', 'ой', 'ую', 'ой', 'ой'),
                             3: ('ые', 'ых', 'ым', 'ые', 'ыми', 'ых')}

        self.ord_three = {0: ('ий', 'ьего', 'ьему', 'ий', 'ьим', 'ьем'),
                          1: ('ье', 'ьего', 'ьему', 'ье', 'ьим', 'ьем'),
                          2: ('ья', 'ьей', 'ьей', 'ью', 'ьей', 'ьей'),
                          3: ('ьи', 'ьих', 'ьим', 'ьи', 'ьими', 'ьих')}

        self.ord_stems = {"ноль": "нулев",
                          "один": "перв",
                          "два": "втор",
                          "три": "трет",
                          "четыре": "четверт",
                          "пять": "пят",
                          "шесть": "шест",
                          "семь": "седьм",
                          "восемь": "восьм",
                          "девять": "девят",
                          "сто": "сот"}
        for x in THOUSANDS_BASE.values():
            self.ord_stems[x] = x + 'н'

        self.ords = {"ноль": "нулевой",
                     "один": "первый",
                     "два": "второй",
                     "три": "третий",
                     "четыре": "четвертый",
                     "пять": "пятый",
                     "шесть": "шестой",
                     "семь": "седьмой",
                     "восемь": "восьмой",
                     "девять": "девятый",
                     "сто": "сотый"}

        self.ords_feminine = {"один": "одна",
                              "одна": "одна",
                              "одного": "одна",
                              "одной": "одна",
                              "две": "двух",
                              "три": "трёх",
                              "четыре": "четырёх",
                              "пять": "пяти",
                              "шесть": "шести",
                              "семь": "семи",
                              "восемь": "восьми",
                              "девять": "девяти",
                              }
        self.ords_suff_map = {'го': (0, 1),
                              'х': (3, 1),
                              'ых': (3, 1),
                              'м': (0, 5),
                              'ом': (0, 5),
                              'му': (0, 2),
                              'ому': (0, 2),
                              'ой': (2, 1),
                              'ая': (2, 0),
                              'я': (2, 0),
                              'ую': (2, 3),
                              'ю': (2, 3),
                              'й': (0, 0),
                              'ый': (0, 0),
                              'е': (3, 0),
                              'ые': (3, 0),
                              'ми': (3, 4)
                             }

    def to_cardinal(self, number, case=0):
        n = str(number).replace(',', '.')
        my_case = case
        m = re.match('^(.*?\d+)\-?(\p{L}{1,3})', n)
        if m:
            n = m.group(1)
            suff = m.group(2)
            if suff in self.cards_suff_map:
                my_case = self.cards_suff_map[suff]

        if '.' in n:
            left, right = n.split('.')
            return u'%s %s %s' % (
                self._int2word(int(left), case=my_case),
                self.pointword,
                self._int2word(int(right), case=my_case)
            )
        else:
            return self._int2word(int(n), case=my_case)

    def pluralize_thousand_potentials(self, n, i, case=0):
        if n % 100 < 10 or n % 100 > 20:
            if n % 10 == 1:
                form = 0
            elif 5 > n % 10 > 1:
                form = 1
            else:
                form = 2
        else:
            form = 2
        m = 1
        if i > 1:
            m = 2
        return THOUSANDS_BASE[i] + THOUSANDS[m][form][case]

    def process_ordinal_word(self, word, ending):
        if word[:-3] in self.ords_feminine:
            word = self.ords_feminine.get(word[:-3], word) + "сот" + ending
        elif word[-1] == "ь" or word[-2] == "т":
            word = word[:-1] + ending
        elif word[-1] == "к": # 40 - сорок
            word = word + "ов" + ending
        elif word[-5:] == "десят":
            word = word.replace('ь', 'и') + ending
        elif word[-2] == "ч" or word[-1] == "ч":
            if word[-2] == "ч":
                word = word[:-1] + "н" + ending
            if word[-1] == "ч":
                word = word + "н" + ending
        elif word[-1] == "н" or word[-2] == "н":
            word = word[:word.rfind('н') + 1] + "н" + ending
        elif word[-1] == "д" or word[-2] == "д":
            word = word[:word.rfind('д') + 1] + "н" + ending
        return word

    def to_ordinal(self, number, num_gender=0, case=0):
        my_num_gender = num_gender
        my_case = case
        m = re.match('(\d+)\-?(\p{L}{1,3})', number)
        if m:
            number = m.group(1)
            suff = m.group(2)
            if suff in self.ords_suff_map:
                my_num_gender, my_case = self.ords_suff_map[suff]
        return self.to_ordinal_num(int(number), num_gender=my_num_gender, case=my_case)

    def to_ordinal_num(self, number, num_gender=0, case=0):
    # optional num_gender: 0 (male), 1 (neutral), 2 (female) , 3 (plural)
    # optional case: from 0 (nominative) to 5 (prepositional)
        self.verify_ordinal(number)
        c = 1 if (number % 1000) == 0 else 0
        outwords = self.to_cardinal(number, case=c).split(' ')
        lastword = outwords[-1].lower()
        if num_gender == 0 and case in [0, 3] and lastword in ['ноль', 'два', 'шесть', 'семь', 'восемь']:
            ending = 'ой'
        else:
            ord_suffixes = self.ord_three if lastword == 'три' else self.ord_suffixes
            ending = ord_suffixes[num_gender][case]
        try:
            if len(outwords) > 1:
                if outwords[-2] in self.ords_feminine:
                    outwords[-2] = self.ords_feminine.get(outwords[-2], outwords[-2])
                for i in range(0, 3):
                    if lastword[:-i] in THOUSANDS_BASE.values():
                        outwords[-2] = ORD_MAP.get(outwords[-2], outwords[-2])
                        if len(outwords) > 2:
                            outwords[-3] = ORD_MAP.get(outwords[-3], outwords[-3])
                        lastword = lastword[:-i]
                        break
            if len(outwords) == 3:
                if outwords[-3] in ['один', 'одна', 'одного', 'одной']:
                    outwords[-3] = ''
            lastword = self.ord_stems[lastword] + ending
        except KeyError: # for everything not in ord_stems
            lastword = self.process_ordinal_word(lastword, ending)
        outwords[-1] = self.title(lastword)
        return " ".join(outwords).strip()

    def _cents_verbose(self, number, currency):
        return self._int2word(number, currency == 'RUB')


    def _int2word(self, n, feminine=False, case=0):
        m = n
        result = ''
        if n < 0:
            m = abs(n)
            result += self.negword + ' '
        return self.my_int2word(m, feminine=feminine, case=case)

    def my_int2word(self, n, feminine=False, case=0):
        if n == 0:
            return ZERO[case]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                words.append(HUNDREDS[n3][case])

            if n2 > 1:
                words.append(TWENTIES[n2][case])

            if n2 == 1:
                words.append(TENS[n1][case])
            elif n1 > 0:
                if i == 1 or (feminine and i == 0):
                    ones = ONES_FEMININE
                else:
                    ones = ONES
                mycase = case
                if mycase == 3: # accusative
                    if i==0 and n1 <= 4 and (n2+n3) == 0:
                        mycase = 1 # genetive form for individual digits <=4 only, only for stand-alone small numbers
                # print("DEBUG: ", n1, mycase, len(ones), len(ones[n1]))
                words.append(ones[n1][mycase])

            if i > 0:
                words.append(self.pluralize_thousand_potentials(x, i, case))

        return ' '.join(words)


if __name__ == '__main__':
    yo = Num2Word_RU()
    import sys
    for line in sys.stdin:
        nums = line.strip().split()
        for num in nums:
            for case in [0, 1, 2, 3, 4, 5]:
                print(num, yo.to_cardinal(num, case=case))
            for num_gender in [0, 1, 2, 3]:
                for case in [0, 1, 2, 3, 4, 5]:
                    print(num, yo.to_ordinal(num, num_gender=num_gender, case=case))
            print(num, yo.to_currency(num, currency='RUB'))
        sys.stdout.write("\n")

