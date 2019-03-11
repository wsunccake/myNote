class Solution:
    def reverse(self, x: 'int') -> 'int':
        # int32_max = 2 ** 31 - 1
        # int32_min = - 2 ** 31
        int32_max = 2147483647
        int32_min = -2147483648

        c = 1
        if x < 0:
            c = -1
        x = c * x

        y = 0
        i, j = divmod(x, 10)
        y = j
        while i != 0:
            x = i
            i, j = divmod(x, 10)
            y = y * 10 + j

        if int32_min > y or y > int32_max:
            return 0
        return y * c

# class Solution:
#     def reverse(self, x: 'int') -> 'int':
#         int32_max = 2147483647
#         int32_min = -2147483648
# 
#         c = 1
#         if x < 0:
#             c = -1
#         x = c * x
# 
#         y = int(str(x)[::-1])
#         if int32_min > y or y > int32_max:
#             return 0
#         return y * c

if __name__ == '__main__':
    sol = Solution()
    assert sol.reverse(123) == 321, 'Fail'
    assert sol.reverse(-123) == -321, 'Fail'
    assert sol.reverse(120) == 21, 'Fail'
    assert sol.reverse(1534236469) == 0, 'Fail'
