package main

import "fmt"

type Node struct {
	data int
	next *Node
}

func traverse(node *Node) {
	fmt.Print("traverse\n")
	for node != nil {
		fmt.Printf("%d -> ", node.data)
		node = node.next
	}
	fmt.Print("\n")
}

func append(head *Node, n *Node) {
	if head == nil {
		head = n // fail to change
		return
	}

	p := head
	for p.next != nil {
		p = p.next
	}
	p.next = n
}

func pop(head *Node) {
	if head.next == nil {
		head = nil
		return
	}

	c := head
	n := head.next
	for n.next != nil {
		c = n
		n = n.next
	}
	c.next = nil
}

func main() {
	node1 := Node{data: 1, next: nil}
	node2 := Node{2, nil}
	node3 := Node{3, nil}
	node1.next = &node2
	node2.next = &node3
	traverse(&node1)

	node4 := Node{4, nil}
	append(&node1, &node4)
	traverse(&node1)

	var node0 *Node
	node0 = nil
	node5 := Node{5, nil}
	append(node0, &node5)
	traverse(node0) // still nil not 5

	pop(&node1)
	traverse(&node1)
	pop(&node1)
	pop(&node1)
	pop(&node1)
	traverse(&node1) // still 1 not nil
}
