# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .lang_EU import Num2Word_EU


class Num2Word_HU(Num2Word_EU):
    def set_high_numwords(self, high):
        for n, word in self.high_numwords:
            self.cards[10**n] = word

    def setup(self):
        self.low_numwords = [
        
		"kilencvenkilenc",
		"kilencvennyolc",
		"kilencvenhét",
		"kilencvenhat",
		"kilencvenöt",
		"kilencvennégy",
		"kilencvenhárom",
		"kilencvenkettő",
		"kilencvenegy",
		"kilencven",
		"nyolcvankilenc",
		"nyolcvannyolc",
		"nyolcvanhét",
		"nyolcvanhat",
		"nyolcvanöt",
		"nyolcvannégy",
		"nyolcvanhárom",
		"nyolcvankettő",
		"nyolcvanegy",
		"nyolcvan",
		"hetvenkilenc",
		"hetvennyolc",
		"hetvenhét",
		"hetvenhat",
		"hetvenöt",
		"hetvennégy",
		"hetvenhárom",
		"hetvenkettő",
		"hetvenegy",
		"hetven",
		"hatvankilenc",
		"hatvannyolc",
		"hatvanhét",
		"hatvanhat"
		"hatvanöt",
		"hatvannégy",
		"hatvanhárom",
		"hatvankettő",
		"hatvanegy",
		"hatvan",
		"ötvenkilenc",
		"ötvennyolc",
		"ötvenhét",
		"ötvenhat",
		"ötvenöt",
		"ötvennégy",
		"ötvenhárom",
		"ötvenkettő",
		"ötvenegy",
		"ötven",
		"negyvenkilenc",
		"negyvennyolc",
		"negyvenhét",
		"negyvenhat",
		"negyvenöt",
		"negyvennégy",
		"negyvenhárom",
		"negyvenkettő",
		"negyvenegy",
		"negyven",
		"harminckilenc",	
		"harmincnyolc",
		"harminchét",
		"harminchat",
		"harmincöt",
		"harmincnégy",
		"harminchárom",
		"harminckettő",
		"harmincegy",
		"harminc",
		"húszonkilenc",
		"húszonnyolc",
		"húszonhét",
		"húszonhat",
		"húszonöt",
		"húszonnégy",
		"húszonhárom",
		"húszonkettő",
		"húszonegy",
		"húsz",
		"tízenkilenc",
		"tízennyolc",
		"tízenhét",
		"tízenhat",
		"tízenöt",
		"tízennégy",
		"tízenhárom",
		"tízenkettő",
		"tízenegy",
		"tíz",
		"kilenc",
		"nyolc",
		"hét",
		"hat",
		"öt",
		"négy",
		"három",
		"kettő",
		"egy",
		"nulla"
	]

        self.mid_numwords = [(100, "száz")]

        self.high_numwords = [(12, "billió"), (9,"milliárd"), (6, "millió"), (3, "ezer")]

        self.pointword = "vessző"

        self.modifiers = [
        
        ]

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
        elif 100 > lnum > rnum:
            return ("%s-%s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 100 > rnum:
            return ("%s %s" % (ltext, rtext), lnum + rnum)
        elif rnum > lnum:
            return ("%s %s" % (ltext, rtext), lnum * rnum)
        return ("%s %s" % (ltext, rtext), lnum + rnum)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return "%s%s" % (value, self.to_ordinal(value))

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value)
        if outwords[-1] in self.modifiers:
            outwords = outwords
        ordinal_num = outwords + "dik"
        return ordinal_num
