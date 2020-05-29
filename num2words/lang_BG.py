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
import sys

def print_forms(mapping, out, pref=''):
    for v in mapping.values():
        for x in v:
            print(pref+x, file=out)

class LanguageResources_BG:

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
        for x in self.THOUSANDS.values():
            for y in x:
               print(y, file=out)
        for v in self.ORD_STEMS_1.values():
            print_forms(self.ORD_SUFFIXES_1, out, v)
        for v in self.ORD_STEMS_2.values():
            print_forms(self.ORD_SUFFIXES_2, out, v)

    def __init__(self):
        self.NOUN_CASES = {'nom': 0, # nominative
                           'detnom': 1} # determinitive form
        self.GENDERS = {'masc': 0,
                        'neut':  1,
                        'fem': 2,
                        'plur': 3} # technically not gender, but...

        self.ZERO = ('нула', 'нулата')
        self.ZERO_ORDINAL = (('нулев', 'нулевте'),
                             ('нулево', 'нулевоте'),
                             ('нулева', 'нулевата'),
                             ('нулеви', 'нулевите'))

        self.number_offsets = [3, 1, 1] # ones, tens, hundreds, thousands ... max offset (e.g. 3 offset levels of 11, 21, 31 in ONES)
        self.ONES_FEMININE = {
            1: ('една', 'едната'),
            11: ('един', 'единия'),
            21: ('едно', 'едното'),
            31: ('един', 'единият'),
            2: ('две', 'двете'),
            12: ('двама', 'двамата'),
            22: ('два', 'двата'),
            3: ('три', 'трите'),
            13: ('трима', 'тримата'),
            4: ('четири', 'четирите'),
            14: ('четирима', 'четиримата'),
            5: ('пет', 'петте'),
            15: ('петима', 'петимата'),
            6: ('шест', 'шестте'),
            16: ('шестима', 'шестимата'),
            7: ('седем', 'седемте'),
            8: ('осем', 'осемте' ),
            9: ('девет', 'деветте'),
        }
        self.ONES = self.ONES_FEMININE.copy()
        self.ONES[1] = ('един', 'единия') # ALSO: единият !
        self.ONES[2] = ('два', 'двата')
        x = 'четиринадесет[_/те]|четиринайсет[_/те]'

        self.TENS = { 0: ('десет', 'десетте'),
                      1: ('единадесет', 'единадесетте'),
                      11: ('единайсет', 'единайсетте'),
                      2: ('дванадесет', 'дванадесетте'),
                      12: ('дванайсет', 'дванайсетте'),
                      3: ('тринадесет', 'тринадесетте'),
                      13: ('тринайсет', 'тринайсетте'),
                      4: ('четиринадесет', 'четиринадесетте'),
                      14: ('четиринайсет', 'четиринайсетте'),
                      5: ('петнадесет', 'петнадесетте'),
                      15: ('петнайсет', 'петнайсетте'),
                      6: ('шестнадесет', 'шестнадесетте'),
                      16: ('шестнайсет', 'шесинайсетте'),
                      7: ('седемнадесет', 'седемнадесетте'),
                      17: ('седемнайсет', 'седемнайсетте'),
                      8: ('осемнадесет', 'осемнадесетте'),
                      18: ('осемнайсет', 'осемнайсетте'),
                      9: ('деветнадесет', 'деветнадесетте'),
                      19: ('деветнайсет', 'деветнайсетте'),
                    }

        self.TWENTIES = {
                         2: ('двадесет', 'двадесетте'),
                         12: ('двайсет', 'двайсетте'),
                         3: ('тридесет', 'тридесетте'),
                         13: ('трийсет', 'трийсетте'),
                         4: ('четиридесет', 'четиридесетте'),
                         14: ('четирийсет', 'четирийсетте'),
                         5: ('петдесет', 'петдесетте'),
                         6: ('шестдесет', 'шестдесетте'),
                         16: ('шейсет', 'шейсетте'),
                         7: ('седемдесет', 'седемдесетте'),
                         8: ('осемдесет', 'осемдесетте'),
                         9: ('деветдесет', 'деветдесетте'),
                         }

        self.HUNDREDS = {
            1: ('сто', 'стоте'),
            2: ('двеста', 'двестата'),
            12: ('двесте', 'двестете'),
            3: ('триста', 'тристата'),
            4: ('четиристотин', 'четиристотинте'),
            5: ("петстотин", "петстотинте"),
            6: ('шестстотин', 'шестстотинте'),
            7: ('седемстотин', 'седемстотинте'),
            8: ('осемстотин', 'осемстотинте'),
            9: ("деветстотин", "деветстотинте")
        }

        self.THOUSANDS = {
            1: ('хиляди', 'хилядата'),  # 10^3
            2: ('милион', 'милионте'),  # 10^6
            3: ('милиард', 'милиардте'),  # 10^9
            4: ('трилион', 'трилионте'),  # 10^12
            5: ('квадрилион', 'квадрилионте'),  # 10^15
            6: ('квинтилион', 'квинтилионте'),  # 10^18
            7: ('секстилион', 'секстилионте'),  # 10^21
            8: ('септилион', 'септилионте'),  # 10^24
            9: ('октилион', 'октилионте',),  # 10^27
            10: ('нонилион', 'нонилионте'),  # 10^30
        }

        self.THOUSANDS_BASE = {
            1: 'хиляд',
            2: 'милион',
            3: 'милиард',
            4: 'трилион',
            5: 'квадрилион',
            6: 'квинтилион',
            7: 'секстилион',
            8: 'септилион',
            9: 'октилион',
            10: 'нонилион'
        }

        self.CURRENCY_FORMS = {} # will be handled via newtn

        self.AND = 'и'
        self.NEGWORD = "минус"
        self.POINTWORD = "запетая"

        self.ORD_STEMS_1 = {"нула": "нуле",
                            "един": "първ",
                            "два": "втор",
                            "три": "трет",
                            "четири": "четвърт",
                            "пет": "пет",
                            "шест": "шест",
                            "седем": "седм",
                            "осем": "осм",
                            }
        # for 3 genders + plural
        self.ORD_SUFFIXES_1 = {0: ('и', 'ите'),
                               1: ('о', 'оте'),
                               2: ('а', 'ата'),
                               3: ('и', 'ите')}
        self.ORD_STEMS_2 = self.get_ord_map()
        self.ORD_STEMS_2["сто"] =  "стот"
        self.ORD_STEMS_2["двеста"] = "двустот"
        self.ORD_STEMS_2["триста"] = "тристот"
        # for 3 genders + plural
        self.ORD_SUFFIXES_2 = {0: ('ен', 'енте'),
                               1: ('но', 'ноте'),
                               2: ('на', 'ната'),
                               3: ('ни', 'ните')}

        self.FLOAT_INTEGER_PART = 'цел' # цели

        self.ORDS_SINGLE = {"един": "една",
                            "единте": "една",
                            "единия": "една",
                            "единият": "една",
                            "едната": "една",
                           }

    def get_ord_map(self):
        result = {}
        for val in list(self.HUNDREDS.values()) + list(self.THOUSANDS.values()):
            stripped = val[0] # without the determinitive suffix
            if stripped.endswith('ин'):
                stripped = stripped[:-2]
            if stripped.endswith('а'): # хиляда
                stripped = stripped[:-1]
            result[val[0]] = stripped
        return result

        #self.ORDS_FEMININE = {}
        #for key, val in self.ONES_FEMININE.items():
            #self.ORDS_FEMININE[key] = val[1] # genetive case: "дві": "двох",
        #self.ORDS_FEMININE.update(self.ORDS_SINGLE) # this should overwrite for "одна"

class Num2Word_BG(Num2Word_Base):

    def setup(self):
        self.lr = LanguageResources_BG()

    def to_cardinal(self, number, case=0, feminine=False, offsets=[], use_float_words=False, connector=None):
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
            return self._int2word(int(n), case=case, feminine=feminine, offsets=offsets)

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
                denom_case = 0
            else:
                num_gender = 3
                denom_case = 0 # 1 if case in [0, 3] else case
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

    #def pluralize_thousand_potentials(self, n, i, case=0):
        #if n % 100 < 10 or n % 100 > 20:
            #if n % 10 == 1:
                #form = 0
            #elif 5 > n % 10 > 1:
                #form = 1
            #else:
                #form = 2
        #else:
            #form = 2
        #m = 1
        #if i > 1:
            #m = 2
        #return self.lr.THOUSANDS_BASE[i] + self.lr.THOUSANDS[case]

    def to_ordinal_num(self, number, num_gender=0, case=0):
    # optional num_gender: 0 (male), 1 (neutral), 2 (female) , 3 (plural)
    # optional case
        self.verify_ordinal(number)
        if number == 0:
            return self.lr.ZERO_ORDINAL[num_gender][case]

        outwords = self.to_cardinal(number, case=0).split(' ') # use nominative case here!
        if len(outwords) == 3:
            if outwords[-3] in self.lr.ORDS_SINGLE.keys():
                outwords[-3] = ''
        lastword = outwords[-1].lower()
        mod_word = lastword
        if lastword in self.lr.ORD_STEMS_1:
            mod_word = self.lr.ORD_STEMS_1[lastword] + self.lr.ORD_SUFFIXES_1[num_gender][case]
        elif lastword in self.lr.ORD_STEMS_2:
            mod_word = self.lr.ORD_STEMS_2[lastword] + self.lr.ORD_SUFFIXES_2[num_gender][case]
        else:
            mod_word = lastword + self.lr.ORD_SUFFIXES_1[num_gender][case]
        outwords[-1] = self.title(mod_word)
        return " ".join(outwords).strip()

    def _cents_verbose(self, number, currency, case=0):
        if number == 0: # don't say "zero cents"
            return ''
        return self._int2word(number, currency == 'USD', case=case)


    def _int2word(self, n, feminine=False, case=0, offsets=[], adjust_accusative=True, float_word=None):
        m = n
        result = ''
        if n < 0:
            m = abs(n)
            result += self.lr.NEGWORD + ' '
        return self.my_int2word(m, feminine=feminine, case=case, offsets=offsets, float_word=float_word)

    def get_digits_with_offsets(self, chunk, offsets, i):
        triple = get_digits(chunk)
        if i > 0:
            return triple
        for n in range(len(offsets)):
            offset = 10*offsets[n]
            if n == 0 and triple[0] > 0 and (triple[0] + offset) in self.lr.ONES:
                triple[0] += offset
            elif n == 1:
                if triple[1] == 1 and (triple[1] + offset) in self.lr.TENS:
                    triple[1] += offset
                elif triple[1] > 1 and (triple[1] + offset) in self.lr.TWENTIES:
                    triple[1] += offset
            elif n==2 and triple[2] > 0 and (triple[2] + offset) in self.lr.HUNDREDS:
                triple[2] += offset
        return triple

    def my_int2word(self, n, feminine=False, case=0, offsets=[], adjust_accusative=True, float_word=None):
        if float_word != None: # e.g. 7 целых 5 десятых
            float_word_realization = self.to_fraction(str(n) + '/' + str(float_word), case=case)
            if float_word == 0:
                float_word_realization = float_word_realization.replace(self.lr.ORD_STEMS_1[self.lr.ZERO[0]],
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
            n1, n2, n3 = self.get_digits_with_offsets(x, offsets, i)
            n1_case = n2_case = n3_case = 0
            if case == 1 and i == 0:
                if n1 > 0:
                    n1_case = 1
                elif n2 > 0:
                    n2_case = 1
                elif n3 > 0:
                    n3_case = 1
            if n3 > 0:
                words.append(self.lr.HUNDREDS[n3][n3_case])
            if n2 > 1:
                words.append(self.lr.TWENTIES[n2][n2_case])
            if n2 == 1:
                words.append(self.lr.TENS[n1][n1_case])
            elif n1 > 0:
                if i == 1 or (feminine and i == 0):
                    ones = self.lr.ONES_FEMININE
                else:
                    ones = self.lr.ONES
                if n2 > 1:
                    words.append(self.lr.AND)
                words.append(ones[n1][n1_case])
            if i > 0:
                # print("DEBUG", i, n1, n2, n3, len(chunks))
                words.append(self.lr.THOUSANDS[i][0])
        return ' '.join(words)


if __name__ == '__main__':
    yo = Num2Word_BG()
#    yo.lr.print_all_forms('num2words.wordforms.uk')

    import sys
    for line in sys.stdin: # ['0 1 22 23 100 1000 2000']: #  ['1/4 14.22 10 150 2го 22-го 56/171 34х 1991 14.2 1016.53 0']:
        nums = line.strip().split()
        for num in nums:
            for case_name, case_variants in yo.lr.NOUN_CASES.items():
                c = [case_variants]
                for case in c:
                    #try:
                        #print("FRACTION", case_name, num, yo.to_fraction(num, case=case))
                    #except ValueError:
                        #pass
                    #try:
                        #print(case_name, num, yo.to_year(num, case=case))
                    #except ValueError:
                        #pass
                    try:
                        print("CARDINAL:", case_name, num, yo.to_cardinal(num, case=case))
                        print("EXPERIMENTAL:", yo.my_int2word(int(num), feminine=False, case=case, offsets=[1,1,1]))
                    except ValueError:
                        pass
 #                   try:
 #                       print(case_name, num, yo.to_currency(num, currency='RUB', case=case))
 #                       print(case_name, num, yo.to_currency(num, currency='USD', case=case))
 #                       print(case_name, num, yo.to_currency(num, currency='EUR', case=case))
 #                   except:
 #                       pass

            for num_gender_name, num_gender in yo.lr.GENDERS.items():
                for case_name, case_variants in yo.lr.NOUN_CASES.items():
                    c = [case_variants]
                    for case in c:
                        try:
                            print(num_gender_name, case_name, num, yo.to_ordinal(num, num_gender=num_gender, case=case))
                        except ValueError:
                            pass

        # sys.stdout.write("\n")

