class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return '{}: {}'.format(self.name, self.score)


def better_score(s1, s2):
    if s1.score > s2.score:
        return True
    return False


def equal_score(s1, s2):
    if s1.score == s2.score:
        return True
    return False


class LinkedNode:
    def __init__(self, val):
        self.val = val
        self.next = None


def traverse(node):
    nodes = []
    while node:
        print(node.val, end=' -> ')
        nodes.append(node)
        node = node.next

    return nodes


class LinkedList:
    def __init__(self, node, comparison):
        self.head = node
        self.comparison = comparison
        self.equal = None

    def set_equal(self, equal):
        self.equal = equal

    def insert1(self, node):
        if self.head.next is None:
            if self.comparison(node.val, self.head.val):
                node.next = self.head
                self.head = node
            else:
                self.head.next = node
            return

        dummy = LinkedNode(None)
        prev = dummy
        current = self.head

        while True:
            if self.comparison(node.val, current.val):
                node.next = current
                prev.next = node
                break

            if current.next is None:
                if self.comparison(node.val, current.val):
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
            if self.comparison( node.val, self.head.val):
                node.next = self.head
                self.head = node
            else:
                self.head.next = node
            return

        dummy = LinkedNode(None)
        prev = dummy
        current = self.head

        while current:
            if self.comparison(node.val, current.val):
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
        if self.comparison(node.val, current.val):
            node.next = current
            self.head = node
            return

        prev = self.head
        current = self.head

        while current:
            if self.comparison(node.val, current.val):
                node.next = current
                prev.next = node
                break

            if not current.next:
                current.next = node
                break

            prev = current
            current = current.next

    def find(self, val):
        current = self.head

        while current:
            if self.equal(val, current.val):
                return current.val

            current = current.next

        return None


if __name__ == '__main__':
    # data
    s1 = Student('s1', 60)
    s2 = Student('s2', 90)
    s3 = Student('s3', 80)
    s4 = Student('s4', 40)
    s5 = Student('s5', 50)
    s6 = Student('s6', 100)

    # insert
    n1 = LinkedNode(s1)
    n1.next = LinkedNode(s2)
    n1.next.next = LinkedNode(s3)
    traverse(n1)
    print()

    # sort insert
    linked_list = LinkedList(LinkedNode(s1), better_score)
    linked_list.insert(LinkedNode(s2))
    linked_list.insert(LinkedNode(s3))
    linked_list.insert(LinkedNode(s4))
    linked_list.insert(LinkedNode(s5))
    linked_list.insert(LinkedNode(s6))
    traverse(linked_list.head)
    print()

    # find
    linked_list.set_equal(equal_score)
    s = linked_list.find(Student('', 40))
    print(s)
