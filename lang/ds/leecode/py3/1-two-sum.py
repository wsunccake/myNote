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
