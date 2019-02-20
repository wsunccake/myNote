"""
Given two strings s and t , write a function to determine if t is an anagram of s.

Example 1:
Input: s = "anagram", t = "nagaram"
Output: true

Example 2:
Input: s = "rat", t = "car"
Output: false
"""


def valid1(s, t):
    word1 = {}
    for c in s:
        if word1.get(c):
            word1[c] += 1
        else:
            word1[c] = 1

    word2 = {}
    for c in t:
        word2[c] = word2.get(c, 0) + 1

    return word1 == word2


def valid2(s, t):
    word1 = {}
    def char_count(c):
        word1[c] = word1.get(c, 0) + 1
    [char_count(c) for c in s]

    word2 = {}
    [word2.update({c: word2.get(c, 0) + 1}) for c in t]

    return word1 == word2


class Solution:
    def isAnagram(self, s: 'str', t: 'str') -> 'bool':
        word1 = {}
        [word1.update({c: word1.get(c, 0) + 1}) for c in s]
        word2 = {}
        [word2.update({c: word2.get(c, 0) + 1}) for c in t]
        return word1 == word2


# class Solution:
#     def isAnagram(self, s: 'str', t: 'str') -> 'bool':
#         return sorted(s) == sorted(t)

if __name__ == '__main__':
    sol = Solution()
    assert sol.isAnagram('anagram', 'nagaram') is True, 'Fail'
    assert sol.isAnagram('rat', 'cat') is False, 'Fail'
    assert sol.isAnagram('obby', 'boy') is False, 'Fail'
