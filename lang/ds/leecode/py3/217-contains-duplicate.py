class Solution:
    def containsDuplicate(self, nums: list) -> bool:
        l = []
        is_duplicate = False
        for n in nums:
            if n in l:
                is_duplicate = True
                break
            l.append(n)
        return is_duplicate


# class Solution:
#     def containsDuplicate(self, nums: List[int]) -> bool:
#         s = sorted(nums)
#         is_duplicate = False
#
#         if len(nums) is 1:
#             return is_duplicate
#
#         for i in range(len(s) - 1):
#             if s[i] == s[i+1]:
#                 is_duplicate = True
#                 break
#
#         return is_duplicate


# class Solution:
#     def containsDuplicate(self, nums: List[int]) -> bool:
#         if len(set(nums)) == len(nums):
#             return False
#         return True


if __name__ == '__main__':
    sol = Solution()
    assert sol.containsDuplicate([1, 2, 3, 1]) is True, 'Fail'
    assert sol.containsDuplicate([1, 2, 3, 4]) is False, 'Fail'
    assert sol.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True, 'Fail'
