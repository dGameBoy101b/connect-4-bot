import random

def possibleShuffle(constant:list,seq:list)->bool:
    '''test for possible shuffle result'''
    if not isinstance(constant,list):
        raise TypeError('possibleShuffle() constant argument must be a list, not a '+str(type(constant)))
    if not isinstance(seq,list):
        raise TypeError('possibleShuffle() seq argument must be a list, not a '+str(type(seq)))
    constant_set=set(constant)
    result=len(constant)==len(seq)
    for item in constant_set:
        result=result and constant.count(item)==seq.count(item)
    return result
assert possibleShuffle(['a','c','e','b','d'],['a','b','c','d','e'])
