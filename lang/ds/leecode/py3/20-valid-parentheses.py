# class Solution:
#     def isValid(self, s: str) -> bool:
#         stack = []
#         for c in s:
#             if c == '(' or c == '{' or c == '[':
#                 stack.append(c)
#                 continue
#             if (c == ')' and len(stack) < 1) or (c == ')' and '(' != stack.pop()):
#                 return False
#             if (c == '}' and len(stack) < 1) or (c == '}' and '{' != stack.pop()):
#                 return False
#             if (c == ']' and len(stack) < 1) or (c == ']' and '[' != stack.pop()):
#                 return False
#         return len(stack) == 0


class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        for c in s:
            if c == '(' or c == '{' or c == '[':
                stack.append(c)
                continue
            if c == ')' and (len(stack) < 1 or '(' != stack.pop()):
                return False
            if c == '}' and (len(stack) < 1 or '{' != stack.pop()):
                return False
            if c == ']' and (len(stack) < 1 or '[' != stack.pop()):
                return False
        return len(stack) == 0


# class Solution:
#     def isValid(self, s: str) -> bool:
#         mapping = {'(': ')', '{': '}', '[': ']'}
#         stack = []
#         for c in s:
#             if mapping.get(c, False):
#                 stack.append(mapping[c])
#                 continue
#             if len(stack) < 1:
#                 return False
#             if c != stack.pop():
#                 return False
#         return len(stack) == 0


# class Solution:
#     def isValid(self, s: str) -> bool:
#         pairs = {'(': ')', '{': '}', '[': ']'}
#         match = []
#         for c in s:
#             if c in pairs.keys():
#                 match.append(pairs[c])
#             elif not match or c != match.pop():
#                 return False
#         return len(match) == 0


if __name__ == '__main__':
    sol = Solution()
    assert sol.isValid('[') is False, 'Fail'
    assert sol.isValid(')') is False, 'Fail'
    assert sol.isValid('()') is True, 'Fail'
    assert sol.isValid('()[]{}') is True, 'Fail'
    assert sol.isValid('())(') is False, 'Fail'
    assert sol.isValid('(]') is False, 'Fail'
    assert sol.isValid('([)]') is False, 'Fail'
    assert sol.isValid('{[]}') is True, 'Fail'
