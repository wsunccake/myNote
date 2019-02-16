from ch4_linked_list.single_linked.linked_list import LinkedList, LinkedNode


class Student2:
    def __init__(self, name):
        self.name = name


class SingleLinked2(LinkedList):
    def __init__(self):
        self.head = None

    def insert(self, data, position=0):
        node = LinkedNode(data, None)
        if self.head is None:
            self.head = node
            return

        current_node = self.head

        if position == 0:
            node.next = current_node
            self.head = node
            return

        for i in range(position):
            previous_node = current_node
            current_node = current_node.next
        node.next = current_node
        previous_node.next = node

    def delete(self, position=0):
        current_node = self.head

        if position == 0:
            self.head = current_node.next
            return

        for i in range(position):
            previous_node = current_node
            current_node = current_node.next

        previous_node.next = current_node.next

    def traverse(self):
        if self.head is None:
            return

        current = self.head
        result = []
        while(True):
            result.append(current.data.name)
            if current.next is None:
                break
            current = current.next
        print(' -> '.join(result))


if __name__ == '__main__':
    single_linked2 = SingleLinked2()
    s21 = Student2('s21')
    s22 = Student2('s22')
    s23 = Student2('s23')
    s24 = Student2('s24')

    single_linked2.insert(s21)
    single_linked2.insert(s22)
    single_linked2.insert(s23)
    single_linked2.insert(s24, 1)
    single_linked2.traverse()

    single_linked2.delete(1)
    single_linked2.traverse()

    single_linked2.delete()
    single_linked2.traverse()
