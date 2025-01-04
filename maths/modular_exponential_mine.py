def mod_exp(base, exp, mod):
    # TODO: refactor
    res = 1
    for _ in range(exp):
        # res*=base
        # res%=mod
        res = (res*base)%mod

    return res

def repeat(func, count, init=1):
    for _ in range(count):
        init=func(init)
    return init


def mod_exp11(base, exp, mod):
    def step(res):
        return (res*base)%mod
    return repeat(step, exp)

import functools
def mod_exp12(base, exp, mod):
    def step(res,_):
        return (res*base)%mod
    return functools.reduce(step, range(exp), 1)

def mod_exp2(base, exp, mod):
    # print(f'mod_exp({base=}, {exp=}, {mod=})')
    # breakpoint()

    # TODO: switch case?
    if exp == 0:
        assert base!=0, 'indetermination'
        return 1

    if exp%2 ==0:
        y = mod_exp2(base, exp/2, mod)
        return y**2 % mod
    else:
        y = mod_exp2(base, (exp-1)/2, mod)
        return ((y**2)*base) % mod

def mod_exp2(base, exp, mod):
    # print(f'mod_exp({base=}, {exp=}, {mod=})')

    if exp == 0:
        assert base!=0, 'indetermination'
        return 1

    if exp%2 ==0:
        y = mod_exp2(base, exp/2, mod)
        return y**2 % mod
    else:
        y = mod_exp2(base, (exp-1)/2, mod)
        return ((y**2)*base) % mod

def test():
    assert mod_exp12(3, 45, 7) == 6
    assert mod_exp12(3, 200, 13) == 9
    assert mod_exp12(1269380576, 374, 34)

if __name__ == '__main__':
    # mod_exp2(1269380576, 374, 34)
    import timeit
    repeat=timeit.repeat('mod_exp(1269380576, 374, 34)', setup='from __main__ import mod_exp2 as mod_exp ')
    # print(f'{t=}')
    print(f'{min(repeat)/1e6=}')
    
