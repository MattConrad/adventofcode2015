import operator
import collections

ingredient_list = [ "Frosting", "Candy", "Butterscotch", "Sugar" ]
# omitting calories here is deliberate, calories are special
properties_list = [ "capacity", "durability", "flavor", "texture" ]

#"flavor": flav!
def getIngredientProps(cap, dur, flav, txt, cal):
    return { "capacity": cap, "durability": dur, "flavor": flav, "texture": txt, "calories": cal }

# this is the beating heart of this solver. got it from internet, didn't write. understand output, but not process, not really.
# for future ref: http://stackoverflow.com/questions/2128784/python-to-c-sharp-code-explanation
def multichoose(n,k):
    if k < 0 or n < 0: return "Error"
    if not k: return [[0]*n]
    if not n: return []
    if n == 1: return [[k]]
    return [[0]+val for val in multichoose(n-1,k)] + \
        [[val[0]+1]+val[1:] for val in multichoose(n,k-1)]

def calories(ingredient_count_row):
    # ingredient_count_row is a len 4 array, like the ingredient list. 
    # we are matching each index in the row to the corresponding ingredient in the ingredient list.
    return sum([ingredients[name]["calories"] * ingredient_count_row[i] for i, name in enumerate(ingredient_list)])

def to_zero(val):
    if val < 0:
        return 0
    else:
        return val

def score_cookie(ingredient_count_row):
    # no not going to try to make this a one liner. 
    total = collections.defaultdict(int) 
    for i, name in enumerate(ingredient_list):
        for prop in properties_list:
            total[prop] += (ingredients[name][prop] * ingredient_count_row[i])
    
    return reduce(operator.mul, [to_zero(total[prop]) for prop in total.keys()], 1)

# didn't write the parser here either.
ingredients = {}
ingredients["Frosting"] = getIngredientProps(4, -2, 0, 0, 5)
ingredients["Candy"] = getIngredientProps(0, 5, -1, 0, 8)
ingredients["Butterscotch"] = getIngredientProps(-1, 0, 5, 0, 6)
ingredients["Sugar"] = getIngredientProps(0, 0, -2, 2, 1)

best_score = 0
best_cookie = []
for row in multichoose(4, 100):
    #to do part one, don't check cals first.
    cals = calories(row)
    if cals == 500:
        score = score_cookie(row)
        if score > best_score:
            best_score = score
            best_cookie = row

print best_score
print best_cookie

