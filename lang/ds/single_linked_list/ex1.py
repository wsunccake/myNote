from ch4_linked_list.single_linked.linked_list import LinkedList


class Student1:
    def __init__(self, name):
        self.name = name
        self.next = None


class SingleLinked1(LinkedList):
    def __init__(self):
        self.head = None

    def insert(self, data, position=0):
        if self.head is None:
            self.head = data
            return

        current = self.head

        if position == 0:
            data.next = current
            self.head = data
            return

        for i in range(position):
            previous = current
            current = current.next
        data.next = current
        previous.next = data

    def delete(self, position=0):
        current = self.head

        if position == 0:
            self.head = current.next
            return

        for i in range(position):
            previous = current
            current = current.next

        previous.next = current.next

    def traverse(self):
        if self.head is None:
            return

        current = self.head
        result = []
        while(True):
            result.append(current.name)
            if current.next is None:
                break
            current = current.next
        print(' -> '.join(result))


if __name__ == '__main__':
    single_linked1 = SingleLinked1()
    s11 = Student1('s11')
    s12 = Student1('s12')
    s13 = Student1('s13')
    s14 = Student1('s14')

    single_linked1.insert(s11)
    single_linked1.insert(s12)
    single_linked1.insert(s13)
    single_linked1.insert(s14, 1)
    single_linked1.traverse()

    single_linked1.delete(1)
    single_linked1.traverse()

    single_linked1.delete()
    single_linked1.traverse()
