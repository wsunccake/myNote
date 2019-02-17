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


class Solution:
    def twoSum(self, nums: 'List[int]', target: 'int') -> 'List[int]':
        result = [0, 0]
        for num in nums:
            goal = target - num
            num_index = nums.index(num)
            nums[num_index] = None
            if goal in nums:
                result = [num_index, nums.index(goal)]
                break
            nums[num_index] = num
        return result


# class Solution:
#     def twoSum(self, nums: 'List[int]', target: 'int') -> 'List[int]':
#         result = [0, 0]
#         for num_index, num in enumerate(nums[:-1]):
#             goal = target - num
#             shift_index = num_index + 1
#             if goal in nums[shift_index:]:
#                 result = [num_index, nums[shift_index:].index(goal) + shift_index]
#                 break
#         return result


# class Solution:
#     def twoSum(self, nums: 'List[int]', target: 'int') -> 'List[int]':
#         tmp_dict = {}
#         for index, num in enumerate(nums):
#             goal = target - num
#             if goal in tmp_dict:
#                 return [tmp_dict[goal], index]
#             tmp_dict[num] = index
#         return [0, 0]


if __name__ == '__main__':
    sol = Solution()
    assert sol.twoSum([1, 2, 3], 6) == [0, 0], 'Fail'
    assert sol.twoSum([3, 2, 4], 6) == [1, 2], 'Fail'
    assert sol.twoSum([3, 3], 6) == [0, 1], 'Fail'