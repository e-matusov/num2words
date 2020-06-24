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

class LanguageResources_SL:

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

        self.ZERO_ORDINAL = self.get_schemes({0: 'nič[ni/nega/nemu/en/nem/nim]',
                                              1: 'nič[no/nega/nému/no/nem/nim]',
                                              2: 'nič[ná/ne/ni/no/ni/no]',
                                              3: 'nič[ni/nih/nim/ne/nimi/nih]'})
        self.ZERO = ['nič']

        self.number_offsets = [2, 0, 0, 2] # ones, tens, hundreds, thousands ... max offset (e.g. 3 offset levels of 11, 21, 31 in ONES) #
        self.ONES = self.get_schemes({
                                     100: 'nič[_/le/li/la//lom/li]',
                                     110: 'nič[la/el/elam/la/lami/lah]', # TODO: check for declensions of null!
                                      1: 'en[a/e/i/o/i/o]',
                                      11: 'en[_/ega/emu/.den/em/im]',
                                      21: 'en[o/ega/emu/o/em/im]',
                                      2: 'dv[e/eh/ema/e/eh/ema]',
                                     12: 'dv[a/eh/ema/a/eh/ema]',
                                     22: 'dvoje',
                                      3: 'tr[i/eh/em/i/eh/emi]',
                                     13: 'tr[ije/eh/em/i/ej/emi]',
                                     23: 'troje',
                                      4: 'štir[i/ih/im/i/ih/imi]',
                                     14: 'štir[je/ih/im/i/ih/imi]',
                                     24: 'četvero',
                                      5: 'pet[_/ih/im/_/ih/imi]',
                                     15: 'petero',
                                      6: 'šest[_/ih/im/_/ih/imi]',
                                      7: 'sed[em/mih/mim/em/mih/mimi]',
                                     17: 'sed[em/mih/m/em/m/m]',
                                      8: 'os[em/mih/mim/em/mih/mimi]',
                                     28: 'os[em/mih/m/em/m/m]',
                                      9: 'devet[_/ih/im/_/ih/imi]',})

        self.TENS = self.get_schemes({ 0: 'deset[_/ih/im/_/ih/imi]',
                                       1: 'enajst[_/ih/im/_/ih/imi]',
                                       2: 'dvanajst[_/ih/im/_/ih/imi]',
                                       3: 'trinajst[_/ih/im/_/ih/imi]',
                                       4: 'štirinajst[_/ih/im/_/ih/imi]',
                                       5: 'petnajst[_/ih/im/_/ih/imi]',
                                       6: 'šestnajst[_/ih/im/_/ih/imi]',
                                       7: 'sedemnajst[_/ih/im/_/ih/imi]',
                                       8: 'osemnajst[_/ih/im/_/ih/imi]',
                                       9: 'devetnajst[_/ih/im/_/ih/imi]'})

        self.TWENTIES = self.get_schemes({ 2: 'dvajset[_/ih/im/_/ih/imi]',
                                           3: 'trideset[_/ih/im/_/ih/imi]',
                                           4: 'štirideset[_/ih/im/_/ih/imi]',
                                           5: 'petdeset[_/ih/im/_/ih/imi]',
                                           6: 'šestdeset[_/ih/im/_/ih/imi]',
                                           7: 'sedemdeset[_/ih/im/_/ih/imi]',
                                           8: 'osemdeset[_/ih/im/_/ih/imi]',
                                           9: 'devetdeset[_/ih/im/_/ih/imi]'})

        self.HUNDREDS = self.get_schemes({ 1: 'st[o/ih/im/o/ih/imi]',
                                           2: 'dvest[o/ih/im/o/ih/imi]',
                                           3: 'trist[o/ih/im/o/ih/imi]',
                                           4: 'štirist[o/ih/im/o/ih/imi]',
                                           5: "petst[o/ih/im/o/ih/imi]",
                                           6: 'šestst[o/ih/im/o/ih/imi]',
                                           7: 'sedemst[o/ih/im/o/ih/imi]',
                                           8: 'osemst[o/ih/im/o/ih/imi]',
                                           9: "devetst[o/ih/im/o/ih/imi]"})

        self.THOUSANDS = self.get_schemes({ 1: 'tisoč[_/ih/im/_/ih/imi]',  # 10^3
                                            2: 'milijon[_/a/u/_/u/om]',  # 10^6
                                           12: 'milijon[a/ov/oma/a/ih/oma]',  # 10^6
                                           22: 'milijon[i/ov/om/e/ih/i]',  # 10^6
                                            3: 'miliard[a/e/i/o/i/o]',  # 10^9
                                           13: 'miliard[i/_/ama/i/ah/ama]',  # 10^9
                                           23: 'miliard[e/_/am/e/ah/ami]',  # 10^9
                                            4: 'bilijon[_/a/u/_/u/om]',  # 10^12
                                           14: 'bilijon[a/ov/oma/a/ih/oma]',  # 10^12
                                           24: 'bilijon[i/ov/om/e/ih/i]',  # 10^12
                                            5: 'biliard[a/e/i/o/i/o]',  # 10^15
                                           15: 'biliard[i/_/ama/i/ah/ama]',  # 10^15
                                           25: 'biliard[e/_/am/e/ah/ami]',  # 10^15
                                            6: 'trilijon[_/a/u/_/u/om]',  # 10^12
                                           16: 'trilijon[a/ov/oma/a/ih/oma]',  # 10^12
                                           26: 'trilijon[i/ov/om/e/ih/i]',  # 10^12
                                            7: 'triliard[a/e/i/o/i/o]',  # 10^15
                                           17: 'triliard[i/_/ama/i/ah/ama]',  # 10^15
                                           27: 'triliard[e/_/am/e/ah/ami]',  # 10^15
                                           })

        self.CURRENCY_FORMS = {} # will be handled via newtn

        self.AND = 'in'
        self.NEGWORD = "minus"
        self.POINTWORD = "vejica"

        self.ORD_STEMS = self.get_ord_map()
        self.ORD_STEMS.update({"nič": "ničn", # keys should be in nominative case here
                               "en": "prv",
                               "dv": "drug",
                               "tr": "tret",
                               "štir": "četrt",
                               "pet": "pet",
                               'p': "pet",
                               "šest": "šest",
                               "sed": "sedm",
                               "os": "osm",
                               "dev": "devet",
                               "des": "deset",
                               "st": "st",
                               })
        # print(self.ORD_STEMS, file=sys.stderr)
        # for 3 genders + plural
        self.ORD_SUFFIXES = {0: 'i/ega/emu/ega/em/im'.split('/'),
                             1: 'o/ega/emu/o/em/im'.split('/'),
                             2: 'a/e/i/o/i/o'.split('/'),
                             3: 'i/ih/im/e/ih/imi'.split('/'),
                             4: 'ina/ini/ine/inu/ine/inu'.split('/'), # special gender for fractions # TODO: check forms in corpus
                             5: 'ini/in/inam/ini/inih/inami'.split('/')} # special gender for fractions
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

        self.ZERO_ORD_STEM = 'ničn>'
        self.FLOAT_INTEGER_PART = 'cel'

        self.ORDS_SINGLE = self.ONES[1] + self.ONES[11] + self.ONES[21] # a list

    def get_ord_map(self):
        result = {}
        for val in list(self.HUNDREDS.values()) + list(self.THOUSANDS.values()) + list(self.TWENTIES.values()) + list(self.TENS.values()):
            new_key = val[0].split('>')[0] # just the stem
            stripped = new_key
            if stripped.endswith('on')or  stripped.endswith('rd'):
                stripped = stripped + 't' # million
            result[new_key] = stripped
        return result

class Num2Word_SL(Num2Word_Base):

    def setup(self):
        self.lr = LanguageResources_SL()

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
            return self.lr.ZERO_ORDINAL[num_gender][case]

        outwords = self.my_int2word(number, offsets=offsets, case=0).split(' ') # use nominative case here!
        my_range = [-1] # only the last word is declined in Slovenian ordinal numbers
        # print("DEBUG: ", outwords)
        if number > 1000 and len(outwords) >= 2: # remove "edin/edna" unless it is at the end
            if len(outwords) == 2:
                my_range = [-1]
            for n in range(len(outwords) - 1):
                if outwords[n].replace('>', '') in self.lr.ORDS_SINGLE: outwords[n] = ''

#            if outwords[0].startswith('dv') and len(outwords) == 2: # two millionth, three billionth
#                outwords[0] = 'dvoj'
#            elif outwords[0].startswith('tr') and len(outwords) == 2: # two millionth, three billionth
#                outwords[0] = 'troj'

        for m in my_range:
            if (len(outwords) + m) < 0:
                continue
            lastword = outwords[m].lower()
            if lastword.endswith('>'):
                lastword = lastword.replace('>', '')
            else:
                lastword = lastword.split('>')[0]
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
            n2_word = ''
            if n1 > 0:
                n1_word = self.get_word_with_offset(self.lr.ONES, n1, 0, 0) # nominative, no offset == feminine
                n2_word += n1_word + self.lr.AND
            n2_word += self.get_word_with_offset(self.lr.TWENTIES, n2, offsets[1], case)
            words.append(n2_word)
        if n2 == 1:
            words.append(self.get_word_with_offset(self.lr.TENS, n1, offsets[1], case))
        elif n1 > 0 and n2 <= 1:
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
    yo = Num2Word_SL()
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


