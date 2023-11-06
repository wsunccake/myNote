# docstring & doctest

```python
# ex.py
def recurrent_sum(l):
    """recurrence / recurrent
    Args:
        l(list[int]): int list

    Returns:
        int: sum of list

    Examples:
        >>> recurrent_sum([1, 2, 3, 4, 5])
        15
    """
    sum = 0
    for i in l:
        sum += i
    return sum


def recursive_sum(l):
    """recursion / recursive
    >>> recursive_sum([1, 2, 3, 4, 5])
    15
    """
    if len(l) == 0:
        return 0
    d = l.pop()
    return recursive_sum(l) + d


if __name__ == "__main__":
    # docstring
    help(recurrent_sum)
    print(recursive_sum.__doc__)

    # doctest
    import doctest
    doctest.testmod()
```

```bash
linux:~ $ python -v ex.py
```
