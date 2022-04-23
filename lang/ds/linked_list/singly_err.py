from typing import Optional, Union


class Node:
    def __init__(self, data: int) -> None:
        self.data: int = data
        self.next: Union[Node, None] = None
        # self.next: Optional[Node] = None


def traverse(head: Optional[Node]) -> None:
    print("traverse\n")
    while (head != None):
        print(f"{head.data} -> ", end="")  # type: ignore[union-attr]
        head = head.next  # type: ignore[union-attr]
    print("\n")


def append(head: Optional[Node], n: Node) -> None:
    if (head == None):
        head = n  # fail to change
        return

    while (head.next != None):  # type: ignore[union-attr]
        head = head.next  # type: ignore[union-attr]
    head.next = n  # type: ignore[union-attr]


def pop(head: Optional[Node]) -> None:
    if head == None:
        return

    if head.next == None:  # type: ignore[union-attr]
        head = None  # fail to change
        return

    n: Node = head.next  # type: ignore
    while (n.next != None):  # type: ignore[union-attr]
        head = n
        n = n.next  # type: ignore

    head.next = None  # type: ignore[union-attr]


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node1.next = node2
node2.next = node3

traverse(node1)

node4 = Node(4)

append(node1, node4)
traverse(node1)

node0 = None
node5 = Node(5)

append(node0, node5)
traverse(node0)  # still be None not 5


pop(node1)
traverse(node1)
pop(node1)
pop(node1)
traverse(node1)  # still be 1 not None
