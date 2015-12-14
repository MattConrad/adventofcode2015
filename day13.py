import itertools

def get_lines():
    input = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 81 happiness units by sitting next to Carol.
Alice would lose 42 happiness units by sitting next to David.
Alice would gain 89 happiness units by sitting next to Eric.
Alice would lose 89 happiness units by sitting next to Frank.
Alice would gain 97 happiness units by sitting next to George.
Alice would lose 94 happiness units by sitting next to Mallory.
Bob would gain 3 happiness units by sitting next to Alice.
Bob would lose 70 happiness units by sitting next to Carol.
Bob would lose 31 happiness units by sitting next to David.
Bob would gain 72 happiness units by sitting next to Eric.
Bob would lose 25 happiness units by sitting next to Frank.
Bob would lose 95 happiness units by sitting next to George.
Bob would gain 11 happiness units by sitting next to Mallory.
Carol would lose 83 happiness units by sitting next to Alice.
Carol would gain 8 happiness units by sitting next to Bob.
Carol would gain 35 happiness units by sitting next to David.
Carol would gain 10 happiness units by sitting next to Eric.
Carol would gain 61 happiness units by sitting next to Frank.
Carol would gain 10 happiness units by sitting next to George.
Carol would gain 29 happiness units by sitting next to Mallory.
David would gain 67 happiness units by sitting next to Alice.
David would gain 25 happiness units by sitting next to Bob.
David would gain 48 happiness units by sitting next to Carol.
David would lose 65 happiness units by sitting next to Eric.
David would gain 8 happiness units by sitting next to Frank.
David would gain 84 happiness units by sitting next to George.
David would gain 9 happiness units by sitting next to Mallory.
Eric would lose 51 happiness units by sitting next to Alice.
Eric would lose 39 happiness units by sitting next to Bob.
Eric would gain 84 happiness units by sitting next to Carol.
Eric would lose 98 happiness units by sitting next to David.
Eric would lose 20 happiness units by sitting next to Frank.
Eric would lose 6 happiness units by sitting next to George.
Eric would gain 60 happiness units by sitting next to Mallory.
Frank would gain 51 happiness units by sitting next to Alice.
Frank would gain 79 happiness units by sitting next to Bob.
Frank would gain 88 happiness units by sitting next to Carol.
Frank would gain 33 happiness units by sitting next to David.
Frank would gain 43 happiness units by sitting next to Eric.
Frank would gain 77 happiness units by sitting next to George.
Frank would lose 3 happiness units by sitting next to Mallory.
George would lose 14 happiness units by sitting next to Alice.
George would lose 12 happiness units by sitting next to Bob.
George would lose 52 happiness units by sitting next to Carol.
George would gain 14 happiness units by sitting next to David.
George would lose 62 happiness units by sitting next to Eric.
George would lose 18 happiness units by sitting next to Frank.
George would lose 17 happiness units by sitting next to Mallory.
Mallory would lose 36 happiness units by sitting next to Alice.
Mallory would gain 76 happiness units by sitting next to Bob.
Mallory would lose 34 happiness units by sitting next to Carol.
Mallory would gain 37 happiness units by sitting next to David.
Mallory would gain 40 happiness units by sitting next to Eric.
Mallory would gain 18 happiness units by sitting next to Frank.
Mallory would gain 7 happiness units by sitting next to George."""
    return input.splitlines()

names = {}
prefs = {}
happiest = 0
best_seating = ""

def set_prefs_from_lines(lines):
    for line in lines:
        #trim off the period before splitting
        words = line[:-1].split()
        names[words[0]] = True
        names[words[-1]] = True
        delta = int(words[3])
        #these are not two way relationships
        key = words[0] + ">" + words[-1]
        #word[2] is gain or lose, delta is +/- accordingly
        prefs[key] = delta if words[2] == "gain" else delta * -1

def find_optimal(names_list):
    permuted = itertools.permutations(names_list)
    for seating in permuted:
        global happiest
        global best_seating
        total = 0
        for i in xrange(len(seating) - 1):
            keyclock = seating[i] + ">" + seating[i+1]
            keycounter = seating[i+1] + ">" + seating[i]
            total = total + prefs[keyclock]
            total = total + prefs[keycounter]

        loopclock = seating[-1] + ">" + seating[0]
        loopcounter = seating[0] + ">" + seating[-1]
        total = total + prefs[loopclock]
        total = total + prefs[loopcounter]

        if total > happiest:
            happiest = total
            best_seating = ", ".join(seating)

def add_me(my_name):
    for name in names_list:
        keyclock = my_name + ">" + name
        keycounter = name + ">" + my_name
        prefs[keyclock] = 0
        prefs[keycounter] = 0
    
    names_list.append(my_name)

lines = get_lines()
set_prefs_from_lines(lines)
names_list = names.keys()

find_optimal(names_list)

print "optimal seating happiness without me: ", happiest, " seating: ", best_seating 
        
add_me('Matt')
happiest = 0
best_seating = ""

find_optimal(names_list)

print "optimal seating happiness including me: ", happiest, " seating: ", best_seating 

