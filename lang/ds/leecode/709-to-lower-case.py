"""
Implement function ToLowerCase() that has a string parameter str, and returns the same string in lowercase.

Example 1:

Input: "Hello"
Output: "hello"
Example 2:

Input: "here"
Output: "here"
Example 3:

Input: "LOVELY"
Output: "lovely"
"""

"""
ascii code
A - Z, 65 - 90
a - z, 97 - 122
"""


class Solution:
    def toLowerCase(self, str: 'str') -> 'str':
        result = ''
        for c in str:
            n = ord(c)
            if 65 <= n <= 90:
                n += 32
            result += chr(n)
        return result


if __name__ == '__main__':
    sol = Solution()
    assert sol.toLowerCase('Hello') == 'hello', 'Fail'
    assert sol.toLowerCase('here') == 'here', 'Fail'
    assert sol.toLowerCase('LOVELY') == 'lovely', 'Fail'
