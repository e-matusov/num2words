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
from .currency import parse_currency_parts, prefix_currency

def get_ord_map(mydict):
    result = {}
    for val in mydict.values():
        result[val[0]] = val[1]
    return result

def print_forms(mapping, pref=''):
    for v in mapping.values():
        for x in v:
            print(pref+x)

class LanguageResources_RU:

    def print_all_forms(self):
        for v in self.ZERO:
            print(v)
        print_forms(self.ONES_FEMININE)
        print_forms(self.ONES)
        print_forms(self.TENS)
        print_forms(self.TWENTIES)
        print_forms(self.HUNDREDS)
        print(self.NEGWORD)
        print(self.POINTWORD)
        for v in self.THOUSANDS_BASE.values():
           for x in self.THOUSANDS.values():
               for y in x:
                   for z in y:
                       print(v+z)
        for v in self.ORD_STEMS.values():
            print_forms(self.ORD_SUFFIXES, v)
            print_forms(self.ORD_THREE, v)
        for x in self.ORDS_FEMININE.values():
            print(x)

    def __init__(self):
        self.NOUN_CASES = {'nom': 0,
                           'gen': 1,
                           'dat': 2,
                           'acc': 3,
                           'inst': 4,
                           'prep': 5}
        self.GENDERS = {'masc': 0,
                        'neut':  1,
                        'fem': 2,
                        'plur': 3} # technically not gender, but...

        self.ZERO = ('ноль', 'нуля', 'нулю', 'ноль', 'нулем', 'нуле')
        self.ONES_FEMININE = {
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

        self.ONES = {
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

        self.TENS = {
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
        self.ORD_MAP = get_ord_map(self.TENS)

        self.TWENTIES = {
            2: ('двадцать', 'двадцати', 'двадцати', 'двадцать', 'двадцатью', 'двадцати'),
            3: ('тридцать', 'тридцати', 'тридцати', 'тридцать', 'тридцатью', 'тридцати'),
            4: ('сорок', 'сорока', 'сорока', 'сорок', 'сорока', 'сорока'),
            5: ('пятьдесят', 'пятидесяти', 'пятидесяти', 'пятьдесят', 'пятидесятью', 'пятидесяти'),
            6: ('шестьдесят', 'шестидесяти', 'шестидесяти', 'шестьдесят', 'шестидесятью', 'шестидесяти'),
            7: ('семьдесят', 'семидесяти', 'семидесяти', 'семьдесят', 'семидесятью', 'семидесяти'),
            8: ('восемьдесят', 'восьмидесяти', 'восьмидесяти', 'восемьдесят', 'восьмидесятью', 'восьмидесяти'),
            9: ('девяносто', 'девяноста', 'девяноста', 'девяносто', 'девяноста', 'девяноста'),
        }
        self.ORD_MAP.update(get_ord_map(self.TWENTIES))

        self.HUNDREDS = {
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
        self.ORD_MAP.update(get_ord_map(self.HUNDREDS))

        self.THOUSANDS_BASE = {
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

        self.THOUSANDS = {
            1: (('а', 'и', 'ам', 'у', 'ью', 'е'),
                ('и', '', 'ам', 'и', 'ами', 'ах'),
                ('', '', 'ам', '', 'ами', 'ах')),  # 10^3
            2: (('', 'а', 'у', '', 'ом', 'е'),
                ('а', 'ов', 'ам', 'а', 'ами', 'ах'),
                ('ов', 'ов', 'ам', 'ов', 'ами', 'ах'))
        }

        self.CURRENCY_FORMS = {
            'RUB': (
                (('рубль', 'рубля', 'рублю', 'рубль', 'рублём', 'рубле'),
                 ('рубля', 'рублей', 'рублям', 'рубля', 'рублями', 'рублях'),
                 ('рублей', 'рублей', 'рублям', 'рублей', 'рублями', 'рублях')),
                (('копейка', 'копейки', 'копейке', 'копейку', 'копейкой', 'копейке'),
                 ('копейки', 'копеек', 'копейкам', 'копейки', 'копейками', 'копейках'),
                 ('копеек', 'копеек', 'копейкам', 'копеек', 'копейками', 'копейках'))
            ),
            'EUR': (
                ('евро', 'евро', 'евро'),
                (('цент', 'цента', 'центу', 'цент', 'центом', 'центе'),
                 ('цента', 'центов', 'центам', 'цента', 'центами', 'центах'),
                 ('центов', 'центов', 'центам', 'центов', 'центами', 'центах'))
            ),
            'USD': (
                (('доллар', 'доллара', 'доллару', 'доллар', 'долларом', 'долларе'),
                 ('доллара', 'долларов', 'долларам', 'доллара', 'долларами', 'долларах'),
                 ('долларов', 'долларов', 'долларам', 'долларов', 'долларами', 'долларах')),
                (('цент', 'цента', 'центу', 'цент', 'центом', 'центе'),
                 ('цента', 'центов', 'центам', 'цента', 'центами', 'центах'),
                 ('центов', 'центов', 'центам', 'центов', 'центами', 'центах'))
            ),
            'UAH': (
                (('гривна', 'гривны', 'гривне', 'гривну', 'гривной', 'гривне'),
                 ('гривны', 'гривен', 'гривнам', 'гривны', 'гривнами', 'гривнах'),
                 ('гривен', 'гривен', 'гривнам', 'гривен', 'гривнами', 'гривнах')),
                (('копейка', 'копейки', 'копейке', 'копейку', 'копейкой', 'копейке'),
                 ('копейки', 'копеек', 'копейкам', 'копейки', 'копейками', 'копейках'),
                 ('копеек', 'копеек', 'копейкам', 'копеек', 'копейками', 'копейках'))
            ),
            'KZT': (
                ('тенге', 'тенге', 'тенге'),
                (('тиын', 'тиына', 'тиыну', 'тиын', 'тиыном', 'тиыне'),
                 ('тиына', 'тиынов', 'тиынам', 'тиына', 'тиынами', 'тиынах'),
                 ('тиынов', 'тиынов', 'тиынам', 'тиынов', 'тиынами', 'тиынах'))
            ),
        }

        self.NEGWORD = "минус"
        self.POINTWORD = "запятая"

        self.ORD_SUFFIXES = {0: ('ый', 'ого', 'ому', 'ый', 'ым', 'ом'),
                             1: ('ое', 'ого', 'ому', 'ое', 'ым', 'ом'),
                             2: ('ая', 'ой', 'ой', 'ую', 'ой', 'ой'),
                             3: ('ые', 'ых', 'ым', 'ые', 'ыми', 'ых')}

        self.ORD_THREE = {0: ('ий', 'ьего', 'ьему', 'ий', 'ьим', 'ьем'),
                          1: ('ье', 'ьего', 'ьему', 'ье', 'ьим', 'ьем'),
                          2: ('ья', 'ьей', 'ьей', 'ью', 'ьей', 'ьей'),
                          3: ('ьи', 'ьих', 'ьим', 'ьи', 'ьими', 'ьих')}

        self.ORD_STEMS = {"ноль": "нулев",
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
        for x in self.THOUSANDS_BASE.values():
            self.ORD_STEMS[x] = x + 'н'

        self.ORDS = {"ноль": "нулевой",
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
        self.ORDS_SINGLE = {"один": "одна",
                            "одна": "одна",
                            "одного": "одна",
                            "одной": "одна"}
        self.ORDS_FEMININE = {"один": "одна",
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
                              "девять": "девяти"}
        self.ORDS_FEMININE.update(self.ORDS_SINGLE)

        self.OY_ORDINALS = ('ноль', 'два', 'шесть', 'семь', 'восемь')

class Num2Word_RU(Num2Word_Base):

    def setup(self):
        self.lr = LanguageResources_RU()

    def to_cardinal(self, number, case=0):
        n = str(number).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
            return u'%s %s %s' % (
                self._int2word(int(left), case=case),
                self.lr.POINTWORD,
                self._int2word(int(right), case=case)
            )
        else:
            return self._int2word(int(n), case=case)

    def to_ordinal(self, number, num_gender=0, case=0):
        n = str(number)
        return self.to_ordinal_num(int(n), num_gender=num_gender, case=case)

    def to_year(self, number, case=0):
        return self.to_ordinal(number, num_gender=0, case=case)

    def to_fraction(self, number, case=0):
        n = str(number)
        m = re.match('(\d+)\/(\d+)', n)
        if m:
            nominator = m.group(1)
            denominator = m.group(2)
            return self.to_cardinal(nominator, case) + ' ' + self.to_ordinal(denominator, num_gender=3, case=1)
        else:
            raise ValueError(number)

    def to_currency(self, val, currency='EUR', cents=True, separator='', case=0, currency_forms=None):
        '''
        currency_forms: tuple (,)
        '''
        my_val = str(val).replace(',', '.')
        left, right, is_negative = parse_currency_parts(my_val)
        if currency_forms:
            cr1, cr2 = currency_forms
            currency_base_form = currency
        else:
            currency_base_form = None
            try:
                cr1, cr2 = self.lr.CURRENCY_FORMS[currency]
            except KeyError:
                raise NotImplementedError(
                    'Currency code "%s" not implemented for "%s"' %
                    (currency, self.__class__.__name__))

        minus_str = "%s " % self.negword if is_negative else ""
        cents_str = self._cents_verbose(right, currency, case=case) \
            if cents else self._cents_terse(right, currency) # TODO: what if you need to say 25,6 млн долларов

        output = minus_str + self.to_cardinal(left, case=case) + ' '
        output += self.pluralize(left, cr1, currency_base_form=currency_base_form, case=case)
        if cents_str:
            output += separator + ' ' + cents_str + ' '
            output += self.pluralize(right, cr2, currency_base_form=currency_base_form, case=case)
        return output

    def decline(self, forms, currency_base_form=None, case=0): # select the right noun case
        if isinstance(forms, tuple):
            if currency_base_form:
                return currency_base_form + forms[case]
            return forms[case]
        return forms

    def pluralize(self, n, forms, currency_base_form=None, case=0): # select the right plural form of e.g. "dollars"
        if not forms:
            return ''
        if n == 0:
            return self.decline(forms[2], currency_base_form, case)
        if n % 10 == 1:
            return self.decline(forms[0], currency_base_form, case)
        elif n % 10 <= 4 and n % 20 < 10: # the second condition means that numbers like 11, 12, 13, 14 use form 2
            return self.decline(forms[1], currency_base_form, case)
        return self.decline(forms[2], currency_base_form, case)

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
        return self.lr.THOUSANDS_BASE[i] + self.lr.THOUSANDS[m][form][case]

    def process_ordinal_word(self, word, ending):
        if word[:-3] in self.lr.ORDS_FEMININE:
            word = self.lr.ORDS_FEMININE.get(word[:-3], word) + "сот" + ending
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

    def to_ordinal_num(self, number, num_gender=0, case=0):
    # optional num_gender: 0 (male), 1 (neutral), 2 (female) , 3 (plural)
    # optional case: from 0 (nominative) to 5 (prepositional)
        self.verify_ordinal(number)
        c = 1 if (number % 1000) == 0 else 0
        outwords = self.to_cardinal(number, case=c).split(' ')
        lastword = outwords[-1].lower()
        if num_gender == 0 and case in [0, 3] and lastword in self.lr.OY_ORDINALS:
            ending = self.lr.ORD_SUFFIXES[2][1] # ой
        else:
            ord_suffixes = self.lr.ORD_THREE if lastword == self.lr.ONES[3][0] else self.lr.ORD_SUFFIXES
            ending = ord_suffixes[num_gender][case]
        try:
            if len(outwords) > 1:
                if outwords[-2] in self.lr.ORDS_FEMININE:
                    outwords[-2] = self.lr.ORDS_FEMININE.get(outwords[-2], outwords[-2])
                for i in range(0, 3):
                    if lastword[:-i] in self.lr.THOUSANDS_BASE.values():
                        outwords[-2] = self.lr.ORD_MAP.get(outwords[-2], outwords[-2])
                        if len(outwords) > 2:
                            outwords[-3] = self.lr.ORD_MAP.get(outwords[-3], outwords[-3])
                        lastword = lastword[:-i]
                        break
            if len(outwords) == 3:
                if outwords[-3] in self.lr.ORDS_SINGLE.keys():
                    outwords[-3] = ''
            lastword = self.lr.ORD_STEMS[lastword] + ending
        except KeyError: # for everything not in ORD_STEMS
            lastword = self.process_ordinal_word(lastword, ending)
        outwords[-1] = self.title(lastword)
        return " ".join(outwords).strip()

    def _cents_verbose(self, number, currency, case=0):
        if number == 0: # don't say "zero cents"
            return ''
        return self._int2word(number, currency == 'RUB', case=case)


    def _int2word(self, n, feminine=False, case=0):
        m = n
        result = ''
        if n < 0:
            m = abs(n)
            result += self.lr.NEGWORD + ' '
        return self.my_int2word(m, feminine=feminine, case=case)

    def my_int2word(self, n, feminine=False, case=0):
        if n == 0:
            return self.lr.ZERO[case]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1
            if x == 0:
                continue
            n1, n2, n3 = get_digits(x)
            if n3 > 0:
                words.append(self.lr.HUNDREDS[n3][case])
            if n2 > 1:
                words.append(self.lr.TWENTIES[n2][case])
            if n2 == 1:
                words.append(self.lr.TENS[n1][case])
            elif n1 > 0:
                if i == 1 or (feminine and i == 0):
                    ones = self.lr.ONES_FEMININE
                else:
                    ones = self.lr.ONES
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
    yo.lr.print_all_forms()

    import sys
    for line in ['14.22 10 150 2го 22-го 56/171 34х 1991 14.2 1016.53']:
        nums = line.strip().split()
        for num in nums:
            for case_name, case in yo.lr.NOUN_CASES.items():
                try:
                    print(case_name, num, yo.to_fraction(num, case=case))
                except ValueError:
                    pass
                try:
                    print(case_name, num, yo.to_year(num, case=case))
                except ValueError:
                    pass
                try:
                    print(case_name, num, yo.to_cardinal(num, case=case))
                except ValueError:
                    pass
                try:
                    print(case_name, num, yo.to_currency(num, currency='RUB', case=case))
                    print(case_name, num, yo.to_currency(num, currency='USD', case=case))
                    print(case_name, num, yo.to_currency(num, currency='EUR', case=case))
                except ValueError:
                    pass

            for num_gender_name, num_gender in yo.lr.GENDERS.items():
                for case_name, case in yo.lr.NOUN_CASES.items():
                    try:
                        print(num_gender_name, case_name, num, yo.to_ordinal(num, num_gender=num_gender, case=case))
                    except ValueError:
                        pass

        # sys.stdout.write("\n")

