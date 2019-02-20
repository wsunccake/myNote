class LinkedNode:
    def __init__(self, val):
        self.val = val
        self.next = None


def traverse(node):
    while node:
        print(node.val, end=' -> ')
        node = node.next


class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return '{}: {}'.format(self.name, self.score)


def compare_score(s1, s2):
    if s1.score > s2.score:
        return True
    return False


class LinkedList:
    def __init__(self, node, comparison):
        self.head = node
        self.comparison = comparison

    def insert1(self, node):
        if self.head.next is None:
            if self.comparison(self.head.val, node.val):
                node.next = self.head
                self.head = node
            else:
                self.head.next = node
            return

        dummy = LinkedNode(None)
        prev = dummy
        current = self.head

        while True:
            if self.comparison(current.val, node.val):
                node.next = current
                prev.next = node
                break

            if current.next is None:
                if self.comparison(current.val, node.val):
                    node.next = current
                    prev.next = node
                else:
                    current.next = node
                break

            prev = current
            current = current.next

        if prev is dummy:
            self.head = dummy.next

    def insert2(self, node):
        if self.head.next is None:
            if self.comparison(self.head.val, node.val):
                node.next = self.head
                self.head = node
            else:
                self.head.next = node
            return

        dummy = LinkedNode(None)
        prev = dummy
        current = self.head

        while current:
            if self.comparison(current.val, node.val):
                node.next = current
                prev.next = node
                break

            if not current.next:
                current.next = node
                break

            prev = current
            current = current.next

        if prev is dummy:
            self.head = dummy.next

    def insert(self, node):
        current = self.head
        if self.comparison(current.val, node.val):
            node.next = current
            self.head = node
            return

        prev = self.head
        current = self.head

        while current:
            if self.comparison(current.val, node.val):
                node.next = current
                prev.next = node
                break

            if not current.next:
                current.next = node
                break

            prev = current
            current = current.next


if __name__ == '__main__':
    # data
    s1 = Student('a', 60)
    s2 = Student('b', 90)

    # insert
    n1 = LinkedNode(s1)
    n1.next = LinkedNode(s2)
    n1.next.next = LinkedNode(Student('c', 80))
    traverse(n1)
    print()

    # sort insert
    linked_list = LinkedList(LinkedNode(s1), compare_score)
    linked_list.insert(LinkedNode(s2))
    linked_list.insert(LinkedNode(Student('c', 80)))
    linked_list.insert(LinkedNode(Student('d', 40)))
    linked_list.insert(LinkedNode(Student('e', 50)))
    linked_list.insert(LinkedNode(Student('f', 100)))
    traverse(linked_list.head)
