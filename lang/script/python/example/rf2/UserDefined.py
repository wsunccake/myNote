def intAdd(a1, a2):
    if type(a1) != type(a2):
        raise TypeError('type different')
    return a1 + a2