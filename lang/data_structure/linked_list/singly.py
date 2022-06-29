class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Linked_List:
    def __init__(self):
        self.head = None

    def traverse(self):
        print("traverse\n")
        h = self.head
        while (h != None):
            print(f"{h.data} -> ", end="")
            h = h.next
        print("\n")

    def append(self, n):
        if (self.head == None):
            self.head = n
            return

        h = self.head
        while (h.next != None):
            h = h.next
        h.next = n

    def pop(self):
        if self.head == None:
            return

        if self.head.next == None:
            self.head = None
            return

        c: Node = self.head
        n: Node = self.head.next
        while (n.next != None):
            c = n
            n = n.next

        c.next = None


linked_list1 = Linked_List()
linked_list1.append(Node(1))
linked_list1.append(Node(2))
linked_list1.append(Node(3))
linked_list1.traverse()

linked_list1.pop()
linked_list1.pop()
linked_list1.pop()  # head be None
linked_list1.traverse()
