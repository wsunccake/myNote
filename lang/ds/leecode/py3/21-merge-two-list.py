# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# class Solution:
#     def mergeTwoLists(self, l1: 'ListNode', l2: 'ListNode') -> 'ListNode':
#         node = ListNode(0)
#         dummy_node = node
#
#         while l1 and l2:
#             if l1.val <= l2.val:
#                 node.next = l1
#                 l1 = l1.next
#             else:
#                 node.next = l2
#                 l2 = l2.next
#             node = node.next
#
#         if l1 or l2:
#             node.next = l1 or l2
#         return dummy_node.next


class Solution:
    def mergeTwoLists(self, l1: 'ListNode', l2: 'ListNode') -> 'ListNode':
        l3 = ListNode(None)
        dummy_node = l3

        while True:
            if l1 is None or l2 is None:
                break

            if l1.val < l2.val:
                l3.next = l1
                l3, l1 = l3.next, l1.next

            else:
                l3.next = l2
                l3, l2 = l3.next, l2.next

        while l1:
            l3.next = l1
            l3, l1 = l3.next, l1.next

        while l2:
            l3.next = l2
            l3, l2 = l3.next, l2.next

        return dummy_node.next


def traverse(l):
    result = []
    while l:
        result.append(l.val)
        if l.next:
            l = l.next
        else:
            break
    return result


if __name__ == '__main__':
    l1 = ListNode(1)
    l1.next = ListNode(2)
    l1.next.next = ListNode(4)

    l2 = ListNode(1)
    l2.next = ListNode(3)
    l2.next.next = ListNode(4)

    sol = Solution()
    l3 = sol.mergeTwoLists(l1, l2)

    assert l3.val == 1, 'Fail'
    assert l3.next.val == 1, 'Fail'
    assert l3.next.next.val == 2, 'Fail'
    assert l3.next.next.next.val == 3, 'Fail'
    assert l3.next.next.next.next.val == 4, 'Fail'
    assert l3.next.next.next.next.next.val == 4, 'Fail'
