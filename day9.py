import itertools

def get_lines():
    input = """Tristram to AlphaCentauri = 34
Tristram to Snowdin = 100
Tristram to Tambi = 63
Tristram to Faerun = 108
Tristram to Norrath = 111
Tristram to Straylight = 89
Tristram to Arbre = 132
AlphaCentauri to Snowdin = 4
AlphaCentauri to Tambi = 79
AlphaCentauri to Faerun = 44
AlphaCentauri to Norrath = 147
AlphaCentauri to Straylight = 133
AlphaCentauri to Arbre = 74
Snowdin to Tambi = 105
Snowdin to Faerun = 95
Snowdin to Norrath = 48
Snowdin to Straylight = 88
Snowdin to Arbre = 7
Tambi to Faerun = 68
Tambi to Norrath = 134
Tambi to Straylight = 107
Tambi to Arbre = 40
Faerun to Norrath = 11
Faerun to Straylight = 66
Faerun to Arbre = 144
Norrath to Straylight = 115
Norrath to Arbre = 135
Straylight to Arbre = 127"""
    return input.splitlines()

names = {}
distances = {}

def set_locations_from_lines(lines):
    for line in lines:
        sides = line.split(" = ")
        distance = int(sides[1])
        locations = sides[0].split(" to ")
        names[locations[0]] = True
        names[locations[1]] = True
        #our key can just be composite of the two names. we'll make the map run both directions, will be easier later.
        distances[locations[0] + "." + locations[1]] = distance
        distances[locations[1] + "." + locations[0]] = distance

#9 hops, longest distance is 147, so 20K is definitely longer
shortest = 20000
longest = 0
lines = get_lines()
set_locations_from_lines(lines)
names_list = names.keys()
#it is because of itertools.permutations() that this is not written in Go.
permuted = itertools.permutations(names_list)
for route in permuted:
    total = 0
    for i in xrange(len(route) - 1):
        total = total + distances[route[i] + "." + route[i+1]]
    if total > longest:
        longest = total
    if total < shortest:
        shortest = total

print "shortest:", shortest
print "longest:", longest
        

