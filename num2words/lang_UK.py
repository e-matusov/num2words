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
        x = val[1]
        if x.endswith('и') or x.endswith('а'):
            x = x[:-1]
        result[val[0]] = x
    return result

def print_forms(mapping, out, pref=''):
    for v in mapping.values():
        for x in v:
            print(pref+x, file=out)

def clone_case_variants(six_tuple):
    '''add identical case variants for cases from genetive to prepositional'''
    assert(len(six_tuple) == 6)
    out = []
    for n, entry in enumerate(six_tuple):
        out.append(entry)
        if n > 0:
            out.append(entry) # copy the variant
    return out

class LanguageResources_UK:

    def print_all_forms(self, filename):
        if filename:
            out = open(filename, 'wt')
        else:
            import sys
            out = sys.stdout
        for v in self.ZERO:
            print(v, file=out)
        print_forms(self.ONES_FEMININE, out)
        print_forms(self.ONES, out)
        print_forms(self.TENS, out)
        print_forms(self.TWENTIES, out)
        print_forms(self.HUNDREDS, out)
        print(self.NEGWORD, file=out)
        print(self.POINTWORD, file=out)

        for v in self.THOUSANDS_BASE.values():
           for x in self.THOUSANDS.values():
               for y in x:
                   for z in y:
                       print(v+z, file=out)
        for v in self.ORD_STEMS.values():
            print_forms(self.ORD_SUFFIXES, out, v)
            print_forms(self.ORD_THREE, out, v)
        for x in self.ORDS_FEMININE.values():
            print(x, file=out)

    def __init__(self):
        self.NOUN_CASES = {'nom': 0,
                           'gen': (1, 2),
                           'dat': (3, 4),
                           'acc': (5, 6),
                           'inst': (7, 8),
                           'prep': (9, 10)} # including variants for numbers especially
        self.GENDERS = {'masc': 0,
                        'neut':  1,
                        'fem': 2,
                        'plur': 3} # technically not gender, but...

        self.ZERO = ('нуль', 'нуля', 'нуля', 'нулю', 'нулеві', 'нуль', 'нуль', 'нулем', 'нулем', 'нулі', 'нулю')
        self.ONES_FEMININE = {
            1: ('одна', 'однієї', 'одної', 'одній', 'одній', 'одну', 'одну', 'однією', 'одною', 'одній', 'одній'),
            2: ('дві', 'двох', 'двох', 'двом', 'двом', 'дві', 'двох', 'двома', 'двома', 'двох', 'двох'),
            3: ('три', 'трьох', 'трьох', 'трьом', 'трьом', 'три', 'трьох', 'трьома', 'трьома', 'трьох', 'трьох'),
            4: ('чотири', 'чотирьох', 'чотирьох', 'чотирьом', 'чотирьом', 'чотири', 'чотирьох', 'чотирма', 'чотирма', 'чотирьох', 'чотирьох'),
            5: ("п'ять", "п'яти", "п'ятьох", "п'яти", "п'ятьом", "п'ять", "п'ятьох", "п'ятьмя", "п'ятьома", "п'яти", "п'ятьох"),
            6: ('шiсть', "шести", "шістьох", "шести", "шістьом", "шість", "шістьох", "шістма", "шістьома", "шести", "шістьох"),
            7: ('сім', "семи", "сімох", "семи", "сімом", "сім", "сімох", "сімома", "сьома", "семи", "сімох"),
            8: ('вісім', "восьми", "вісьмох", "восьми", "вісьмом", "вісім", "вісьмох", "вісьма", "вісьмома", "восьми", "вісьмох"),
            9: ('дев\'ять', "дев'яти", "дев'ятьох", "дев'яти", "дев'ятьом", "дев'ять", "дев'ятьох", "дев'ятьма", "дев'ятьома", "дев'яти", "дев'ятьох"),
        }
        self.ONES = self.ONES_FEMININE.copy()
        self.ONES[1] = ('один', 'одного', 'одного', 'одному', 'одному', 'один', 'одного', 'одним', 'одним', 'однім', 'одному')
        self.ONES[2] = ('два', 'двох', 'двох', 'двом', 'двом', 'два', 'двох', 'двома', 'двома', 'двох', 'двох')

        tens_suffixes = ('ь', 'и', 'ьох', 'и', 'ьом', 'ь', 'ьох', 'ьма', 'ьома', 'и', 'ьох')
        tens_stems = ('десять', 'одинадцять', 'дванадцять', 'тринадцять', 'чотирнадцять', "п'ятнадцять",
                      'шістнадцять', 'сімнадцять', 'вісімнадцять', "дев'ятнадцять")
        self.TENS = {}
        for n, stem in enumerate(tens_stems):
            forms = []
            self.TENS[n] = ()
            for suff in tens_suffixes:
                forms.append(stem[:-1] + suff) # remove the soft sign from stem first
            self.TENS[n] = tuple(forms)
        self.ORD_MAP = get_ord_map(self.TENS)

        twenties_stems = ('двадцят', 'тридцят', 'сорок', "п'ятдесят", 'шістдесят', 'сімдесят', 'вісімдесят')
        self.TWENTIES = {}
        for n, stem in enumerate(twenties_stems):
            forms = []
            for suff in tens_suffixes:
                forms.append(stem + suff) # start from 2
            self.TWENTIES[n+2] = tuple(forms)
        self.TWENTIES[4] = ('сорок', 'сорока', 'сорока', 'сорока', 'сорока', 'сорок', 'сорок', 'сорока', 'сорока', 'сорока', 'сорока') # overwrite
        self.TWENTIES[9] = ("дев'яносто", "дев'яноста", "дев'яноста", "дев'яноста", "дев'яноста", "дев'яносто", "дев'яносто",
                            "дев'яноста", "дев'яноста", "дев'яноста", "дев'яноста")
        self.ORD_MAP.update(get_ord_map(self.TWENTIES))

        self.HUNDREDS = {
            1: clone_case_variants(('сто', 'ста', 'стам', 'сто', 'ста', 'ста')),
            2: clone_case_variants(('двісті', 'двохсот', 'двомстам', 'двісті', 'двомастами', 'двохстах')),
            3: clone_case_variants(('триста', 'трьохсот', 'трьомстам', 'триста', 'трьомастами', 'трьохстах')),
            4: clone_case_variants(('чотириста', 'чотирьохсот', 'чотирьомстам', 'чотириста', 'чотирмастами', 'чотирьохстах')),
            5: clone_case_variants(("п'ятсот", "п'ятисот", "п'ятистам", "п'ятсот", "п'ятьмастами", "п'ятистах")),
            6: clone_case_variants(('шістсот', 'шестисот', 'шестистам', 'шістсот', 'шістьмастами', 'шестистах')),
            7: clone_case_variants(('сімсот', 'семисот', 'семистам', 'сімсот', 'сьомастами', 'семистах')),
            8: clone_case_variants(('вісімсот', 'восьмисот', 'восьмистам', 'восьмисот', 'восьмистами', 'восьмистах')),
            9: clone_case_variants(("дев'ятсот", "дев'ятисот", "дев'ятистам", "дев'ятсот", "дев'ятьмастами", "дев'ятистах"))
        }
        self.HUNDREDS[5][8] = "п'ятьомастами" # variant instrumental case
        self.HUNDREDS[7][8] = "сімомастами" # variant instrumental case
        self.HUNDREDS[9][8] = "дев'ятьомастами" # variant instrumental case
        self.ORD_MAP.update(get_ord_map(self.HUNDREDS))

        THOUSANDS = {
            1: ('тисяча', 'тисячі', 'тисяч'),  # 10^3
            2: ('мільйон', 'мільйони', 'мільйонів'),  # 10^6
            3: ('мільярд', 'мільярди', 'мільярдів'),  # 10^9
            4: ('трильйон', 'трильйони', 'трильйонів'),  # 10^12
            5: ('квадрильйон', 'квадрильйони', 'квадрильйонів'),  # 10^15
            6: ('квінтильйон', 'квінтильйони', 'квінтильйонів'),  # 10^18
            7: ('секстильйон', 'секстильйони', 'секстильйонів'),  # 10^21
            8: ('септильйон', 'септильйони', 'септильйонів'),  # 10^24
            9: ('октильйон', 'октильйони', 'октильйонів'),  # 10^27
            10: ('нонільйон', 'нонільйони', 'нонiльйонів'),  # 10^30
        }

        self.THOUSANDS_BASE = {
            1: 'тисяч',
            2: 'мільйон',
            3: 'мільярд',
            4: 'трильйон',
            5: 'квадрильйон',
            6: 'квінтильйон',
            7: 'секстильйон',
            8: 'септильйон',
            9: 'октильйон',
            10: 'нонільйон'
        }

        self.THOUSANDS = {
            1: (clone_case_variants(('а', 'і', 'і', 'у', 'ею', 'і')),
                clone_case_variants(('і', '', 'ам', 'і', 'ами', 'ах')),
                clone_case_variants(('', '', 'ам', '', 'ами', 'ах'))),  # 10^3
            2: (('', 'а', 'а', 'у', 'ові', '', '', 'ом', 'ом', 'і', 'е'), # including the "calling" case as the last variant
                clone_case_variants(('а', 'ів', 'ам', 'а', 'ами', 'ах')),
                clone_case_variants(('ів', 'ів', 'ам', 'ів', 'ами', 'ах')))
        }
        self.CURRENCY_FORMS = {
            'RUB': (
                (clone_case_variants(('рубель', 'рубля', 'рублю', 'рубель', 'рублём', 'рублю')),
                 clone_case_variants(('рубля', 'рублів', 'рублям', 'рубля', 'рублями', 'рублях')),
                 clone_case_variants(('рублів', 'рублів', 'рублям', 'рублі', 'рублями', 'рублях'))),
                (clone_case_variants(('копійка', 'копійки', 'копійці', 'копійку', 'копійкою', 'копійці')),
                 clone_case_variants(('копійки', 'копійок', 'копійкам', 'копійки', 'копійками', 'копійках')),
                 clone_case_variants(('копійок', 'копійок', 'копійкам', 'копійок', 'копійками', 'копійках')))
            ),
            'EUR': (
                ('євро', 'євро', 'євро'),
                (('цент', 'цента', 'цента', 'центу', 'центові', 'цент', 'цент', 'центом', 'центом', 'центі', 'центі'),
                 ('центі', 'цента', 'центі', 'центам', 'центам', 'центі', 'цента', 'центами', 'центами', 'центах', 'центі'),
                 ('центів', 'центів', 'центів', 'центам', 'центам', 'центі', 'центи', 'центами', 'центами', 'центах', 'центі')),
            ),
            'USD': (
                (('долар', 'долара', 'долара', 'долару', 'доларові', 'долар', 'долар', 'доларом', 'доларом', 'доларі', 'доларі'),
                 ('долара', 'доларів', 'доларів', 'доларам', 'доларам', 'долара', 'долара', 'доларами', 'доларами', 'доларах', 'доларах'),
                 ('доларів', 'доларів', 'доларів', 'доларам', 'доларам', 'доларів', 'доларів', 'доларами', 'доларами', 'доларах', 'доларах')),
                (('цент', 'цента', 'цента', 'центу', 'центові', 'цент', 'цент', 'центом', 'центом', 'центі', 'центі'),
                 ('центі', 'цента', 'центі', 'центам', 'центам', 'центі', 'цента', 'центами', 'центами', 'центах', 'центі'),
                 ('центів', 'центів', 'центів', 'центам', 'центам', 'центі', 'центи', 'центами', 'центами', 'центах', 'центі')),
            ),
            'UAH': (
                (clone_case_variants(('гривня', 'гривні', 'гривні', 'гривню', 'гривнею', 'гривні')),
                 clone_case_variants(('гривні', 'гривень', 'гривням', 'гривні', 'гривнями', 'гривнах')),
                 clone_case_variants(('гривень', 'гривень', 'гривням', 'гривень', 'гривнями', 'гривнях'))),
                (clone_case_variants(('копійка', 'копійки', 'копійці', 'копійку', 'копійкою', 'копійці')),
                 clone_case_variants(('копійки', 'копійок', 'копійкам', 'копійки', 'копійками', 'копійках')),
                 clone_case_variants(('копійок', 'копійок', 'копійкам', 'копійок', 'копійками', 'копійках')))
            )
        }

        self.NEGWORD = "мiнус"
        self.POINTWORD = "кома"

        # for 3 genders + plural
        self.ORD_THREE = {0: ('ій', 'ього', 'ього', 'ьому', 'ьому', 'ього', 'ій', 'ім', 'ім', 'ім', 'ьому'),
                          1: ('є', 'ього', 'ього', 'ьому', 'ьому', 'є', 'є', 'ім', 'ім', 'ім', 'ьому'),
                          2: ('я', 'ьої', 'ьої', 'ій', 'ій', 'ю', 'ю', 'ьою', 'ьою', 'ій', 'я'),
                          3: ('і', 'іх', 'іх', 'ім', 'ім', 'і', 'іх', 'іми', 'іми', 'іх', 'і')}
        self.ORD_SUFFIXES = {0: ('ий', 'ого', 'ого', 'ому', 'ому', 'ий', 'у', 'им', 'им', 'ім', 'ому'),
                             1: ('е', 'ого', 'ого', 'ому', 'ому', 'е', 'е', 'им', 'им', 'ім', 'ому'),
                             2: ('а', 'ої', 'ої', 'ій', 'ій', 'у', 'у', 'ою', 'ою', 'ій', 'ій'),
                             3: ('і', 'их', 'их', 'им', 'им', 'и', 'их', 'ими', 'ими', 'их', 'их')}

        self.ORD_STEMS = {"нуль": "нульов",
                          "один": "перш",
                          "два": "друг",
                          "три": "трет",
                          "чотири": "четверт",
                          "п'ять": "п'ят",
                          "шiсть": "шост",
                          "сім": "сьом",
                          "вісім": "восьм",
                          "дев\'ять": "дев'ят",
                          "сто": "сот"}
        self.FLOAT_INTEGER_PART = 'ціл'

        for x in self.THOUSANDS_BASE.values():
            self.ORD_STEMS[x] = x + 'н'

        self.ORDS_SINGLE = {"один": "одна",
                            "одна": "одна",
                            "одного": "одна",
                            "одної": "одна",
                            "однієї": "одна"
                           }
        self.ORDS_FEMININE = {}
        for key, val in self.ONES_FEMININE.items():
            self.ORDS_FEMININE[key] = val[1] # genetive case: "дві": "двох",
        self.ORDS_FEMININE.update(self.ORDS_SINGLE) # this should overwrite for "одна"

class Num2Word_UK(Num2Word_Base):

    def setup(self):
        self.lr = LanguageResources_UK()

    def to_cardinal(self, number, case=0, feminine=False, adjust_accusative=True, use_float_words=False, connector=None):
        n = str(number).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
            float_word_left = 0 if use_float_words else None
            float_word_right = 10**len(right) if use_float_words else None
            point_word = connector if connector != None else self.lr.POINTWORD
            if len(point_word):
                point_word += ' '
            return u'%s %s%s' % (
                self._int2word(int(left), case=case, feminine=feminine, float_word=float_word_left),
                point_word,
                self._int2word(int(right), case=case, feminine=feminine, float_word=float_word_right)
            )
        else:
            return self._int2word(int(n), case=case, feminine=feminine, adjust_accusative=adjust_accusative)

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

            res = self.to_cardinal(nominator, case=case, feminine=True) + ' '
            n = int(nominator)
            if n % 10 == 1 and (n % 100 != 11):
                num_gender = 2
                denom_case = case
            else:
                num_gender = 3
                denom_case = 1 if case in [0, 3] else case
            res += self.to_ordinal(denominator, num_gender=num_gender, case=denom_case)
            return res
        else:
            raise ValueError(number)

    def to_currency(self, val, currency='EUR', cents=True, separator='', case=0):
        '''
        currency_forms: tuple (,)
        '''
        my_val = str(val).replace(',', '.')
        left, right, is_negative = parse_currency_parts(my_val)
        currency_unit_reading = ''
        if isinstance(currency, list): # then the expected format is (currency_base_form, cr1))
            for (currency_base_form, cr1) in currency:
                if not cr1:
                    cr1, cr2 = self.lr.CURRENCY_FORMS[currency_base_form]
                    currency_base_form=None
                currency_unit_reading += ' ' + self.pluralize(left, cr1, case=case,
                                                              currency_base_form=currency_base_form)
            cr2 = None
        else:
            currency_base_form = None
            try:
                cr1, cr2 = self.lr.CURRENCY_FORMS[currency]
                currency_unit_reading += ' ' + self.pluralize(left, cr1, case=case,
                                                              currency_base_form=currency_base_form)
            except KeyError:
                raise NotImplementedError(
                    'Currency code "%s" not implemented for "%s"' %
                    (currency, self.__class__.__name__))

        minus_str = "%s " % self.negword if is_negative else ""
        cents_str = self._cents_verbose(right, currency, case=case) \
            if cents else self._cents_terse(right, currency)

        output = minus_str + self.to_cardinal(left, case=case, adjust_accusative=False)
        output += currency_unit_reading
        if cents_str:
            output += separator + ' ' + cents_str
        if cr2:
            output += ' ' + self.pluralize(right, cr2, currency_base_form=currency_base_form, case=case)
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
        elif n % 10 <= 4 and (n % 100 > 14 or n % 100 <= 10): # the second condition means that numbers like 11, 12, 13, 14 use form 2
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
        if word in self.lr.ORD_MAP:
            word = self.lr.ORD_MAP[word] + ending
        elif word[:-3] in self.lr.ORDS_FEMININE:
            word = self.lr.ORDS_FEMININE.get(word[:-3], word) + "сот" + ending
        elif word[-1] == "ь" or word[-2] == "т":
            word = word[:-1] + ending
        elif word[-1] == "к": # 40 - сорок
            word = word + "ов" + ending
        # elif word[-5:] == "десят": # does not apply to UK, only to RU
        #    word = word.replace('ь', 'и') + ending
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
        c = 1 if (number != 0) and (number % 1000) == 0 else 0
        outwords = self.to_cardinal(number, case=c).split(' ')
        lastword = outwords[-1].lower()
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
        return self._int2word(number, currency == 'UAH', case=case)


    def _int2word(self, n, feminine=False, case=0, adjust_accusative=True, float_word=None):
        m = n
        result = ''
        if n < 0:
            m = abs(n)
            result += self.lr.NEGWORD + ' '
        return self.my_int2word(m, feminine=feminine, case=case,
                                adjust_accusative=adjust_accusative, float_word=float_word)

    def my_int2word(self, n, feminine=False, case=0, adjust_accusative=True, float_word=None):
        if float_word != None: # e.g. 7 целых 5 десятых
            float_word_realization = self.to_fraction(str(n) + '/' + str(float_word), case=case)
            if float_word == 0:
                float_word_realization = float_word_realization.replace(self.lr.ORD_STEMS[self.lr.ZERO[0]],
                                                                        self.lr.FLOAT_INTEGER_PART)
            return float_word_realization

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
                if adjust_accusative and not feminine and mycase == 3:
                    if i==0 and n1 <= 4 and (n2+n3) == 0:
                        mycase = 1 # genetive form for individual digits <=4 only, only for stand-alone small numbers
                                   #    e.g. я вижу двух человек BUT: я вижу два миллиона
                words.append(ones[n1][mycase])

            if i > 0:
                words.append(self.pluralize_thousand_potentials(x, i, case))
        return ' '.join(words)


if __name__ == '__main__':
    yo = Num2Word_UK()
#    yo.lr.print_all_forms('num2words.wordforms.uk')

    import sys
    for line in sys.stdin: # ['300 301 311 1/4 14.22 10 150 2го 22-го 56/171 34х 1991 14.2 1016.53 0']:
        nums = line.strip().split()
        for num in nums:
            for case_name, case_variants in yo.lr.NOUN_CASES.items():
                c = case_variants if isinstance(case_variants, tuple) else [case_variants]
                for case in c:
                    try:
                        print(case_name, num, yo.to_cardinal(num, case=case))
                    except ValueError:
                        pass
            for num_gender_name, num_gender in yo.lr.GENDERS.items():
                for case_name, case_variants in yo.lr.NOUN_CASES.items():
                    c = case_variants if isinstance(case_variants, tuple) else [case_variants]
                    for case in c:
                        try:
                            print(num_gender_name, case_name, num, yo.to_ordinal(num, num_gender=num_gender, case=case))
                        except ValueError:
                            pass

        # sys.stdout.write("\n")

