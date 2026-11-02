class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def traverse(self):
        print("traverse")
        h = self.head
        while h is not None:
            print(f"{h.data} -> ", end="")
            h = h.next
        print("\n")

    def append(self, n: Node):
        if self.head is None:
            self.head = n
            return

        h = self.head
        while h.next is not None:
            h = h.next
        h.next = n

    def pop(self):
        if self.head is None:
            return

        if self.head.next is None:
            self.head = None
            return

        current = self.head
        next_node = self.head.next
        while next_node.next is not None:
            current = next_node
            next_node = next_node.next

        current.next = None


if __name__ == "__main__":
    ll = LinkedList()
    
    ll.append(Node(1))
    ll.append(Node(2))
    ll.append(Node(3))
    ll.traverse()

    ll.pop()
    ll.traverse()

    ll.pop()
    ll.traverse()

    ll.pop()
    ll.traverse()

    ll.pop() 
    ll.append(Node(5))
    ll.traverse()