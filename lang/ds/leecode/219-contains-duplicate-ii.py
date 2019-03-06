"""
Given an array of integers and an integer k, find out whether there are two distinct indices i and j in the array such that nums[i] = nums[j] and the absolute difference between i and j is at most k.

Example 1:
Input: nums = [1,2,3,1], k = 3
Output: true

Example 2:
Input: nums = [1,0,1,1], k = 1
Output: true

Example 3:
Input: nums = [1,2,3,1,2,3], k = 2
Output: false
"""


# class Solution:
#     def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
#         is_duplicate = False
#
#         for i, v in enumerate(nums):
#             for n in nums[i+1:i+1+k]:
#                 if v == n:
#                     is_duplicate = True
#                     break
#
#             if is_duplicate:
#                 break
#
#         return is_duplicate


# class Solution:
#     def containsNearbyDuplicate(self, nums: list, k: int) -> bool:
#         is_duplicate = False
#
#         for i, v in enumerate(nums):
#             if v in nums[i+1:i+1+k]:
#                 is_duplicate = True
#                 break
#
#         return is_duplicate


# class Solution:
#     def containsNearbyDuplicate(self, nums: list, k: int) -> bool:
#         is_duplicate = False
#         tmp = {}
#
#         for i, v in enumerate(nums):
#             if v in tmp:
#                 if i - tmp[v] <= k:
#                     is_duplicate = True
#                     break
#             tmp[v] = i
#
#         return is_duplicate


class Solution:
    def containsNearbyDuplicate(self, nums: list, k: int) -> bool:
        is_duplicate = False
        tmp = {}
        for i, v in enumerate(nums):
            if v in tmp and i - tmp[v] <= k:
                is_duplicate = True
                break
            tmp[v] = i

        return is_duplicate


if __name__ == '__main__':
    sol = Solution()
    assert sol.containsNearbyDuplicate([1, 2, 3, 1], 3) is True, 'Fail'
    assert sol.containsNearbyDuplicate([99, 99], 2) is True, 'Fail'
    assert sol.containsNearbyDuplicate([1, 2, 1], 0) is False, 'Fail'
    assert sol.containsNearbyDuplicate([98, 99], 2) is False, 'Fail'
    assert sol.containsNearbyDuplicate([1, 0, 1, 1], 1) is True, 'Fail'
    assert sol.containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2) is False, 'Fail'
