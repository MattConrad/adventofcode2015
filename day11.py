import re

# lowercase ascii range is 97-122
def inc_pwd(pwd):
    chs = [ord(c) for c in pwd]
    pos = -1
    while True:
        ch = chs[pos]
        if ch < 122:
            chs[pos] = ch + 1
            return "".join([chr(i) for i in chs])
        else:
            chs[pos] = 97
            pos -= 1
    #can assume no IndexError in this game, I think

# something more elegant? maybe.
def has_straight(pwd):
    chs = [ord(c) for c in pwd]
    #check windows of three chars, one after another, but don't run the right edge of the window off the pwd. 
    # seems fairly clear that yza is NOT considered a straight, assuming this for now (whew!).
    for i in range(0, len(pwd) - 2, 1):
        if chs[i] + 2 == chs[i + 1] + 1 == chs[i + 2]:
            return True

    return False

def get_next_good_pwd(pwd):
    # i'll have to see how nessalc did this with back refs 
    re_double_letter = re.compile(r'(aa|bb|cc|dd|ee|ff|gg|hh|ii|jj|kk|ll|mm|nn|oo|pp|qq|rr|ss|tt|uu|vv|ww|xx|yy|zz)')
    re_iol = re.compile(r'i|o|l')

    while True:
        pwd = inc_pwd(pwd)
        dbls = re_double_letter.findall(pwd)
        if has_straight(pwd) and len(set(dbls)) > 1 and re_iol.match(pwd) == None:
            break

    return pwd

pwd = 'cqjxjnds'
pwd = get_next_good_pwd(pwd)
print 'first new password:', pwd
pwd = get_next_good_pwd(pwd)
print 'second new password:', pwd


    



