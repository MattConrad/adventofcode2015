from collections import defaultdict
import re

subsstr = """Al => ThF
Al => ThRnFAr
B => BCa
B => TiB
B => TiRnFAr
Ca => CaCa
Ca => PB
Ca => PRnFAr
Ca => SiRnFYFAr
Ca => SiRnMgAr
Ca => SiTh
F => CaF
F => PMg
F => SiAl
H => CRnAlAr
H => CRnFYFYFAr
H => CRnFYMgAr
H => CRnMgYFAr
H => HCa
H => NRnFYFAr
H => NRnMgAr
H => NTh
H => OB
H => ORnFAr
Mg => BF
Mg => TiMg
N => CRnFAr
N => HSi
O => CRnFYFAr
O => CRnMgAr
O => HP
O => NRnFAr
O => OTi
P => CaP
P => PTi
P => SiRnFAr
Si => CaSi
Th => ThCa
Ti => BP
Ti => TiTi
e => HF
e => NAl
e => OMg"""

medicine = "ORnPBPMgArCaCaCaSiThCaCaSiThCaCaPBSiRnFArRnFArCaCaSiThCaCaSiThCaCaCaCaCaCaSiRnFYFArSiRnMgArCaSiRnPTiTiBFYPBFArSiRnCaSiRnTiRnFArSiAlArPTiBPTiRnCaSiAlArCaPTiTiBPMgYFArPTiRnFArSiRnCaCaFArRnCaFArCaSiRnSiRnMgArFYCaSiRnMgArCaCaSiThPRnFArPBCaSiRnMgArCaCaSiThCaSiRnTiMgArFArSiThSiThCaCaSiRnMgArCaCaSiRnFArTiBPTiRnCaSiAlArCaPTiRnFArPBPBCaCaSiThCaPBSiThPRnFArSiThCaSiThCaSiThCaPTiBSiRnFYFArCaCaPRnFArPBCaCaPBSiRnTiRnFArCaPRnFArSiRnCaCaCaSiThCaRnCaFArYCaSiRnFArBCaCaCaSiThFArPBFArCaSiRnFArRnCaCaCaFArSiRnFArTiRnPMgArF"

def get_subs_dict(lines):
    subs = defaultdict(list)
    for line in lines:
        initial, replace = line.split(' => ')
        subs[initial].append(replace)

    return subs

def get_variants(subs, medicine):
    re_tc = re.compile('[A-z][a-z]$')
    variants = defaultdict(int)
    size = len(medicine)
    i = 0
    while i < size:
        #our atomic symbol might be one or two letters. we'll assemble both for later checking (don't do twoletter at the very end)
        # fortunately, there are no tricky cases like C and Ca or S and Si in the data.
        oneletter = medicine[i]
        twoletter = ''
        if i + 1 < size:
            twoletter = medicine[i:i+2]
        if oneletter in subs:
            fill_variants(variants, medicine[:i], medicine[i+1:], subs[oneletter])
            i = i + 1
        elif twoletter in subs:
            fill_variants(variants, medicine[:i], medicine[i+2:], subs[twoletter])
            i = i + 2
        # we didn't find a match, is our non-substitutable atom a single letter or two letter atom?
        elif re_tc.match(twoletter):
            i = i + 2
        else:
            i = i + 1
    
    return variants

def fill_variants(variants, left, right, replacements):
    for rep in replacements:
        key = left + rep + right
        variants[key] += 1

def get_unsubs(subs):
    unsubs = {}
    for k, v in subs.iteritems():
        for e in v:
            unsubs[e] = k

    return unsubs

def reduce_to_final(final, unsubs, medicine):
    i = 0
    reduced = set([medicine])
    found_final = False
    #later this becomes while True with a break
    while True:
        predecessors = []
        for molecule in reduced:
            for start, replace in unsubs.iteritems():
                #this is ALMOST what translate was made for, but I only want to replace a single instance...
                #http://stackoverflow.com/questions/3873361/finding-multiple-occurrences-of-a-string-within-a-string-in-python
                indices = [n for n in xrange(len(molecule)) if molecule.find(start, n) == n]
                for idx in indices:
                    pred = molecule[:idx] + molecule[idx:].replace(start, replace, 1)
                    # be sure to count the step we're on if this is the final match
                    if pred == final:
                        return i + 1
                    predecessors.append(pred)
        #this gets out of control quickly. we're going to trim to the n shortest predecessors, let's try 1000 first.
        # yes, chars aren't the actual unit, but they're ok as an approximation. 
        # we could miss the shortest path this way. i hope it works.
        predecessors.sort(key = lambda s: len(s))
        reduced = set(predecessors[:1000])
        if len(reduced) == 0:
            return - 1
        i += 1
        #"print i" is kinda handy as a timer to let you know how things are progressing. speeds up at the end!
        #print i

    return -1

lines = subsstr.splitlines()
subs = get_subs_dict(lines)

variants = get_variants(subs, medicine)
print 'Distinct variants for single substitution: ', len(variants.keys())

#oh, they got me. for part 2, I don't think I can run all the permutations forward from 'e' to 500 chars.
# let's try working backward from the starter molecule, making it smaller step by step. still a lot of permutes, but not as many. i think.
# this can only work because there aren't any dupe substitutions. could have been, certainly.
unsubs = get_unsubs(subs)

final = 'e'
steps_to_final = reduce_to_final(final, unsubs, medicine)
print 'Steps to reduce starting molecule down to "' + final + '": ', steps_to_final

