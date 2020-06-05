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

class LanguageResources_SK:

    def print_all_forms(self, filename):
        if filename:
            out = open(filename, 'wt')
        else:
            import sys
            out = sys.stdout
        for v in self.ZERO:
            print(v, file=out)
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
# šä’
        self.number_offsets = [4, 1, 1] # ones, tens, hundreds, thousands ... max offset (e.g. 3 offset levels of 11, 21, 31 in ONES)
        self.ONES = self.get_schemes({1: 'jedn[a/ej/ej/u/ej/ou]', # TODO: implement get_schemes
                                      11: 'jed[en/ného/nému/en/nom/ným]',
                                      21: 'jed[no/ného/nému/no/nom/ným]',
                                      31: 'jed[en/ného/nému/ného/nom/ným]', # acc case variant
                                      2: 'dv[e/och/om/e/och/oma]',
                                     12: 'dv[a/och/om/a/och/oma]',
                                     22: 'dvoje',
                                     32: 'dv[aja/och/om/oh/och/oma]', # TODO: check acc if "oh" or "och"
                                      3: 'tr[i/och/om/i/och/oma]',
                                     13: 'tr[aja/och/om/och/och/oma]',
                                     23: 'troje',
                                     33: 'tr[i/och/om/i/och/omi]',
                                     43: 'tr[aja/och/om/och/och/omi]',
                                      4: 'štyr[i/och/om/i/och/mi]',
                                     14: 'štyr[ia/och/om/och/och/mi]',
                                     24: 'štvoro',
                                      5: 'piat[...ät’/ich/im/...ät’/ich/imi]', # TODO: in postprocessing, join the apostrophe with t: ť
                                     15: 'piat[i/ich/im/ich/ich/imi]',
                                     25: 'pätoro',
                                      6: 'šest[’/ich/im/’/ich/imi]'
                                     26: 'šestoro',
                                      7: 'sed[em/mich/mim/em/mich/mimi]',
                                     27: 'sedmoro',
                                      8: 'os[em/mich/mim/em/mich/mimi]',
                                     28: 'osmoro',
                                      9: 'deviat[...ät’/ich/im/...ät’/ich/imi]',
                                     29: 'devätoro'})

        self.TENS = { 0: 'desat[’/ich/im/’/ich/imi]',
                      1: 'jedenást[’/ich/im/’/ich/imi]',
                      2: 'dvanást[’/ich/im/’/ich/imi]',
                      12: 'dvanástoro',
                      3: 'trinást[’/ich/im/’/ich/imi]',
                      4: 'štrnást[’/ich/im/’/ich/imi]',
                      5: 'pätnást[’/ich/im/’/ich/imi]',
                      6: 'šestnást[’/ich/im/’/ich/imi]',
                      7: 'sedemnást[’/ich/im/’/ich/imi]',
                      8: 'osemnást[’/ich/im/’/ich/imi]',
                      9: 'devätnást[’/ich/im/’/ich/imi]',
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
            1: ('хиляди', 'хилядите'),  # 10^3
            11: ('хиляда', 'хилядата'),  # 10^3
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
                            "една": "първ",
                            "две": "втор",
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
        self.ORD_STEMS_2["двесте"] = "двустот"
        self.ORD_STEMS_2["триста"] = "тристот"
        # for 3 genders + plural
        self.ORD_SUFFIXES_2 = {0: ('ен', 'енте'),
                               1: ('но', 'ноте'),
                               2: ('на', 'ната'),
                               3: ('ни', 'ните')}

        self.FLOAT_INTEGER_PART = 'цел' # цели

        self.ORDS_SINGLE = ["една", "един", "едно", "единия", "единият", "едното", "едната"]

    def get_ord_map(self):
        result = {}
        for val in list(self.HUNDREDS.values()) + list(self.THOUSANDS.values()):
            stripped = val[0] # without the determinitive suffix
            if stripped.endswith('ин'):
                stripped = stripped[:-2]
            elif stripped.endswith('а') or stripped == 'хиляди': # хиляда
                stripped = stripped[:-1]
            elif stripped.endswith('он') or stripped.endswith('рд'):
                result[val[0] + 'а'] = stripped
            result[val[0]] = stripped
        return result


class Num2Word_SK(Num2Word_Base):

    def setup(self):
        self.lr = LanguageResources_SK()

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

    def to_ordinal(self, number, offsets=[], num_gender=0, case=0):
        n = str(number)
        return self.to_ordinal_num(int(n), offsets=offsets, num_gender=num_gender, case=case)

    def to_year(self, number, case=0):
        return self.to_ordinal(number, num_gender=0, case=case)

    def to_fraction(self, number, case=0):
        n = str(number)
        m = re.match('(\d+)\/(\d+)', n)
        if m:
            nominator = m.group(1)
            denominator = m.group(2)

            res = self.to_cardinal(nominator, case=case) + ' '
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

    def to_ordinal_num(self, number, offsets=[], num_gender=0, case=0):
    # optional num_gender: 0 (male), 1 (neutral), 2 (female) , 3 (plural)
    # optional case
        self.verify_ordinal(number)
        if number == 0:
            return self.lr.ZERO_ORDINAL[num_gender][case]

        outwords = self.to_cardinal(number, offsets=offsets, case=0).split(' ') # use nominative case here!
        if len(outwords) >= 2: # remove "edin/edna" unless it is at the end
            for n in range(len(outwords) - 1):
                if outwords[n] in self.lr.ORDS_SINGLE: outwords[n] = ''
            if outwords[0].startswith('два') and len(outwords) == 2: # two millionth, three billionth
                outwords[0] = 'дву'

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

    def detnom_form(self, word):
        result = word
        if word == 'един':
            return 'единия'
        if word.endswith('а'):
            return result + 'та'
        else: # if word.endswith('е') or word.endswith('и') or word.endswith('о') or word.endswith('т'):
            return result + 'те'
        return result

    def get_word_with_offset(self, mapping, n, offset, case):
        real_offset = 10 * offset
        idx = n + real_offset
        if idx not in mapping: idx = n
        word = mapping[idx][0]
        if case == 1:
            word = self.detnom_form(word)
        return word

    def get_words_with_offsets(self, chunk, case, offsets, i, insert_and=False, last_chunk=False):
        words = []
        n1, n2, n3 = get_digits(chunk)
        if insert_and and (n3==0): # specific to SK
            words.append(self.lr.AND)
        n1_case = n2_case = n3_case = 0
        if case == 1 and last_chunk:  # this is specific to SK
            if n1 > 0:
                n1_case = 1
            elif n2 > 0:
                n2_case = 1
            elif n3 > 0:
                n3_case = 1
        # print("DEBUG: i, n1/n2/n3, last_chunk", i, n1_case, n2_case, n3_case, last_chunk)
        if n3 > 0:
            words.append(self.get_word_with_offset(self.lr.HUNDREDS, n3, offsets[2], n3_case))
        if n2 > 1:
            words.append(self.get_word_with_offset(self.lr.TWENTIES, n2, offsets[1], n2_case))
        if n2 == 1:
            if n1 == 0: n1_case = n2_case # for 10
            words.append(self.get_word_with_offset(self.lr.TENS, n1, offsets[1], n1_case))
        elif n1 > 0:
            if n2 > 1 or n3 > 0:
                words.append(self.lr.AND)
            offset = offsets[0]
            if i > 1:
                if n1==1 or n1==2: offset = 1
            words.append(self.get_word_with_offset(self.lr.ONES, n1, offset, n1_case))
        if i > 0:
            offset = 0
            if (i==1) and (n1==1): offset = 10 # to use the feminine form of one thousand
            suffix = ''
            if i > 1 and n1 > 1:
                suffix = 'а' # милион - милиона
            form = self.lr.THOUSANDS[i + offset][0] + suffix
            # if case == 1 and last_chunk:
            #    form = self.detnom_form(form)
            words.append(form)
        return words

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
        last_non_empty = 0
        while i > 0:
            if chunks[i-1] != 0:
                last_non_empty = i-1
                break
            i -= 1
        # print("DEBUG: chunks: ", chunks, last_non_empty)
        i = len(chunks)
        insert_and = False
        for k, chunk in enumerate(chunks):
            i -= 1
            if chunk == 0:
                continue
            real_offsets = offsets
            if i > 0 or not len(offsets): real_offsets = [0, 0, 0]
            words += self.get_words_with_offsets(chunk, case, real_offsets, i, insert_and, last_chunk=(k==last_non_empty))
            if i == 1 or (k < len(chunks) - 1 and chunks[k+1] == 0):  # specific for SK
                insert_and = True
            else:
                insert_and = False

        return ' '.join(words)

if __name__ == '__main__':
    yo = Num2Word_SK()
    import sys
    for line in sys.stdin: # ['0 1 22 23 100 1000 2000']: #  ['1/4 14.22 10 150 2го 22-го 56/171 34х 1991 14.2 1016.53 0']:
        nums = line.strip().split()
        for num in nums:
            for case_name, case_variants in yo.lr.NOUN_CASES.items():
                c = [case_variants]
                for case in c:
                    try:
                        print("CARDINAL:", case_name, num, yo.to_cardinal(num, case=case))
                        print("EXPERIMENTAL:", yo.my_int2word(int(num), feminine=False, case=case, offsets=[1,1,1]))
                    except ValueError:
                        pass
            for num_gender_name, num_gender in yo.lr.GENDERS.items():
                for case_name, case_variants in yo.lr.NOUN_CASES.items():
                    c = [case_variants]
                    for case in c:
                        try:
                            print(num_gender_name, case_name, num, yo.to_ordinal(num, num_gender=num_gender, case=case))
                        except ValueError:
                            pass


