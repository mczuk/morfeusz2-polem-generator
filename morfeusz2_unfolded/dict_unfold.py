#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import itertools

unique_out = None
unique_ctags = set()
init_str = ""
neutral_sgjp = set(['n1', 'n2', 'n3', 'p2', 'p3', 'p1'])
with codecs.open("%s.tab" % sys.argv[1], 'rb', 'utf-8') as f:    
    for line in f:
        if unique_out is None:
            init_str += line
            if line.strip() == "#</COPYRIGHT>":
                unique_out = set()
        else:
            (orth, base, ctag) = line.split(None, 3)[:3]
            sets = map(lambda c: 
                           set([elem if elem not in neutral_sgjp 
                            else 'm1' if elem == 'p1' 
                            else 'n' for elem in c.split(".")]), 
                           ctag.split(":"))
            for tag_parts in itertools.product(*sets):
                ctag = ":".join(tag_parts)
                unique_out.add((orth, base, ctag))
                unique_ctags.add(ctag)
                    
with codecs.open("%s.new.tab" % sys.argv[1], 'wb', 'utf-8') as f:    
    f.write(init_str)
    for (orth, base, ctag) in sorted(unique_out):
        f.write("%s\t%s\t%s\n" % (orth, base, ctag))

with codecs.open("%s.new.tagset" % sys.argv[1], 'wb', 'utf-8') as f:
    i = 2
    f.write("#!TAGSET-ID pl.sgjp.morfeusz-0.5.1\n\n[TAGS]\n")
    for ctag in sorted(unique_ctags):        
        f.write("%s\t%s\n" % (i, ctag))
        i += 1
    f.write("%s\t%s\n" % (3000, 'ign'))
    f.write("%s\t%s\n" % (3001, 'sp'))
    f.write("%s\t%s\n" % (3002, 'interp'))
    f.write("%s\t%s\n" % (3003, 'dig'))
    f.write("%s\t%s\n" % (3004, 'emoticon'))
    f.write("%s\t%s\n" % (3005, 'prefa'))
    f.write("%s\t%s\n" % (3006, 'prefppas'))
    f.write("%s\t%s\n" % (3007, 'prefs'))
    f.write("%s\t%s\n" % (3008, 'prefv'))
    f.write("%s\t%s\n" % (3009, 'nie'))
    f.write("%s\t%s\n" % (3010, 'naj'))
    f.write("%s\t%s\n" % (3011, 'romandig'))
    f.write("%s\t%s\n" % (3012, 'substa'))       
 