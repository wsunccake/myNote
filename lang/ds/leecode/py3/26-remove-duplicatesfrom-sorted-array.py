# class Solution:
#     def removeDuplicates(self, nums: 'List[int]') -> 'int':
#         count = 0
#         current = None
#         for num in nums:
#             if current != num:
#                 nums[count] = num
#                 count += 1
#                 current = num
#
#         return count


class Solution:
    def removeDuplicates(self, nums: 'List[int]') -> 'int':
        count = 0
        current = None
        for ind, num in enumerate(nums):
            if current != num:
                nums[count] = num
                count += 1
                current = num

        return count


# class Solution:
#     def removeDuplicates(self, nums: 'List[int]') -> 'int':
#         count = 0
#         current = None
#         i = 0
#         while i < len(nums):
#             if current != nums[i]:
#                 nums[count] = nums[i]
#                 count += 1
#                 current = nums[i]
#             i += 1
#
#         return count


if __name__ == '__main__':
    sol = Solution()
    q1 = [1, 1, 2]
    assert sol.removeDuplicates(q1) == 2, 'Fail'
    assert q1[:2] == [1, 2], 'Fail'

    q2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    assert sol.removeDuplicates(q2) == 5, 'Fail'
    assert q2[:5] == [0, 1, 2, 3, 4], 'Fail'
