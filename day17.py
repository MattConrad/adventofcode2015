import itertools

sizes_string = '33,14,18,20,45,35,16,35,1,13,18,13,50,44,48,6,24,41,30,42'

# i got this from nessalc. he got it from itertools-recipes. :)
def powerset(iterable):
    #from https://docs.python.org/3/library/itertools.html#itertools-recipes
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

sizes = [int(s) for s in sizes_string.split(',')]

fewest_150_containers = 10000
fits_150_count = 0
for t in powerset(sizes):
    if sum(t) == 150: 
        fits_150_count += 1
        if len(t) < fewest_150_containers:
            fewest_150_containers = len(t)

print 'combinations fitting 150 liters: ', fits_150_count
print 'fewest containers holding 150 liters: ', fewest_150_containers 

#this ran way faster than I expected, so we'll just loop it again and not hard code answer from part 1
fits_150_min_containers = 0
for t in powerset(sizes):
    if sum(t) == 150 and len(t) == fewest_150_containers: 
        fits_150_min_containers += 1

print 'combinations fitting 150 liters and ',  fewest_150_containers, ' containers: ', fits_150_min_containers
