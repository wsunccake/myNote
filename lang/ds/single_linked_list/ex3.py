from ch4_linked_list.single_linked.linked_list import LinkedList, LinkedNode


class SingleLinked3(LinkedList):
    def __init__(self, comparison):
        self.head = None
        self.comparison = comparison

    def insert(self, data, position=None):
        node = LinkedNode(data, None)
        if self.head is None:
            self.head = node
            return

        current_node = self.head
        if current_node is self.head and self.comparison(node.data, current_node.data):
            node.next = current_node
            self.head = node
            return

        current_node = self.head.next
        previous_node = self.head
        while True:
            if self.comparison(node.data, current_node.data):
                node.next = current_node
                previous_node.next = node
                break

            if current_node.next is None:
                current_node.next = node
                break

            previous_node = current_node
            current_node = current_node.next

    def delete(self, position):
        pass

    def traverse(self):
        if self.head is None:
            return

        current = self.head
        result = []
        while(True):
            result.append(str(current.data))
            if current.next is None:
                break
            current = current.next
        print(' -> '.join(result))



class Grade:
    def __init__(self, subject, score):
        self.subject = subject
        self.score = score

    def __str__(self):
        return '{}: {}'.format(self.subject, self.score)


def better_score(grade1, grade2):
    if grade1.score > grade2.score:
        return True
    return False


if __name__ == '__main__':
    single_linked3 = SingleLinked3(better_score)
    g1 = Grade('Ch1', 10)
    g2 = Grade('En1', 20)
    g3 = Grade('Ma1', 40)
    g4 = Grade('Ch2', 5)
    g5 = Grade('En2', 15)
    g6 = Grade('Ma2', 20)

    single_linked3.insert(g1)
    single_linked3.insert(g2)
    single_linked3.insert(g3)
    single_linked3.insert(g4)
    single_linked3.insert(g5)
    single_linked3.insert(g6)

    single_linked3.traverse()
