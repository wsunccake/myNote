# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def addTwoNumbers(self, l1: 'ListNode', l2: 'ListNode') -> 'ListNode':
        r1 = ListNode(None)
        while l1:
            r1_next = r1.next
            l1_next = l1.next

            r1.next = l1
            l1.next = r1_next
            l1 = l1_next

        r1 = r1.next
        v1 = 0
        while r1:
            v1 = v1 * 10 + r1.val
            r1 = r1.next

        r2 = ListNode(None)
        while l2:
            r2_next = r2.next
            l2_next = l2.next

            r2.next = l2
            l2.next = r2_next
            l2 = l2_next

        r2 = r2.next
        v2 = 0
        while r2:
            v2 = v2 * 10 + r2.val
            r2 = r2.next

        t = v1 + v2
        r0 = ListNode(0)
        dummy = r0

        if t == 0:
            return dummy

        while t != 0:
            t, r = divmod(t, 10)
            r0.next = ListNode(r)
            r0 = r0.next

        return dummy.next


# class Solution:
#     def addTwoNumbers(self, l1: 'ListNode', l2: 'ListNode') -> 'ListNode':
#         r0 = ListNode(None)
#         dummy = r0
#         q = 0
#         while True:
#             # quotient
#             # remainder
#             q, r = divmod(l1.val + l2.val + q, 10)
#             r0.next = ListNode(r)
#
#             l1 = l1.next
#             l2 = l2.next
#             r0 = r0.next
#
#             if not l1 or not l2:
#                 break
#
#         while l1:
#             q, r = divmod(l1.val + q, 10)
#             r0.next = ListNode(r)
#
#             l1 = l1.next
#             r0 = r0.next
#
#         while l2:
#             q, r = divmod(l2.val + q, 10)
#             r0.next = ListNode(r)
#
#             l2 = l2.next
#             r0 = r0.next
#
#         if q != 0:
#             r0.next = ListNode(q)
#
#         return dummy.next

# class Solution:
#     def addTwoNumbers(self, l1: 'ListNode', l2: 'ListNode') -> 'ListNode':
#         h = l1
#         c = None
#         q = 0
#         while True:
#             l1.val = l1.val + l2.val + q
#             q, r = divmod(l1.val, 10)
#             l1.val = r
#
#             c = l1
#             l1 = l1.next
#             l2 = l2.next
#
#             if not l1 or not l2:
#                 break
#
#         while l1:
#             l1.val += q
#             q, r = divmod(l1.val, 10)
#             l1.val = r
#
#             c = l1
#             l1 = l1.next
#
#         while l2:
#             c.next = l2
#             l2.val += q
#             q, r = divmod(l2.val, 10)
#             l2.val = r
#
#             c = c.next
#             l2 = l2.next
#
#         if q != 0:
#             c.next = ListNode(q)
#
#         return h


if __name__ == '__main__':
    sol = Solution()
    l1 = ListNode(2)
    l1.next = ListNode(4)
    l1.next.next = ListNode(3)
    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)
    l3 = ListNode(8)
    l3.next = ListNode(0)
    l3.next.next = ListNode(7)
    l3 = sol.addTwoNumbers(l1, l2)
    assert l3.val == 7, 'Fail'
    assert l3.next.val == 0, 'Fail'
    assert l3.next.next.val == 8, 'Fail'

    l1 = ListNode(0)
    l2 = ListNode(0)
    l3 = sol.addTwoNumbers(l1, l2)
    assert l3.val == 0, 'Fail'

    l1 = ListNode(5)
    l2 = ListNode(5)
    l3 = sol.addTwoNumbers(l1, l2)
    assert l3.val == 0, 'Fail'
    assert l3.next.val == 1, 'Fail'

    l1 = ListNode(3)
    l2 = ListNode(9)
    l2.next = ListNode(8)
    l3 = sol.addTwoNumbers(l1, l2)
    assert l3.val == 2, 'Fail'
    assert l3.next.val == 9, 'Fail'

    l1 = ListNode(9)
    l1.next = ListNode(8)
    l2 = ListNode(9)
    l3 = sol.addTwoNumbers(l1, l2)
    assert l3.val == 8, 'Fail'
    assert l3.next.val == 9, 'Fail'

    l1 = ListNode(1)
    l2 = ListNode(9)
    l2.next = ListNode(9)
    l3 = sol.addTwoNumbers(l1, l2)
    assert l3.val == 0, 'Fail'
    assert l3.next.val == 0, 'Fail'
    assert l3.next.next.val == 1, 'Fail'

    l1 = ListNode(9)
    l1.next = ListNode(9)
    l2 = ListNode(1)
    l3 = sol.addTwoNumbers(l1, l2)
    assert l3.val == 0, 'Fail'
    assert l3.next.val == 0, 'Fail'
    assert l3.next.next.val == 1, 'Fail'
