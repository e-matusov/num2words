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
            w = pref + x
            print(w.replace('>', ''), file=out)

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
        print_forms(self.THOUSANDS, out)
        for v in self.ORD_STEMS.values():
            print_forms(self.ORD_SUFFIXES, out, v)
        for v in self.ORD_STEMS_EXCEPTION.values():
            print_forms(self.ORD_SUFFIXES_EXCEPTION, out, v)

    def get_schemes(self, mapping, strict=True):
        result = {}
        for key, val in mapping.items():
            if not isinstance(key, tuple):
                key = (key,) # make it a tuple
            result_list = []
            for entity in val.split('|'):
                word_suff = entity.split('[')
                stem = word_suff[0]
                if len(word_suff) > 1:
                    suffs = word_suff[1][:-1].split('/') # remove "]" in the end first
                    for suff in suffs:
                        real_stem = stem
                        real_suff = '' if suff == '_' else suff # underscore signals empty suffix
                        while real_suff.startswith("."): # period(s) signal that first the last char(s) from the stem has to be removed before attaching the suff
                            real_stem = real_stem[:-1]
                            real_suff = real_suff[1:]
                        result_list.append(real_stem + '>' + real_suff)
                else:
                    result_list.append(stem)
            if strict and len(result_list) < len(self.NOUN_CASES): # strict mode means that you have to have all noun forms filled
                last_elem = result_list[-1]
                while len(result_list) < len(self.NOUN_CASES):
                    result_list.append(last_elem)
            for k in key:
                result[k] = result_list
        return result


    def __init__(self):
        self.NOUN_CASES = {'nom': 0, # nominative
                           'gen': 1, # genetive
                           'dat': 2,
                           'acc': 3,
                           'loc': 4,
                           'inst': 5
                          }
        self.GENDERS = {'masc': 0,
                        'neut':  1,
                        'fem': 2,
                        'plur': 3} # technically not gender, but...

        self.ZERO_ORDINAL = self.get_schemes({0: 'nulov[ý/ého/ému/ý/ým/om]',
                                              1: 'nulov[é/ého/ému/é/ým/om]',
                                              2: 'nulov[á/ej/ej/ú/ou/ej]',
                                              3: 'nulov[é/ých/ým/í/ými/ých]'})
        self.ZERO = ['nula']

        self.number_offsets = [4, 1, 2, 3] # ones, tens, hundreds, thousands ... max offset (e.g. 3 offset levels of 11, 21, 31 in ONES)
        self.ONES = self.get_schemes({
                                     100: 'nul[a/y/e/u/e/ou]',
                                     110: 'nul[y/_/ám/y/ách/ami]',
                                      1: 'jedn[a/ej/ej/u/ej/ou]', # TODO: check millions, etc.
                                      11: 'jed[en/ného/nému/en/nom/ným]',
                                      21: 'jed[no/ného/nému/no/nom/ným]',
                                      31: 'jed[en/ného/nému/ného/nom/ným]', # acc case variant
                                      2: 'dv[e/och/om/e/och/oma]',
                                     12: 'dv[a/och/om/a/och/oma]',
                                     22: 'dvoje',
                                     32: 'dv[aja/och/om/oh/och/oma]',
                                      3: 'tr[i/och/om/i/och/oma]',
                                     13: 'tr[aja/och/om/och/och/oma]',
                                     23: 'troje',
                                     33: 'tr[i/och/om/i/och/omi]',
                                     43: 'tr[aja/och/om/och/och/omi]',
                                      4: 'štyr[i/och/om/i/och/mi]',
                                     14: 'štyr[ia/och/om/och/och/mi]',
                                     24: 'štvoro',
                                      5: 'piat[...ät’/ich/im/...ät’/ich/imi]',
                                     15: 'piat[i/ich/im/ich/ich/imi]',
                                     25: 'pätoro',
                                      6: 'šest[’/ich/im/’/ich/imi]',
                                     26: 'šestoro',
                                      7: 'sed[em/mich/mim/em/mich/mimi]',
                                     27: 'sedmoro',
                                      8: 'os[em/mich/mim/em/mich/mimi]',
                                     28: 'osmoro',
                                      9: 'deviat[...ät’/ich/im/i/ich/imi]',
                                     29: 'devätoro'})

        self.TENS = self.get_schemes({ 0: 'desiat[...at’/ich/im/i/ich/imi]',
                                       1: 'jedenást[’/ich/im/i/ich/imi]',
                                       2: 'dvanást[’/ich/im/i/ich/imi]',
                                      12: 'dvanástoro',
                                       3: 'trinást[’/ich/im/i/ich/imi]',
                                       4: 'štrnást[’/ich/im/i/ich/imi]',
                                       5: 'pätnást[’/ich/im/i/ich/imi]',
                                       6: 'šestnást[’/ich/im/i/ich/imi]',
                                       7: 'sedemnást[’/ich/im/i/ich/imi]',
                                       8: 'osemnást[’/ich/im/i/ich/imi]',
                                       9: 'devätnást[’/ich/im/i/ich/imi]'})

        self.TWENTIES = self.get_schemes({ 2: 'dvads[at’/iati/iatim/at’/iatich/iatimi]',
                                           3: 'trids[at’/iati/iatim/at’/iatich/iatimi]',
                                           4: 'štyrids[at’/iati/iatim/at’/iatich/iatimi]',
                                           5: 'päťdesiat[_/i/im/_/ich/imi]',
                                           6: 'šesťdesiat[_/i/im/_/ich/imi]',
                                           7: 'sedemdesiat[_/i/im/_/ich/imi]',
                                           8: 'osemdesiat[_/i/im/_/ich/imi]',
                                           9: 'deväťdesiat[_/i/im/_/ich/imi]'})

        self.HUNDREDS = self.get_schemes({ 1: 'st[o/á/ám/a/ách/ámi]',
                                          11: 'st[a/o/e/o/om]',
                                          21: 'storo',
                                           2: 'dvesto',
                                           3: 'tristo',
                                           4: 'štyristo',
                                           5: "päťsto",
                                           6: 'šesťsto',
                                           7: 'sedemsto',
                                           8: 'osemsto',
                                           9: "deväťsto"})

        self.THOUSANDS = self.get_schemes({ 1: 'tisíc[_/a/u/_/i/om]',  # 10^3
                                           11: 'tisíc[e/ov/om/e/och/mi]',  # 10^3
                                           21: 'tisíc[e/ov/om/e/och/imi]',  # 10^3
                                           31: 'tisícoro',
                                            2: 'milión[_/a/u/_/e/om]',  # 10^6
                                           12: 'milión[y/ov/om/y/och/mi]',  # 10^6
                                            3: 'miliard[a/y/e/u/e/ou]',  # 10^9
                                           13: 'miliard[y/_/ám/y/ách/ámi]',  # 10^9
                                            4: 'trilión[_/a/u/_/e/om]',  # 10^12
                                           14: 'trilión[y/ov/om/y/och/mi]',  # 10^12
                                            5: 'kvadrilión[_/a/u/_/e/om]',  # 10^15
                                           15: 'kvadrilión[y/ov/om/y/och/mi]',  # 10^15
                                            6: 'kvintilión[_/a/u/_/e/om]',  # 10^18
                                           16: 'kvintilión[y/ov/om/y/och/mi]',  # 10^18
                                            7: 'sekstilión[_/a/u/_/e/om]',  # 10^18
                                           17: 'sekstilión[y/ov/om/y/och/mi]',
                                            8: 'septilión[_/a/u/_/e/om]',  # 10^18
                                           18: 'septilión[y/ov/om/y/och/mi]',
                                            9: 'oktilión[_/a/u/_/e/om]',  # 10^18
                                           19: 'oktilión[y/ov/om/y/och/mi]',
                                            9: 'nonilión[_/a/u/_/e/om]',  # 10^18
                                           19: 'nonilión[y/ov/om/y/och/mi]'})

        self.CURRENCY_FORMS = {} # will be handled via newtn

        self.AND = 'a'
        self.NEGWORD = "mínus"
        self.POINTWORD = "čiarka"

        self.ORD_STEMS = self.get_ord_map()
        self.ORD_STEMS.update({"nula": "nulov", # keys should be in nominative case here
                               "jedn": "prv",
                               "dv": "druh",
                               "tr": "tret",
                               "štyr": "štvrt",
                               "pät": "piat",
                               'p': "piat",
                               "šest": "šiest",
                               "sed": "siedm",
                               "os": "ôsm",
                               "dev": "deviat",
                               "des": "desiat",
                               "dvads": "dvadsiat",
                               "trids": "tridsiat",
                               "štyrids": "štyridsiat",
                               "st": "st",
                               "dvesto": "dvojst",
                               "tristo": "trojst",
                               "štyristo": "štvorst",
                               "miliard": "miliardt"})
        # print(self.ORD_STEMS, file=sys.stderr)
        # for 3 genders + plural
        self.ORD_SUFFIXES = {0: 'ý/ého/ému/ý/ým/om'.split('/'),
                             1: 'é/ého/ému/é/ým/om'.split('/'),
                             2: 'á/ej/ej/ú/ou/ej'.split('/'),
                             3: 'é/ých/ým/í/ými/ých'.split('/'),
                             4: 'ina/iny/ine/inu/ine/inou'.split('/'), # special gender for fractions
                             5: 'iny/ín/inám/iny/inách/inami'.split('/')} # special gender for fractions
        self.ORD_STEMS_EXCEPTION = {
                                    "tri": "tret",
                                    "tisíc": "tisíc",
                                    "tisíce": "tisíc",
                                   }
        # for 3 and 1000
        self.ORD_SUFFIXES_EXCEPTION = {0: 'í/ieho/iemu/í/ím/om'.split('/'),
                                       1: 'ie/ieho/iemu/ie/ím/om'.split('/'),
                                       2: 'ia/ej/ej/iu/ou/ej'.split('/'),
                                       3: 'i/ich/im/i/imi/ich'.split('/'),
                                       4: 'ina/iny/ine/inu/ine/inou'.split('/'), # special gender for fractions
                                       5: 'iny/ín/inám/iny/inách/inami'.split('/')} # special gender for fractions

        self.ZERO_ORD_STEM = 'nulov'
        self.FLOAT_INTEGER_PART = 'cel'

        self.ORDS_SINGLE = self.ONES[1] + self.ONES[11] + self.ONES[21] + self.ONES[31] # a list

    def get_ord_map(self):
        result = {}
        for val in list(self.HUNDREDS.values()) + list(self.THOUSANDS.values()) + list(self.TWENTIES.values()) + list(self.TENS.values()):
            new_key = val[0].split('>')[0] # just the stem
            stripped = new_key
            if stripped.endswith('’') or stripped.endswith('o'):
                stripped = stripped[:-1]
            elif stripped.endswith('ón'): # million
                stripped += 't'
            result[new_key] = stripped
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
            d = int(denominator)
            denom_case = case
            if n % 10 == 1 and (n % 100 != 11):
                num_gender = 2
                shift = 2
            elif n % 10 in [2, 3, 4] and (n % 100 not in [12, 13, 14]):
                num_gender = 3
                shift = 2
            else:
                num_gender = 3
                shift = 2
                if denom_case in [0, 3]: denom_case = 1
            mapped_denom = self.to_ordinal_num(d, num_gender=num_gender, case=denom_case, shift=shift)
            if d == 2:
                mapped_denom = mapped_denom.replace('druh', 'polov').replace('in', 'ic').replace('ín', 'íc').replace('á', 'ia')
            return res + mapped_denom
        else:
            raise ValueError(number)

    def to_ordinal_num(self, number, offsets=[], num_gender=0, case=0, shift=0):
    # optional num_gender: 0 (male), 1 (neutral), 2 (female) , 3 (plural). Shift is for using different suffixes for fraction denominators
    # optional case
        self.verify_ordinal(number)
        if number == 0:
            return self.lr.ZERO_ORDINAL[num_gender][case].replace('>', '')

        outwords = self.my_int2word(number, offsets=offsets, case=0).split(' ') # use nominative case here!
        my_range = [-1] if shift > 0 else  [-3, -2, -1] # last 2 positions should get the ordinal form (not for fractions!)
                                                        # this is different from other langs where it is only the last word
        # print("DEBUG: ", outwords)
        if number > 1000 and len(outwords) >= 2: # remove "edin/edna" unless it is at the end
            if len(outwords) == 2:
                my_range = [-1]
            for n in range(len(outwords) - 1):
                if outwords[n].replace('>', '') in self.lr.ORDS_SINGLE: outwords[n] = ''

            if outwords[0].startswith('dv') and len(outwords) == 2: # two millionth, three billionth
                outwords[0] = 'dvoj'
            elif outwords[0].startswith('tr') and len(outwords) == 2: # two millionth, three billionth
                outwords[0] = 'troj'

        for m in my_range:
            if (len(outwords) + m) < 0:
                continue
            lastword = outwords[m].lower().split('>')[0]
            # if len(lastword) == 1: lastword = outwords[m].lower().replace('>', '') # e.g. pät'
            mod_word = lastword
            if lastword in self.lr.ORD_STEMS_EXCEPTION:
                mod_word = self.lr.ORD_STEMS_EXCEPTION[lastword] + self.lr.ORD_SUFFIXES_EXCEPTION[num_gender+ shift][case]
            elif lastword in self.lr.ORD_STEMS and (shift==0 or (number % 10 <= 4 and (number % 100 not in [11, 12, 13, 14]))):
                mod_word = self.lr.ORD_STEMS[lastword] + self.lr.ORD_SUFFIXES[num_gender + shift][case]
            else:
                mod_word = lastword + self.lr.ORD_SUFFIXES[num_gender + shift][case]
            outwords[m] = self.title(mod_word)
        return " ".join(outwords).strip().replace('>', '')

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
        res = self.my_int2word(m, feminine=feminine, case=case, offsets=offsets, float_word=float_word)
        res = res.replace('>', '')
        return res

    def get_word_with_offset(self, mapping, n, offset, case):
        real_offset = 10 * offset
        idx = n + real_offset
        if idx not in mapping: idx = n
        word = mapping[idx][case]
        return word

    def get_words_with_offsets(self, chunk, case, offsets, i, insert_and=False, last_chunk=False):
        words = []
        n1, n2, n3 = get_digits(chunk)
        # print("DEBUG: i, n1/n2/n3, case", i, n1, n2, n3, case)
        if n3 > 0:
            words.append(self.get_word_with_offset(self.lr.HUNDREDS, n3, offsets[2], case))
        if n2 > 1:
            words.append(self.get_word_with_offset(self.lr.TWENTIES, n2, offsets[1], case))
        if n2 == 1:
            words.append(self.get_word_with_offset(self.lr.TENS, n1, offsets[1], case))
        elif n1 > 0:
            offset = offsets[0]
            if i > 1 and n1 <= 2: offset = 1
            if i < 1 or n1 >= 2: # do not output "one thousand", just "thousand", same for million, etc.
                words.append(self.get_word_with_offset(self.lr.ONES, n1, offset, case))
        if i > 0:
            offset = offsets[3]
            suffix = ''
            mycase = case
            if i > 1 and n1 > 1:
                if case in [0, 3]: mycase = 1
                elif n1 >= 2:
                    offset = 1
            # print("DEBUG: i, n1/n2/n3, case", i, n1, n2, n3, mycase)
            words.append(self.get_word_with_offset(self.lr.THOUSANDS, i, offset, mycase))
        return words

    def my_int2word(self, n, feminine=False, case=0, offsets=[], adjust_accusative=True, float_word=None):
        if float_word != None: # e.g. 7 целых 5 десятых
            float_word_realization = self.to_fraction(str(n) + '/' + str(float_word), case=case)
            if float_word == 0:
                float_word_realization = float_word_realization.replace(self.lr.ZERO_ORD_STEM,
                                                                        self.lr.FLOAT_INTEGER_PART)
            return float_word_realization
        if n == 0:
            offset = offsets[0] if len(offsets) else 0
            return self.get_word_with_offset(self.lr.ONES, 100, offset, case)
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
            if not len(offsets): real_offsets = [0, 0, 0, 0]
            words += self.get_words_with_offsets(chunk, case, real_offsets, i, insert_and, last_chunk=(k==last_non_empty))
        return ' '.join(words)

if __name__ == '__main__':
    yo = Num2Word_SK()
    import sys
    for line in sys.stdin: # ['0 1 22 23 100 1000 2000']: #  ['1/4 14.22 10 150 2го 22-го 56/171 34х 1991 14.2 1016.53 0']:
        nums = line.strip().split()
        for num in nums:
            for case_name, case in yo.lr.NOUN_CASES.items():
                try:
                    print("CARDINAL:", case_name, num, yo.to_cardinal(num, case=case))
                    # print("EXPERIMENTAL:", yo.my_int2word(int(num), feminine=False, case=case, offsets=[1,1,1,1]))
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


