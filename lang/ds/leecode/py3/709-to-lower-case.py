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
