# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def partition(self, head: 'ListNode', x: 'int') -> 'ListNode':
        small = ListNode(None)
        small_head = small
        large = ListNode(None)
        large_head = large

        while head:
            if head.val < x:
                small.next = head
                small = small.next
            else:
                large.next = head
                large = large.next
            head = head.next

        large.next = None
        small.next = large_head.next

        return small_head.next


def traverse(n):
    l = []
    while n:
        l.append(n.val)
        n = n.next
    return l


if __name__ == '__main__':
    n1 = ListNode(1)
    n1.next = ListNode(4)
    n1.next.next = ListNode(3)
    n1.next.next.next = ListNode(2)
    n1.next.next.next.next = ListNode(5)
    n1.next.next.next.next.next = ListNode(2)

    sol = Solution()
    assert traverse(sol.partition(n1, 3)) == [1, 2, 2, 4, 3, 5], 'Fail'

    n2 = ListNode(1)
    assert traverse(sol.partition(n2, 0)) == [1], 'Fail'

    n3 = ListNode(1)
    assert traverse(sol.partition(n3, 3)) == [1], 'Fail'
