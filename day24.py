import itertools, operator

#for groups after the first (smallest) group, we only need to check if valid subgroups exist, we don't need to know what they actually are.
def has_valid_next_group(group, target_weight, group_count):
    #divide the group into subgroups and look for subgroups (and perhaps sub-subgroups) with valid weights
    max_count = len(group) / group_count 
    for i in range(1, max_count + 1):
        for subgroup in itertools.combinations(group, i):
            if sum(subgroup) == target_weight:
                #if we're down to two groups and one is valid, we don't need to check the final group, it has to be valid.
                if group_count <= 2: 
                    return True
                else:
                    remainder = set(group) - set(subgroup)
                    return has_valid_next_group(remainder, target_weight, group_count - 1)
    return False

def get_valid_first_groups(weights, group_count):
    target_weight = sum(weights) / group_count
    #at most, our smallest group will have 1/group_count elements
    max_count = len(weights) / 3
    for i in range(1, max_count + 1):
        valids = []
        for group in itertools.combinations(weights, i):
            if sum(group) == target_weight: 
                #see if the remaining presents can be divided into two^H^H^H further groups each with target weight.
                #spec doesn't say weights are unique, but ours are. we'll use it. 
                remainder = set(weights) - set(group)
                if has_valid_next_group(remainder, target_weight, group_count - 1):
                    valids.append(group)

        #if we found any valid groups in this size, we're done. no need to check larger group sizes.
        if len(valids) > 0:
            return valids

    raise ValueError('Found no valid groups!')

def find_best_qe(weights, group_count):
    target_group_weight = sum(weights) / group_count
    valids = get_valid_first_groups(weights, group_count)
    return min([reduce(operator.mul, g, 1) for g in valids])


weights = [1, 3, 5, 11, 13, 17, 19, 23, 29, 31, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

best_3_qe = find_best_qe(weights, 3)
print 'Smallest qe among valid groupings with 3 groups:', best_3_qe

best_4_qe = find_best_qe(weights, 4)
print 'Smallest qe among valid groupings with 4 groups:', best_4_qe


