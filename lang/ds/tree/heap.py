class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return '{}: {}'.format(self.name, self.score)

    def __repr__(self):
        # return '{}, {}'.format(self.name, hex(id(self)))
        return '{}'.format(self.score)


def better_score(s1, s2):
    if s1.score > s2.score:
        return True
    return False


def equal_score(s1, s2):
    if s1.score == s2.score:
        return True
    return False


class Heap:
    """
         i
      /    \
     2i   2i+1
    """
    def __init__(self, data, comparison, size=100):
        self.heap = [None] * size
        self.comparison = comparison
        self.last_index = 0
        self.heap[self.last_index] = data

    def insert(self, data):
        self.last_index += 1
        self.heap[self.last_index] = data
        self.adjust_up(self.last_index)

    def delete(self, position=0):
        self.heap[self.last_index], self.heap[position] = None, self.heap[self.last_index]
        self.last_index -= 1
        self.adjust_down(position)

    def adjust_up_recursive(self, index):
        """
        recursive
        :param index:
        :return:
        """
        if index == 0:
            return

        parent_index = int((index - 1) / 2)
        if self.comparison(self.heap[index], self.heap[parent_index]):
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            self.adjust_up(parent_index)
        return

    def adjust_up(self, index):
        while index >= 0:
            parent_index = int((index - 1) / 2)
            if self.comparison(self.heap[index], self.heap[parent_index]):
                self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
                index = parent_index
                continue
            break

    def adjust_down(self, index):
        while True:
            child_index_0 = index * 2 + 1
            child_index_1 = index * 2 + 2
            child_0 = self.heap[child_index_0]
            child_1 = self.heap[child_index_1]

            if child_0 is None and child_1 is None:
                break

            if child_0 is None and self.comparison(child_1, self.heap[index]):
                self.heap[child_index_1], self.heap[index] = self.heap[index], self.heap[child_index_1]
                index = child_index_1
                continue

            if child_1 is None and self.comparison(child_0, self.heap[index]):
                self.heap[child_index_0], self.heap[index] = self.heap[index], self.heap[child_index_0]
                index = child_index_0
                continue

            better_child_index = child_index_1
            better_child = child_1
            if self.comparison(child_0, child_1):
                better_child_index = child_index_0
                better_child = child_0

            if self.comparison(better_child, self.heap[index]):
                self.heap[better_child_index], self.heap[index] = self.heap[index], self.heap[better_child_index]
                index = better_child_index
                continue

            break

    def show(self):
        print(self.heap[:self.last_index+1])


if __name__ == '__main__':
    # data
    s0 = Student('s0', 60)
    s1 = Student('s1', 20)
    s2 = Student('s2', 80)
    s3 = Student('s3', 10)
    s4 = Student('s4', 40)
    s5 = Student('s5', 30)
    s6 = Student('s6', 50)
    s7 = Student('s7', 70)
    s8 = Student('s8', 90)
    s9 = Student('s9', 100)
    s10 = Student('s10', 0)
    s11 = Student('s11', 15)

    MAX_ELEMENT = 100
    max_heap = Heap(s0, better_score, MAX_ELEMENT)

    for s in [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]:
        max_heap.insert(s)
        # max_heap.show()

    max_heap.show()
    max_heap.delete(0)
    max_heap.show()
