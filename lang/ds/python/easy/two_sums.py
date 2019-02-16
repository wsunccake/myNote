"""
Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:
Given nums = [2, 7, 11, 15], target = 9,
Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
"""


elements = [2, 7, 11, 15]
target = 9


for i in range(len(elements)-1):
    for j in range(i+1, len(elements)):
        if elements[i] + elements[j] == target:
            print('{}: {}, {}: {}'.format(i, elements[i], j, elements[j]))


for i in range(len(elements)-1):
    goal = target - elements[i]
    if goal in elements:
        for j in range(i+1, len(elements)):
            if goal == elements[j]:
                print('{}: {}, {}: {}'.format(i, elements[i], j, elements[j]))


for i in range(len(elements)-1):
    goal = target - elements[i]
    if goal in elements:
        j = elements.index(goal)
        print('{}: {}, {}: {}'.format(i, elements[i], j, elements[j]))
        break


for e in elements:
    goal = target - e
    if goal in elements:
        print('{}: {}, {}: {}'.format(elements.index(e), e, elements.index(goal), goal))
        break
